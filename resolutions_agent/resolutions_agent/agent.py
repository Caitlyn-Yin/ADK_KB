"""Agent to test out RAG engine to retrieve instructions from files."""

import os

from google.adk.agents import Agent
from tools.tools import get_intent_resolution_instructions

from utils import read_instructions_from_file

description = """Agent to retrieve instructions to handle user requests.
Handles user intent classification and retrieves relevant step-by-step
instructions to solve users problem based on the user's classified intent."""

resolutions_agent = Agent(
    name='retrieve_instructions_agent',
    model=os.environ.get('GOOGLE_CLOUD_LLM_NAME', ''),
    description=description,
    instruction=read_instructions_from_file(
        './resolutions_agent/instructions.md'
    ),
    tools=[get_intent_resolution_instructions],
)
