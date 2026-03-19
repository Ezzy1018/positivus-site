import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { SSEClientTransport } from "@modelcontextprotocol/sdk/client/sse.js";
import * as EventSourcePkg from "eventsource";

// Polyfill EventSource for Node environment where window is missing
globalThis.EventSource = EventSourcePkg.default || EventSourcePkg;

async function run() {
  const token = process.env.FIGMA_API_KEY;
  
  // Official Figma MCP SSE endpoint
  const transport = new SSEClientTransport(
    new URL("https://mcp.figma.com/mcp"),
    {
       requestInit: {
          headers: {
             "Authorization": `Bearer ${token}`
          }
       }
    }
  );

  const client = new Client(
    { name: "antigravity-agent", version: "1.0.0" },
    { capabilities: { tools: {} } }
  );

  console.log("Connecting remotely to Figma Official MCP via SSE...");
  try {
      await client.connect(transport);
      console.log("Connected Successfully.");

      console.log("Triggering official 'generate_figma_design' (Code-to-Canvas)...");
      const result = await client.callTool({
        name: "generate_figma_design",
        arguments: {
          url: "http://localhost:8080/index.html",
          destinationFileUrl: "https://www.figma.com/design/s9hXBJXnZZGbIPuL7etZfL/Positivus-Landing-Page-Design--Community-?node-id=1912-153"
        }
      });

      console.log("Push Complete!");
      console.log(JSON.stringify(result, null, 2));
      
  } catch (err) {
      console.error("Execution Failed:", err.message);
  } finally {
      process.exit(0);
  }
}

run();
