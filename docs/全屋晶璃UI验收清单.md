# 全屋晶璃 UI 验收清单

## 静态与配置

- [ ] `dashboard-v2.yaml`、`dashboard-wall.yaml`、两个主题 YAML 可解析。
- [ ] Home Assistant `check_config` 通过且无主题重复键警告。
- [ ] 两张 Crystal 背景和原有 2.5D 户型图均存在。
- [ ] `git ls-files` 不包含 `.storage/`、`secrets.yaml`、数据库、日志、缓存或 Token。

## 页面

- [ ] `/yuedu-home/home` 首屏突出家庭状态和户型图，不显示未来五日天气、常用空间四宫格或无设备预留入口。
- [ ] `/yuedu-home/map` 有真实设备 Marker、房间入口和一致 Tap/Hold 行为。
- [ ] Agenda 承载完整天气、7 日日历和万年历；首页只保留天气摘要和下一事件。
- [ ] 墙屏默认使用 `全屋晶璃 Lite`，桌面/移动端可切换 Standard 与 Lite。

## 安全与控制

- [ ] 门锁只读，无远程开锁控件。
- [ ] 离家模式、结束洗涤、关闭摄像机电源均有确认。
- [ ] 设备离线时隐藏可执行控件并显示“设备离线，正在等待米家连接”。
- [ ] 摄像机无视频实体时不伪造画面，视频区不模糊。
- [ ] 空调、循环扇、洗衣机控制仍绑定已确认的实体 ID。

## 视觉与性能

- [ ] Light/Dark 正文有足够对比度，Marker 坐标在移动端不重叠。
- [ ] Bubble 弹层没有重复 Blur；Select 下拉正常。
- [ ] Lite 文件不包含 `backdrop-filter: blur`。
