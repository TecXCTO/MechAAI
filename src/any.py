import os
from google.adk.agents import Agent
from google.adk.artifacts import GcsArtifactService
from google.adk.tools import google_search

# 1. Initialize GCS Artifact Service for "Any Size" files (up to 5TB)
# This prevents large files from bloating the agent's session memory.
artifact_service = GcsArtifactService(bucket_name="your-agent-artifacts-bucket")

# 2. Tools for Large File Import/Export
def import_large_file(source_path: str, destination_name: str) -> str:
    """Uploads a file of any size from a local path to the agent's cloud storage."""
    try:
        artifact_service.save_artifact(source_path, destination_name)
        return f"Successfully imported {destination_name} to cloud storage."
    except Exception as e:
        return f"Import failed: {str(e)}"

def export_large_file(artifact_name: str, local_destination: str) -> str:
    """Downloads a file from the agent's cloud memory to a local path."""
    try:
        artifact_service.load_artifact(artifact_name, local_destination)
        return f"Successfully exported {artifact_name} to {local_destination}."
    except Exception as e:
        return f"Export failed: {str(e)}"

# 3. Create the Agent with Gemini 2.5 (Multimodal for Audio/Text)
file_master_agent = Agent(
    name="Universal_File_Agent",
    model="gemini-2.5-flash", # Native support for audio/text input in 2025
    instruction=(
        "You are a file management expert. Users will provide commands via text or audio. "
        "Use 'import_large_file' for local uploads and 'export_large_file' for downloads. "
        "For audio commands, transcribe the intent first, then execute the tool."
    ),
    tools=[import_large_file, export_large_file, google_search],
    artifact_service=artifact_service
)

# 4. Running with Text or Audio (Simplified Interface)
def handle_command(input_data, is_audio=False):
    if is_audio:
        # In 2025, ADK handles audio streams directly as part of the prompt
        # The model processes the audio and determines the action automatically.
        response = file_master_agent.run(audio=input_data)
    else:
        response = file_master_agent.run(prompt=input_data)
    
    print(f"Agent Response: {response.text}")

# Example: handle_command("Export the blood_report.csv to my desktop.")
