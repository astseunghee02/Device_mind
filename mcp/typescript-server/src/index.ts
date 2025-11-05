#!/usr/bin/env node

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

/**
 * Custom MCP Server
 *
 * This server provides tools and resources for integration with Claude Code.
 */

class CustomMCPServer {
  private server: Server;

  constructor() {
    this.server = new Server(
      {
        name: "custom-mcp-server",
        version: "1.0.0",
      },
      {
        capabilities: {
          tools: {},
          resources: {},
        },
      }
    );

    this.setupHandlers();
    this.setupErrorHandling();
  }

  private setupHandlers(): void {
    // Handle list_tools request
    this.server.setRequestHandler(ListToolsRequestSchema, async () => {
      return {
        tools: [
          // TODO: Add your tools here
          // Example:
          // {
          //   name: "example_tool",
          //   description: "An example tool",
          //   inputSchema: {
          //     type: "object",
          //     properties: {
          //       param1: {
          //         type: "string",
          //         description: "First parameter",
          //       },
          //     },
          //     required: ["param1"],
          //   },
          // },
        ],
      };
    });

    // Handle call_tool request
    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;

      try {
        switch (name) {
          // TODO: Implement your tool handlers here
          // Example:
          // case "example_tool":
          //   return await this.handleExampleTool(args);

          default:
            throw new Error(`Unknown tool: ${name}`);
        }
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : String(error);
        return {
          content: [
            {
              type: "text",
              text: `Error: ${errorMessage}`,
            },
          ],
          isError: true,
        };
      }
    });
  }

  // TODO: Add your tool implementation methods here
  // Example:
  // private async handleExampleTool(args: any) {
  //   const { param1 } = args;
  //
  //   // Your tool logic here
  //
  //   return {
  //     content: [
  //       {
  //         type: "text",
  //         text: `Result: ${param1}`,
  //       },
  //     ],
  //   };
  // }

  private setupErrorHandling(): void {
    this.server.onerror = (error) => {
      console.error("[MCP Error]", error);
    };

    process.on("SIGINT", async () => {
      await this.server.close();
      process.exit(0);
    });
  }

  async run(): Promise<void> {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error("Custom MCP Server running on stdio");
  }
}

// Start the server
const server = new CustomMCPServer();
server.run().catch(console.error);
