import express from "express";
import { createServer } from "@playwright/mcp";
import { SSEServerTransport } from "@modelcontextprotocol/sdk/server/sse.js";

// Playwright MCP サーバーを起動（headless オプションなど必要な設定を追加）
const server = createServer({
  launchOptions: { channel: "chromium", headless: false },
});

const app = express();

// 複数の同時接続をサポートするため、セッション ID をキーとした transports オブジェクトを用意
const transports: { [sessionId: string]: SSEServerTransport } = {};

// クライアントが SSE 接続を確立するエンドポイント
app.get("/sse", async (_, res) => {
  const transport = new SSEServerTransport("/messages", res);
  transports[transport.sessionId] = transport;

  // クライアント接続が切れた場合、transport を削除
  res.on("close", () => {
    delete transports[transport.sessionId];
  });

  // MCP サーバーに transport を接続
  await server.connect(transport);
});

// クライアントからのメッセージを受け付けるエンドポイント
app.post("/messages", async (req, res) => {
  const sessionId = req.query.sessionId as string;
  const transport = transports[sessionId];

  if (transport) {
    await transport.handlePostMessage(req, res);
  } else {
    res.status(400).send("No transport found for sessionId");
  }
});

// サーバーをポート 3001 で起動
app.listen(3001, () => {
  console.log("SSE MCP server is running on port 3001");
});
