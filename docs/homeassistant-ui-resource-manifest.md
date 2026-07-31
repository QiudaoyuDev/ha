# 悦都 Home Assistant UI 资源清单

本清单记录 Dashboard 运行时依赖，避免把 `source/` 下载目录误当成已安装资源。

当前 Dashboard 使用 `悦都暖雾` 主题：它沿用悦都暖石配色，仅对普通信息卡启用轻量毛玻璃；2.5D 户型图、标题、Mushroom Chips 和 Bubble 弹层保持清晰。

| 资源 | 用途 | 运行路径 | 来源/版本 |
| --- | --- | --- | --- |
| Mushroom | 标题、摘要、标准实体控制 | `/hacsfiles/lovelace-mushroom/mushroom.js` | HACS，现有资源记录 `hacstag=444350375511` |
| Bubble Card | 房间深度控制弹层 | `/hacsfiles/Bubble-Card/bubble-card.js` | HACS，现有资源记录 `hacstag=680112919325` |
| Card Mod | 少量共享卡片样式 | `/local/community/lovelace-card-mod/card-mod.js?v=4.1.0` | `source/lovelace-card-mod/card-mod.js`，4.1.0 |
| Button Card | 地图/设备状态徽标 | `/local/community/button-card/button-card.js?v=7.0.1` | button-card release v7.0.1 |
| Clock Weather Card | 首页与墙屏天气时钟、天气趋势 | `/hacsfiles/clock-weather-card/clock-weather-card.js` | HACS |
| Calendar Card Pro | 家庭未来日程与天气联动 | `/hacsfiles/calendar-card-pro/calendar-card-pro.js` | HACS |
| Chinese Almanac | 农历/黄历实体与详情卡 | 由自定义集成自动注册 | HACS，自定义集成；不重复声明 JS |
| 悦都暖雾 | Dashboard 全局视觉主题 | `config/themes/yuedu-frosted.yaml` | 本地派生主题，依赖 Card Mod |

`dashboard-v2.yaml` 与 `dashboard-wall.yaml` 显式声明本地资源；Mushroom/Bubble 仍由 HACS 更新，避免手工复制覆盖 HACS 文件。升级任一资源时，同时更新本表、URL 版本参数并完成移动端/墙屏缓存刷新验证。

## 资源边界

- `source/` 下的开源仓库是参考源码和升级依据，不直接作为 HA 静态资源目录。
- UI Lovelace Minimalist 与毛玻璃主题暂不注册为默认主题；它们保留在 source 目录，待独立视觉方案评审后再接入。
- `yuedu-home-2p5d.png` 是当前唯一真实 2.5D 主图；没有真实 3D 模型和设备坐标前，不启用 3D 控制层。
