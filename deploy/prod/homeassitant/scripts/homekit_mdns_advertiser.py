#!/usr/bin/env python3
"""Publish the Home Assistant HomeKit bridge on the Windows LAN.

Docker Desktop host networking is layer-4 only.  The HAP TCP listener is
available through Windows, but its multicast DNS announcement remains in the
Docker VM.  This process announces the existing bridge from the Windows host;
it never handles pairing or device control.
"""

from __future__ import annotations

import logging
import signal
import subprocess
import sys
import time
import json
from typing import Any, Dict

try:
    from zeroconf import ServiceInfo, Zeroconf
except ImportError as exc:
    raise SystemExit("Missing dependency: run `python -m pip install zeroconf==0.150.0`") from exc


SERVICE_TYPE = "_hap._tcp.local."
CONTAINER_NAME = "homeassistant-local"

# Querying the HA process gives us the current setup hash (sh). pyhap generates
# that hash at every HA start, so re-creating it from files on Windows would
# advertise stale pairing metadata after a restart.
CONTAINER_QUERY = r'''
from zeroconf import Zeroconf, ServiceBrowser, ServiceStateChange
import json, time
services = []
def handler(zeroconf, service_type, name, state_change, **kwargs):
    if state_change is not ServiceStateChange.Added:
        return
    info = zeroconf.get_service_info(service_type, name, timeout=1500)
    if info and info.port == 21063:
        services.append({
            "name": name, "server": info.server, "port": info.port,
            "addresses": info.parsed_addresses(),
            "properties": {key.decode(): (value or b"").decode() for key, value in info.properties.items()},
        })
zc = Zeroconf()
ServiceBrowser(zc, "_hap._tcp.local.", handlers=[handler])
time.sleep(3)
zc.close()
if not services:
    raise SystemExit("HomeKit HAP service on port 21063 was not found")
print(json.dumps(services[0], ensure_ascii=False))
'''


def load_native_service() -> Dict[str, Any]:
    """Read the actual HAP mDNS record from the Docker network namespace."""
    try:
        completed = subprocess.run(
            ["docker", "exec", "-i", CONTAINER_NAME, "python3", "-"],
            input=CONTAINER_QUERY,
            capture_output=True,
            text=True,
            timeout=12,
            check=True,
        )
        value = json.loads(completed.stdout)
    except (OSError, subprocess.SubprocessError, json.JSONDecodeError) as exc:
        raise RuntimeError("Cannot read HomeKit mDNS metadata from Docker: {}".format(exc)) from exc
    if not isinstance(value, dict) or not value.get("name") or not value.get("addresses"):
        raise RuntimeError("Invalid HomeKit mDNS metadata returned by Docker")
    return value


def make_service(native_service: Dict[str, Any]) -> ServiceInfo:
    """Publish an exact copy of HA's HAP DNS-SD record from Windows."""
    return ServiceInfo(
        SERVICE_TYPE,
        native_service["name"],
        addresses=[bytes(map(int, address.split("."))) for address in native_service["addresses"]],
        port=int(native_service["port"]),
        properties=native_service["properties"],
        server=native_service["server"],
    )


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    zeroconf = Zeroconf()
    stopped = False
    service = None

    def stop(*_: object) -> None:
        nonlocal stopped
        stopped = True

    signal.signal(signal.SIGINT, stop)
    signal.signal(signal.SIGTERM, stop)
    try:
        while not stopped:
            try:
                native_service = load_native_service()
                desired = make_service(native_service)
                if service is None:
                    zeroconf.register_service(desired, cooperating_responders=True)
                    service = desired
                    logging.info("HomeKit mDNS announced: %s -> %s:%s", desired.name, native_service["addresses"], desired.port)
                elif service.name != desired.name or service.properties != desired.properties:
                    zeroconf.unregister_service(service)
                    zeroconf.register_service(desired, cooperating_responders=True)
                    service = desired
                    logging.info("HomeKit mDNS metadata refreshed")
            except RuntimeError as exc:
                logging.warning("HomeKit mDNS metadata is not ready: %s", exc)
            for _ in range(30):
                if stopped:
                    break
                time.sleep(1)
    finally:
        if service is not None:
            zeroconf.unregister_service(service)
        zeroconf.close()
        logging.info("HomeKit mDNS advertiser stopped")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # Keep failure visible to the scheduled task log.
        logging.exception("HomeKit mDNS advertiser failed: %s", exc)
        raise
