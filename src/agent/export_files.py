import os
import requests
from google.adk.agents import Agent
from google.adk.tools import google_search

# --- PREVIOUS TOOLS ---

def read_local_file(path: str) -> str:
    """Reads a local file from the computer's file system."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error: {str(e)}"

def fetch_url_content(url: str) -> str:
    """Fetches text content from a web link."""
    try:
        response = requests.get(url, timeout=10)
        return response.text[:5000]
    except Exception as e:
        return f"Error: {str(e)}"

# --- NEW EXPORT TOOL ---

def export_content_to_file(content_source: str, file_name: str, mode: str = "text") -> str:
    """
    Exports content to a local file. 
    'content_source' can be a URL to a file or raw text from conversation history.
    'mode' can be 'text' or 'binary' (for images/PDFs from links).
    """
    try:
        # Check if source is a URL to download
        if content_source.startswith("http"):
            response = requests.get(content_source, stream=True)
            write_mode = 'wb' if mode == "binary" else 'w'
            content = response.content if mode == "binary" else response.text
        else:
            # Source is raw text/history
            write_mode = 'w'
            content = content_source

        with open(file_name, write_mode) as f:
            f.write(content)
        
        return f"Successfully exported to {os.path.abspath(file_name)}"
    except Exception as e:
        return f"Export failed: {str(e)}"

# --- INITIALIZE ENHANCED AGENT ---

multi_input_agent = Agent(
    name="Unified_File_Agent_v2",
    model="gemini-2.5-flash", 
    instruction=(
        "You are a file management assistant. You can read local files, fetch web content, "
        "and export data. If a user asks to 'save', 'download', or 'export' something "
        "you just read or a link they provided, use the 'export_content_to_file' tool. "
        "You can retrieve information from your session history to perform these exports."
    ),
    tools=[read_local_file, fetch_url_content, export_content_to_file, google_search]
)

# --- EXAMPLE USAGE ---

# Scenario: "Export the summary of the blood report I showed you earlier to 'summary.txt'"
# The agent will use its history to find the 'blood report' content and pass it to the tool.
