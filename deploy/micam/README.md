# 悦都摄像机桥接

该目录独立运行 Miloco、Micam 与 go2rtc，不修改现有 Home Assistant Compose。

## 首次启动

```powershell
Copy-Item .env.example .env
docker compose up -d miloco go2rtc
```

在本机浏览器打开 `https://localhost:8000`，接受自签名证书后设置 Miloco 密码并绑定小米账号。

随后在 Miloco 中找到小米智能摄像机 3 云台版（`chuangmi.camera.069a01`）的设备 DID；将 `.env` 中的 `MILOCO_PASSWORD` 填为该密码的**小写 MD5**，填写 `CAMERA_ID`，再执行：

```powershell
docker compose --profile camera up -d micam1
```

验证 RTSP 输出：`rtsp://127.0.0.1:8554/yuedu_living_camera`。

## 安全约束

- 仅在内网使用；不要暴露 8000、1984、8554 端口到公网。
- `.env` 和 `miloco/` 含账号授权或运行数据，已忽略提交。
- 确认本机视频可播放后，再把 RTSP 接入 Home Assistant 的 Generic Camera 并更新仪表盘。
