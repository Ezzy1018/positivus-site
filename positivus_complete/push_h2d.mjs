import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { SSEClientTransport } from "@modelcontextprotocol/sdk/client/sse.js";
import * as EventSourcePkg from "eventsource";
import fs from "fs";
import path from "path";

globalThis.EventSource = EventSourcePkg.default || EventSourcePkg;

async function run() {
  const url = "https://h2d-mcp.divriots.com/315071b7-e8c1-4e97-8632-045da0267852/mcp";
  const transport = new SSEClientTransport(new URL(url));

  const client = new Client(
    { name: "antigravity-agent", version: "1.0.0" },
    { capabilities: { tools: {} } }
  );

  console.log("Preparing Positivus 1:1 Bundle...");
  
  const baseDir = "/Users/Akshi/Desktop/Test Dox/Figma test/positivus_complete";
  const htmlPath = path.join(baseDir, "index.html");
  const cssPath = path.join(baseDir, "css/main.css");

  let htmlContent = fs.readFileSync(htmlPath, "utf8");
  const cssContent = fs.readFileSync(cssPath, "utf8");

  // Inline the CSS
  const inlinedStyle = `<style>\n${cssContent}\n</style>`;
  htmlContent = htmlContent.replace('<link rel="stylesheet" href="css/main.css">', inlinedStyle);

  console.log("Connecting to html.to.design MCP...");
  try {
      await client.connect(transport);
      console.log("Connected.");

      console.log("Executing 'import-html' to Node 1912:153...");
      const result = await client.callTool({
        name: "import-html",
        arguments: {
          name: "Positivus Full Page 1:1 Push",
          html: htmlContent,
          intoNodeId: "1912:153"
        }
      });

      console.log("Push Result:", JSON.stringify(result, null, 2));
      
  } catch (err) {
      console.error("Failed:", err.message);
  } finally {
      process.exit(0);
  }
}

run();
