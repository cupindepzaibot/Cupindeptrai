# tele-webhook-server

Nhận webhook từ Telegram và phát cho client qua WebSocket.

## Cách dùng
1. Deploy lên Render, Railway, hoặc Heroku.
2. Sau khi deploy xong, bạn có URL server (vd: https://your-app.onrender.com).

## Set Telegram webhook
Dùng lệnh (thay BOT_TOKEN và SERVER_URL):
```bash
curl -X POST "https://api.telegram.org/bot<BOT_TOKEN>/setWebhook?url=<SERVER_URL>/webhook"
