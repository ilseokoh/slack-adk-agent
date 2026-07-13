import asyncio
import os 
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.integrations.slack import SlackRunner
from slack_bolt.app.async_app import AsyncApp
from google.adk.sessions import InMemorySessionService
from fastapi import FastAPI

from slack_root import app as adk_app

load_dotenv()

print("SLACK_APP_TOKEN", os.getenv("SLACK_APP_TOKEN"))
print("SLACK_BOT_TOKEN", os.getenv("SLACK_BOT_TOKEN"))

async def main():
    runner = Runner(app=adk_app, session_service=InMemorySessionService(), app_name="slack_root_agent",auto_create_session=True)
    slack_app = AsyncApp(token=os.environ["SLACK_BOT_TOKEN"])
    slack_runner = SlackRunner(slack_app=slack_app, runner=runner)
    await slack_runner.start(app_token=os.environ["SLACK_APP_TOKEN"])

if __name__ == "__main__":
    asyncio.run(main())
