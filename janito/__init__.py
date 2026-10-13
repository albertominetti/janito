"""
Janito - AI Coding Agent with tools, MCP, and skills.

An AI Coding Agent with terminal and browser interfaces, built-in tools,
MCP (Model Context Protocol) support, and task-specific skills.
"""

from ._version import __version__, __version_tuple__
from .mcp_client.base import MCPTransport
from .mcp_client.factory import create_transport
from .mcp_client.http import HttpTransport
from .mcp_client.stdio import StdioTransport

# MCP modules
from .mcp_config import (
    add_service,
    get_mcp_config_path,
    get_service,
    list_services,
    load_mcp_config,
    remove_service,
    save_mcp_config,
)
from .mcp_manager import MCPManager, get_mcp_manager, shutdown_mcp_manager

__all__ = [
    # Version
    "__version__",
    "__version_tuple__",
    # MCP Config
    "get_mcp_config_path",
    "load_mcp_config",
    "save_mcp_config",
    "get_service",
    "add_service",
    "remove_service",
    "list_services",
    # MCP Client
    "MCPTransport",
    "StdioTransport",
    "HttpTransport",
    "create_transport",
    # MCP Manager
    "MCPManager",
    "get_mcp_manager",
    "shutdown_mcp_manager",
]
