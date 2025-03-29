playwright-mcpをsse server化してagent-sdkと連携。
ついでに、カスタムsse serverも同時に起動して複数mcp-serverとの接続の動作確認も実施

```bash
npm install

npx tsc

uv run python app.py
```

```bash
(node:8885) [MODULE_TYPELESS_PACKAGE_JSON] Warning: Module type of file:///Users/kyojin/Documents/agent_sdk_w_mcp/dist/index.js is not specified and it doesn't parse as CommonJS.
Reparsing as ES module because module syntax was detected. This incurs a performance overhead.
To eliminate this warning, add "type": "module" to /Users/kyojin/Documents/agent_sdk_w_mcp/package.json.
(Use `node --trace-warnings ...` to show where the warning was created)
SSE MCP server is running on port 3001
Starting SSE server at http://localhost:8000/sse ...
INFO:     Started server process [8922]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
SSE server started. Running example...


INFO:     127.0.0.1:49878 - "GET /sse HTTP/1.1" 200 OK
INFO:     127.0.0.1:49880 - "POST /messages/?session_id=56a94791647c4707a19f9f4197028d72 HTTP/1.1" 202 Accepted
View trace: https://platform.openai.com/traces/trace_8ec633e0f32947388f6b94d95bd62c4c

Enter a prompt (MCP servers (playwright-mcp, sse) are available): 大谷翔平のホームランの数を教えて  
INFO:     127.0.0.1:49884 - "POST /messages/?session_id=56a94791647c4707a19f9f4197028d72 HTTP/1.1" 202 Accepted
INFO:     127.0.0.1:49884 - "POST /messages/?session_id=56a94791647c4707a19f9f4197028d72 HTTP/1.1" 202 Accepted
Processing request of type ListToolsRequest
大谷翔平は、2025年シーズンに2本のホームランを打っています。また、2024年シーズンには54本のホームランを打ち、ナショナルリーグで1位となっています。

最新情報や詳細については、[MLBの公式サイト](https://www.mlb.com/player/shohei-ohtani-660271)を参照してください。


Running: What's the secret word?
INFO:     127.0.0.1:50015 - "POST /messages/?session_id=56a94791647c4707a19f9f4197028d72 HTTP/1.1" 202 Accepted
Processing request of type ListToolsRequest
INFO:     127.0.0.1:50015 - "POST /messages/?session_id=56a94791647c4707a19f9f4197028d72 HTTP/1.1" 202 Accepted
Processing request of type CallToolRequest
[debug-server] get_secret_word()
The secret word is "banana." 🍌
```