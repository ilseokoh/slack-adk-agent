import os

from google.adk.agents.llm_agent import Agent
from google.adk.agents.remote_a2a_agent import AGENT_CARD_WELL_KNOWN_PATH
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent

from dotenv import load_dotenv

from google.adk.agents.llm_agent import Agent
from google.adk.tools import google_search
from google.adk.apps import App

from .prompts import return_instructions_root

import httpx
from google.auth import default
from google.auth.transport.requests import Request as AuthRequest

A2A_CARD_URL = f"/api/a2a/app{AGENT_CARD_WELL_KNOWN_PATH}"

load_dotenv()

class GoogleCloudAuth(httpx.Auth):
    """Auto-refreshing Google Cloud authentication for httpx.

    Refreshes the access token before each request if expired,
    so long-running agents never hit 401 errors.
    """

    def __init__(self):
        self.credentials, _ = default(
            scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )

    def auth_flow(self, request):
        # Refresh the token if it is expired or missing
        if not self.credentials.valid:
            self.credentials.refresh(AuthRequest())
            
        request.headers["Authorization"] = f"Bearer {self.credentials.token}"
        yield request

knowledge_agent = RemoteA2aAgent(
    name="knowledge_agent",
    description="Agent that handles knowledge-based queries.",
    agent_card=(
        f"{os.getenv('KNOWLEDGE_AGENT_URL')}{A2A_CARD_URL}"
    ),
    httpx_client=httpx.AsyncClient(auth=GoogleCloudAuth(), timeout=360),
)

# TODO: check the convertor, interceptor: https://adk.dev/a2a/quickstart-consuming/#converters

slack_root_agent = Agent(
    model='gemini-flash-latest',
    name='slack_root_agent',
    description='A helpful assistant for user questions.',
    instruction=return_instructions_root(),
    global_instruction="You are a helpful assistant for user questions.",
    # config=A2aRemoteAgentConfig(
    #     a2a_message_converter=my_a2a_message_converter,
    #     request_interceptors=[my_request_interceptor],
    # ),
    sub_agents=[knowledge_agent],
)

app = App(
    root_agent=slack_root_agent,
    name="slack_root_agent",
)
