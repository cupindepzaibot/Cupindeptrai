const express = require("express");
const bodyParser = require("body-parser");
const { WebSocketServer } = require("ws");

const app = express();
app.use(bodyParser.json());

// test endpoint
app.get("/", (req, res) => {
  res.send("tele-webhook-server running");
});

let wsClients = [];

// webhook endpoint từ Telegram
app.post("/webhook", (req, res) => {
  console.log("Telegram update:", JSON.stringify(req.body).slice(0, 200));
  const payload = JSON.stringify(req.body);
  wsClients.forEach(ws => {
    if (ws.readyState === 1) {
      try { ws.send(payload); } catch (e) { console.error("ws send err", e); }
    }
  });
  res.sendStatus(200);
});

const PORT = process.env.PORT || 3000;
const server = app.listen(PORT, () => {
  console.log("Server listening on port", PORT);
});

// WebSocket server
const wss = new WebSocketServer({ server });
wss.on("connection", (ws, req) => {
  console.log("WS client connected", req.socket && req.socket.remoteAddress);
  wsClients.push(ws);
  try { ws.send(JSON.stringify({ type: "hello", msg: "welcome" })); } catch {}
  ws.on("close", () => {
    wsClients = wsClients.filter(c => c !== ws);
  });
});
