"""
Cohere North MCP Server

A Model Context Protocol (MCP) server built using the Cohere North MCP Python SDK.
Provides example tools that can be called by Cohere's North platform or locally
via the MCP Inspector.

Usage:
    # Run with authentication (for production / North platform)
    python server.py

    # Run WITHOUT auth for local testing with MCP Inspector
    python server.py --no-auth

    # Run with stdio transport (for MCP Inspector local testing)
    python server.py --no-auth --transport stdio
"""

import argparse
import datetime

from fastmcp import FastMCP

from north_mcp_python_sdk import NorthMCPServer

SERVER_NAME = "Cohere MCP Server"
SERVER_PORT = 5222


def create_server(use_auth: bool) -> FastMCP:
    """Create the MCP server with or without North authentication."""
    if use_auth:
        mcp = NorthMCPServer(
            name=SERVER_NAME,
            port=SERVER_PORT,
            host="0.0.0.0",
            instructions="A helpful MCP server with utility tools.",
        )
    else:
        mcp = FastMCP(
            name=SERVER_NAME,
            port=SERVER_PORT,
            host="0.0.0.0",
            instructions="A helpful MCP server with utility tools.",
        )

    # ─── Register Tools ───────────────────────────────────────────────────

    @mcp.tool()
    def execute_sql_query(query: str) -> str:
        """Execute an SQL query on the configured local SQLite database.
        Returns the data in a JSON array format.
        
        CRITICAL SYSTEM INSTRUCTIONS FOR AGENT:
        1. This database is SQLite, NOT PostgreSQL. 
        2. Do NOT use PostgreSQL syntax like `SERIAL`. Use `INTEGER PRIMARY KEY AUTOINCREMENT`.
        3. Do NOT use PostgreQL-specific types or functions. Data types should be SQLite compatible (TEXT, INTEGER, REAL, BLOB).
        4. You can execute multiple SQL statements separated by semicolons.
        """
        import json
        import db
        
        try:
            results = db.execute_query(query)
            # Default helper to serialize things like date/datetime that may come from DB
            return json.dumps(results, default=str, indent=2)
        except Exception as e:
            return f"Error executing query: {str(e)}"

    return mcp


# ─── Entry Point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cohere North MCP Server")
    parser.add_argument(
        "--transport",
        choices=["streamable-http", "stdio"],
        default="streamable-http",
        help="Transport type (default: streamable-http)",
    )
    parser.add_argument(
        "--no-auth",
        action="store_true",
        help="Disable North authentication (for local development/testing)",
    )
    args = parser.parse_args()

    mcp = create_server(use_auth=not args.no_auth)

    auth_status = "WITHOUT auth (local mode)" if args.no_auth else "WITH North auth"
    print(f"Starting {SERVER_NAME} on port {SERVER_PORT}")
    print(f"  Transport: {args.transport}")
    print(f"  Auth: {auth_status}")
    mcp.run(transport=args.transport)
