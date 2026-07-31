# 悦都全屋 Home Assistant 原生仪表盘

`dashboard-v2.yaml` 是可部署的新版仪表盘：`/yuedu-home/home` 以家庭状态、真实 2.5D 户型图、天气摘要和按需设备入口为主；地图、客厅、主卧、阳台与 Agenda 分页承载更完整的信息和控制。视觉主题为独立的“全屋晶璃”，提供自动 Light/Dark、显式 Light/Dark 和墙屏优先的 Lite 无模糊版本。设计与验收边界见 [全屋晶璃主题设计规范](docs/全屋晶璃主题设计规范.md) 和 [全屋晶璃 UI 验收清单](docs/全屋晶璃UI验收清单.md)。

## 部署

1. 在 Home Assistant 主机创建目录：`/config/dashboards`、`/config/www/floorplan`。
2. 复制 `dashboard-v2.yaml` 到 `/config/dashboards/dashboard-v2.yaml`，复制 `configuration-dashboard-v2.yaml` 中的 `lovelace.dashboards.yuedu-v2` 段到现有 `/config/configuration.yaml` 的 `lovelace:` 下。
3. 复制 `www/floorplan/yuedu-home-2p5d.png` 到 `/config/www/floorplan/yuedu-home-2p5d.png`。该图是根据用户户型重绘的 2.5D 底图；原始裁切平面图保留作参考，不作为新版页面底图。
4. 在“开发者工具 → YAML”检查配置并重启 Home Assistant；侧栏会出现“悦都全屋”。

5. 确认 `/config/www/backgrounds/crystal-home-light.webp` 与 `crystal-home-dark.webp` 已复制；用户主题选择“全屋晶璃”即可自动跟随系统明暗，墙屏 Dashboard 使用“全屋晶璃 Lite”。

6. 参考仓库主题已注册为 `Frosted Glass`、`Frosted Glass Light/Dark`、`Frosted Glass Lite` 及对应 Light/Dark Lite 版本；它们不会自动替换当前 Dashboard，可在用户主题选择器中手动切换。

项目使用原生 Lovelace 卡片、`picture-elements` 和少量 HACS 卡片。摄像机没有可用实时流时只展示离线/未接入语义；门锁只有传感器实体，因此只展示状态和电量、不提供远程解锁。Lite 版本不使用 `backdrop-filter`，用于墙屏、下拉菜单和低性能设备。

Home Assistant 运行时文件（`.storage/`、`secrets.yaml`、数据库、日志、缓存和 `.HA_VERSION`）由 `.gitignore` 排除，不能提交到仓库。已存在的运行实例仍需在 HA 中注销旧会话并轮换已暴露的凭据。

## 天气、家庭日历与万年历

详细实施边界见 [天气日历万年历集成实施方案](docs/悦都全屋_天气日历万年历集成实施方案_20260731.md)。首次部署按以下顺序完成：

1. 在“设置 → 设备与服务 → 添加集成”中添加并配置 Open-Meteo Enhanced（或官方 Open-Meteo），选择 Home Zone。当前实例实际实体为 `weather.wo_de_jia`，如后续重命名，需同步 Dashboard 与模板中的实体 ID。
2. 添加两个官方 Local Calendar。当前实例实际实体为 `calendar.calendar_yuedu_family` 与 `calendar.calendar_yuedu_birthdays`；如果重新创建，日历名称只填写“悦都家庭”和“悦都生日纪念日”，不要填写完整 entity ID。墙屏只引用这两个家庭共享日历，不展示地点、描述或会议链接。
3. 通过 HACS 安装 `clock-weather-card` 与 `calendar-card-pro`，安装后确认 `/hacsfiles/clock-weather-card/clock-weather-card.js` 和 `/hacsfiles/calendar-card-pro/calendar-card-pro.js` 可访问。
4. 通过 HACS 安装 `knoop7/ha_laohuangli`，重启后添加“中国老黄历”集成。只启用基础历法，不启用生日、事件、通知和 AI 预测。
5. 老黄历实体已按当前实例接入 `sensor.zhong_guo_lao_huang_li_nong_li`、`sensor.zhong_guo_lao_huang_li_jie_qi` 和 `sensor.zhong_guo_lao_huang_li_jin_ri_jie_ri`；如果重新配置集成后实体 ID 发生变化，再以开发者工具实际结果同步模板。不得猜测或提交 `.storage`、账号、Token、API Key 和日历隐私数据。
6. 运行 `deploy/homeassistant/scripts/check-weather-calendar.sh` 检查本地依赖，然后执行 Home Assistant 配置检查并重启。

实体和资源验证完成后，用 iPhone 强制刷新前端；墙屏端清理浏览器缓存后重新打开“悦都墙屏”。如果第三方卡片异常，可暂时改用 `weather-forecast` 与原生 `calendar` 卡验证数据源，设备控制与 HomeKit 不依赖本次新增卡片。

`lovelace-yuedu.yaml` 和 `hearth.yaml` 是此前的单页/Fusion 方案，保留作回退参考；部署 v2 时不需要替换它们。

## HomeKit 与快捷模式

`homekit.yaml` 将主卧空调、循环扇、客厅摄像机开关和阳台洗衣机电源桥接给 Apple Home；门锁不桥接，避免远程解锁风险。`scripts.yaml` 提供“离家”和“睡眠”模式：它们不写死空调温度，保留家庭的实际舒适度偏好。部署后在 Home Assistant 的通知中取得 HomeKit 配对码，并在 iPhone“家庭”App 中扫描完成最终配对。
