# 悦都 Home Assistant UI 资源清单

本清单记录 Dashboard 运行时依赖，避免把 `source/` 下载目录误当成已安装资源。

当前 Dashboard 使用独立的 `全屋晶璃` 主题：蓝紫灰 Light、深蓝黑 Dark 通过主题 mode 自动切换；`全屋晶璃 Lite` 去除模糊，默认用于墙屏。2.5D 户型图、视频画面、标题、Mushroom Chips 和 Bubble 外层保持清晰，玻璃只作用于外层卡、控制卡和设备 Marker。

| 资源 | 用途 | 运行路径 | 来源/版本 |
| --- | --- | --- | --- |
| Mushroom | 标题、摘要、标准实体控制 | `/hacsfiles/lovelace-mushroom/mushroom.js` | HACS，现有资源记录 `hacstag=444350375511` |
| Bubble Card | 房间深度控制弹层 | `/hacsfiles/Bubble-Card/bubble-card.js` | HACS，现有资源记录 `hacstag=680112919325` |
| Card Mod | 少量共享卡片样式 | `/local/community/lovelace-card-mod/card-mod.js?v=4.1.0` | `source/lovelace-card-mod/card-mod.js`，4.1.0 |
| Button Card | 地图/设备状态徽标 | `/local/community/button-card/button-card.js?v=7.0.1` | button-card release v7.0.1 |
| Clock Weather Card | 首页与墙屏天气时钟、天气趋势 | `/hacsfiles/clock-weather-card/clock-weather-card.js` | HACS |
| Calendar Card Pro | 家庭未来日程与天气联动 | `/hacsfiles/calendar-card-pro/calendar-card-pro.js` | HACS |
| Chinese Almanac | 农历/黄历实体与详情卡 | 由自定义集成自动注册 | HACS，自定义集成；不重复声明 JS |
| 全屋晶璃 | Dashboard 自动 Light/Dark 玻璃主题 | `config/themes/crystal-home.yaml` | 本地独立主题，参考 `homeassistant-frosted-glass-themes` 的 mode/Card Mod 分层 |
| 全屋晶璃 Lite | 墙屏与低性能设备无模糊主题 | `config/themes/crystal-home-lite.yaml` | 本地降级主题，不使用 `backdrop-filter` |
| Crystal Home 背景 | Light/Dark 本地环境背景 | `/local/backgrounds/crystal-home-light.webp`、`crystal-home-dark.webp` | `config/www/backgrounds/` |

`dashboard-v2.yaml` 与 `dashboard-wall.yaml` 显式声明本地资源；Mushroom/Bubble 仍由 HACS 更新，避免手工复制覆盖 HACS 文件。升级任一资源时，同时更新本表、URL 版本参数并完成移动端/墙屏缓存刷新验证。

## 资源边界

- `source/` 下的开源仓库是参考源码和升级依据，不直接作为 HA 静态资源目录。
- `yuedu-warm.yaml` 与 `yuedu-frosted.yaml` 保留为回滚参考，不作为当前 Dashboard 基础主题。
- `yuedu-home-2p5d.png` 是当前唯一真实 2.5D 主图；没有真实 3D 模型和设备坐标前，不启用 3D 控制层。
