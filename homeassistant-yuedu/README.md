# 悦都全屋 Home Assistant 原生仪表盘

`dashboard-v2.yaml` 是可部署的新版仪表盘：总览只显示家庭状态和空间入口，户型图、客厅、主卧、阳台与未来空间各自独立，避免单页堆叠全部设备。完整的空间分析和扩展约定见 [空间模型规划.md](空间模型规划.md)。

## 部署

1. 在 Home Assistant 主机创建目录：`/config/dashboards`、`/config/www/floorplan`。
2. 复制 `dashboard-v2.yaml` 到 `/config/dashboards/dashboard-v2.yaml`，复制 `configuration-dashboard-v2.yaml` 中的 `lovelace.dashboards.yuedu-v2` 段到现有 `/config/configuration.yaml` 的 `lovelace:` 下。
3. 复制 `www/floorplan/yuedu-home-2p5d.png` 到 `/config/www/floorplan/yuedu-home-2p5d.png`。该图是根据用户户型重绘的 2.5D 底图；原始裁切平面图保留作参考，不作为新版页面底图。
4. 在“开发者工具 → YAML”检查配置并重启 Home Assistant；侧栏会出现“悦都全屋”。

项目使用原生 Lovelace 卡片和 `picture-elements`，不依赖 HACS。摄像机没有 `camera.*` 视频流实体，因此不提供失效的实时画面；门锁只有传感器实体，因此只展示状态和电量、不提供远程解锁。

`lovelace-yuedu.yaml` 和 `hearth.yaml` 是此前的单页/Fusion 方案，保留作回退参考；部署 v2 时不需要替换它们。

## HomeKit 与快捷模式

`homekit.yaml` 将主卧空调、循环扇、客厅摄像机开关和阳台洗衣机电源桥接给 Apple Home；门锁不桥接，避免远程解锁风险。`scripts.yaml` 提供“离家”和“睡眠”模式：它们不写死空调温度，保留家庭的实际舒适度偏好。部署后在 Home Assistant 的通知中取得 HomeKit 配对码，并在 iPhone“家庭”App 中扫描完成最终配对。
