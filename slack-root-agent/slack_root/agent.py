import os

from google.adk.agents.llm_agent import Agent
from google.adk.agents.remote_a2a_agent import AGENT_CARD_WELL_KNOWN_PATH
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent

from dotenv import load_dotenv

from google.adk.agents.llm_agent import Agent
from google.adk.tools import google_search
from google.adk.apps import App

from .prompts import return_instructions_root

A2A_CARD_URL = f"/api/a2a/app{AGENT_CARD_WELL_KNOWN_PATH}"

load_dotenv()

caa_agent = RemoteA2aAgent(
    name="caa_agent",
    description="Agent that handles checking if numbers are prime.",
    agent_card=(
        f"{os.getenv('CAA_AGENT_URL')}{A2A_CARD_URL}"
    ),
    use_legacy=False,
)

knowledge_agent = RemoteA2aAgent(
    name="knowledge_agent",
    description="Agent that handles knowledge-based queries.",
    agent_card=(
        f"{os.getenv('KNOWLEDGE_AGENT_URL')}{A2A_CARD_URL}"
    ),
    use_legacy=False,
)

t2s_agent = RemoteA2aAgent(
    name="t2s_agent",
    description="Agent that handles text-to-speech conversion.",
    agent_card=(
        f"{os.getenv('T2s_AGENT_URL')}{A2A_CARD_URL}"
    ),
    use_legacy=False,
)


# TODO: check the convertor, interceptor: https://adk.dev/a2a/quickstart-consuming/#converters

slack_root_agent = Agent(
    model='gemini-3.5-flash',
    name='slack_root_agent',
    description='A helpful assistant for user questions.',
    instruction=return_instructions_root(),
    global_instruction="You are a helpful assistant for user questions.",
    # config=A2aRemoteAgentConfig(
    #     a2a_message_converter=my_a2a_message_converter,
    #     request_interceptors=[my_request_interceptor],
    # ),
    sub_agents=[caa_agent, knowledge_agent, t2s_agent],
)

app = App(
    root_agent=slack_root_agent,
    name="slack_root_agent",
)
