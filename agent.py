import os
from google.adk.agents import Agent
from google.adk.tools import google_search # Optional: For general web searching
from google.genai import types

# Define custom tools for the agent

def read_local_file(path: str) -> str:
    """Reads a local file from the computer's file system."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

def fetch_url_content(url: str) -> str:
    """Fetches text content from any provided link/URL."""
    # In 2025, the GenAI SDK's 'URL Context' feature or a standard request library can be used
    import requests
    try:
        response = requests.get(url, timeout=10)
        return response.text[:5000]  # Limit to 5000 chars for prompt space
    except Exception as e:
        return f"Error fetching URL: {str(e)}"

# Initialize the ADK Agent

# In late 2025, 'gemini-2.5-flash' is a common target model for agents
multi_input_agent = Agent(
    name="Unified_File_Agent",
    model="gemini-2.5-flash", 
    instruction=(
        "You are an assistant that can process local files, web links, and "
        "direct user instructions. Use the 'read_local_file' tool if a path "
        "is provided, and 'fetch_url_content' if a URL link is provided. "
        "Summarize or answer questions based on the content found."
    ),
    tools=[read_local_file, fetch_url_content, google_search]
)

# Execution Logic

def run_agent_interaction(customer_prompt: str):
    print(f"Customer: {customer_prompt}")
    
    # The ADK automatically determines if it needs to call tools
    response = multi_input_agent.run(customer_prompt)
    print(f"Agent: {response.text}")

# Example Scenarios

# 1. Local File Request
# run_agent_interaction("Read C:/Users/Docs/blood_report.txt and summarize it.")

# 2. URL Link Request
# run_agent_interaction("Check this link https://example.com/data and tell me the main point.")

# 3. Direct Prompt
# run_agent_interaction("Just write a poem about artificial intelligence.")
