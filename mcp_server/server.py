import os
import sys

# Add project root to sys.path to enable importing local packages like memory
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from mcp.server.fastmcp import FastMCP

# Import tools directly from the local folder
from search_tool import search_web
from memory_tool import save_memory, retrieve_memory
from calculator import calculator
from pdf_reader import read_pdf
from compare_tool import compare_options

# Initialize FastMCP Server
mcp = FastMCP("SecondBrainTools")

# Register tools using decorators
@mcp.tool(name="search_web")
def tool_search_web(query: str) -> str:
    """Searches the web for the given query and returns a summary of top results."""
    return search_web(query)

@mcp.tool(name="save_memory")
def tool_save_memory(key: str, val: str) -> str:
    """Saves a key-value memory pair to the persistent memory bank."""
    return save_memory(key, val)

@mcp.tool(name="retrieve_memory")
def tool_retrieve_memory(key: str) -> str:
    """Retrieves a memory value from the persistent memory bank by key."""
    return retrieve_memory(key)

@mcp.tool(name="calculator")
def tool_calculator(expression: str) -> str:
    """Evaluates a basic mathematical expression (addition, subtraction, multiplication, division, parentheses)."""
    return calculator(expression)

@mcp.tool(name="read_pdf")
def tool_read_pdf(filepath: str) -> str:
    """Reads content from a PDF or text file."""
    return read_pdf(filepath)

@mcp.tool(name="compare_options")
def tool_compare_options(options_json: str) -> str:
    """Creates a comparison matrix from options data in JSON format."""
    return compare_options(options_json)

if __name__ == "__main__":
    mcp.run()
