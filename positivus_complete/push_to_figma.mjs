import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

async function run() {
  const transport = new StdioClientTransport({
    command: "npx",
    args: ["-y", "figma-developer-mcp", `--figma-api-key=${process.env.FIGMA_API_KEY}`, "--stdio"],
  });

  const client = new Client(
    { name: "antigravity-figma-pusher", version: "1.0.0" },
    { capabilities: { tools: {} } }
  );

  console.log("Connecting to Figma MCP Server...");
  await client.connect(transport);

  console.log("Executing generate_figma_design tool...");
  const result = await client.callTool({
    name: "generate_figma_design",
    arguments: {
      url: "http://localhost:8080/index.html",
      destinationFileUrl: "https://www.figma.com/design/s9hXBJXnZZGbIPuL7etZfL/Positivus-Landing-Page-Design--Community-?node-id=1912-153"
    }
  });

  console.log("Code to Canvas Initiated Successfully!");
  console.log(JSON.stringify(result, null, 2));
  
  // Close gracefully
  process.exit(0);
}

run().catch(console.error);
