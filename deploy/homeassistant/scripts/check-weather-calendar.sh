#!/usr/bin/env bash
set -euo pipefail

CONFIG_DIR="${1:-$(cd "$(dirname "$0")/.." && pwd)/config}"
COMMUNITY_DIR="$CONFIG_DIR/www/community"
failed=0

check_hacs_card() {
  local name="$1"
  local file="$2"
  if [[ -f "$COMMUNITY_DIR/$file" ]]; then
    echo "[OK] $name: $COMMUNITY_DIR/$file"
  else
    echo "[MISSING] $name: expected HACS file $COMMUNITY_DIR/$file"
    failed=1
  fi
}

check_hacs_card "Clock Weather Card" "clock-weather-card/clock-weather-card.js"
check_hacs_card "Calendar Card Pro" "calendar-card-pro/calendar-card-pro.js"

almanac_dir=""
for candidate in chinese_calendar chinese-almanac ha_laohuangli; do
  if [[ -d "$CONFIG_DIR/custom_components/$candidate" ]]; then
    almanac_dir="$CONFIG_DIR/custom_components/$candidate"
    break
  fi
done

if [[ -n "$almanac_dir" ]]; then
  echo "[OK] Chinese Almanac integration: $almanac_dir"
else
  echo "[OPTIONAL MISSING] Chinese Almanac integration is not installed."
fi

if [[ ! -f "$CONFIG_DIR/templates/yuedu_weather_calendar.yaml" ]]; then
  echo "[MISSING] Semantic template: $CONFIG_DIR/templates/yuedu_weather_calendar.yaml"
  failed=1
else
  echo "[OK] Semantic template: $CONFIG_DIR/templates/yuedu_weather_calendar.yaml"
fi

exit "$failed"
