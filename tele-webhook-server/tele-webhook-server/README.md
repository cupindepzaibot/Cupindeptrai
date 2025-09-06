# tele-webhook-server

Nhận webhook từ Telegram và broadcast tới WebSocket clients (Chrome extension).

## Deploy (Render / Railway)
- Push repo chứa thư mục `tele-webhook-server/` lên GitHub.
- Trên Render: New → Blueprint → chọn repo → Deploy.
- Render sẽ đọc render.yaml và deploy code trong `tele-webhook-server/`.

## Set Telegram webhook
Thay <BOT_TOKEN> và <SERVER_URL>:
