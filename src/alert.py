import os
import requests
from google.adk.agents import Agent, WorkflowAgent
from google.adk.tools import google_search

# --- EXISTING TOOLS ---
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

# --- NEW CONDITIONAL & NOTIFICATION TOOLS ---
def send_alert_notification(message: str) -> str:
    """Sends a high-priority alert if specific conditions are met."""
    # Logic to send email/Slack/SMS would go here
    return f"ALERT NOTIFICATION SENT: {message}"

def export_content_to_file(content_source: str, file_name: str) -> str:
    """Exports content to a local file from history or links."""
    with open(file_name, 'w') as f:
        f.write(content_source)
    return f"Exported to {file_name}"

# --- INITIALIZE CONDITIONAL AGENT ---

# In 2025, WorkflowAgent allows for sophisticated branching logic
conditional_agent = WorkflowAgent(
    name="Conditional_File_Manager",
    model="gemini-2.5-flash",
    instruction="""
    You are a smart data manager. 
    1. READ the source (file or link).
    2. IF the content contains 'CRITICAL' or 'ERROR', THEN use 'send_alert_notification' first.
    3. ALWAYS export the final result if requested.
    """,
    tools=[read_local_file, fetch_url_content, send_alert_notification, export_content_to_file]
)

# Example Scenario:
# Prompt: "Read https://example.com/log and if it has errors, alert me and save to 'log.txt'"
