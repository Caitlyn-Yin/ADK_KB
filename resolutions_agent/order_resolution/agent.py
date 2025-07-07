"""Order resolution agent for The Home Depot customer service."""

import os

from google.adk.agents import Agent
from tools.tools import cancel_order, check_order_status, initiate_return

from utils import read_instructions_from_file

description = """A customer service agent for The Home Depot, focused on order
cancellations and returns."""


order_resolver = Agent(
    name='customer_service_agent',
    model=os.environ.get('GOOGLE_CLOUD_LLM_NAME', ''),
    description=description,
    instruction=read_instructions_from_file(
        './order_resolution/instructions.md'
    ),
    tools=[check_order_status, cancel_order, initiate_return],
)
