from google.adk.agents.llm_agent import Agent

root_agent = Agent(
    model='gemini-3.5-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
)

from google.adk.agents.llm_agent import Agent
from google.adk.tools import google_search
from google.adk.apps import App

slack_root_agent = Agent(
    model='gemini-3.5-flash',
    
    name='slack_root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
    tools=[google_search]
)

app = App(
    root_agent=slack_root_agent,
    name="slack_root_agent",
)
