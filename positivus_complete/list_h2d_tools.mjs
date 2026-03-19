import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { SSEClientTransport } from "@modelcontextprotocol/sdk/client/sse.js";
import * as EventSourcePkg from "eventsource";

globalThis.EventSource = EventSourcePkg.default || EventSourcePkg;

async function run() {
  const url = "https://h2d-mcp.divriots.com/315071b7-e8c1-4e97-8632-045da0267852/mcp";
  const transport = new SSEClientTransport(new URL(url));

  const client = new Client(
    { name: "antigravity-agent", version: "1.0.0" },
    { capabilities: { tools: {} } }
  );

  console.log("Connecting to html.to.design MCP...");
  try {
      await client.connect(transport);
      console.log("Connected.");

      const tools = await client.listTools();
      console.log("Tools:", JSON.stringify(tools, null, 2));
      
  } catch (err) {
      console.error("Failed:", err.message);
  } finally {
      process.exit(0);
  }
}

run();
