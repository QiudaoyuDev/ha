#requires -RunAsAdministrator
$ErrorActionPreference = 'Stop'

# The broadcaster must run on Windows, where it can send Bonjour multicast to
# the physical LAN. Docker Desktop's Linux VM cannot do that for this bridge.
$taskName = 'HomeAssistant-HomeKit-mDNS'
$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$launcher = Join-Path $scriptRoot 'start-homekit-mdns-advertiser.ps1'

$python = 'C:\Users\lzx10\AppData\Local\Python\pythoncore-3.14-64\python.exe'
if (-not (Test-Path -LiteralPath $python)) {
    throw "Python executable was not found: $python"
}

& $python -m pip install --user -r (Join-Path $scriptRoot 'requirements-homekit-mdns.txt')

$action = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument (
    '-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File "{0}"' -f $launcher
)
$trigger = New-ScheduledTaskTrigger -AtLogOn
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -StartWhenAvailable -RestartCount 3 -RestartInterval (New-TimeSpan -Minutes 1)
Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Description 'Advertises the Home Assistant HomeKit bridge over Windows LAN mDNS.' -Force | Out-Null

# Permit HomeKit HAP pairing/control and Bonjour only on trusted networks.
New-NetFirewallRule -DisplayName 'Home Assistant HomeKit HAP TCP 21063' -Direction Inbound -Action Allow -Protocol TCP -LocalPort 21063 -Profile Private -ErrorAction SilentlyContinue | Out-Null
New-NetFirewallRule -DisplayName 'Home Assistant HomeKit mDNS UDP 5353' -Direction Inbound -Action Allow -Protocol UDP -LocalPort 5353 -Profile Private -ErrorAction SilentlyContinue | Out-Null

Start-ScheduledTask -TaskName $taskName
Write-Host "Installed and started scheduled task: $taskName"
