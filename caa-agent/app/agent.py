# ruff: noqa
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import datetime
from zoneinfo import ZoneInfo

from dotenv import load_dotenv

from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types

from google.adk.tools.data_agent.data_agent_toolset import DataAgentToolset
from google.adk.tools.data_agent.config import DataAgentToolConfig
from google.adk.tools.data_agent.credentials import DataAgentCredentialsConfig

import google.auth

load_dotenv()

# _, project_id = google.auth.default()
# os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
# os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
# os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"

print("GOOGLE_CLOUD_PROJECT:", os.environ.get("GOOGLE_CLOUD_PROJECT"))
print("GOOGLE_CLOUD_LOCATION:", os.environ.get("GOOGLE_CLOUD_LOCATION"))
print("GOOGLE_GENAI_USE_VERTEXAI:", os.environ.get("GOOGLE_GENAI_USE_VERTEXAI"))

# Use Application Default Credentials (ADC)
# https://cloud.google.com/docs/authentication/provide-credentials-adc
application_default_credentials, _ = google.auth.default()
credentials_config = DataAgentCredentialsConfig(
    credentials=application_default_credentials
)

# Define tool configuration
tool_config = DataAgentToolConfig(
    max_query_result_rows=100,
)

# Instantiate a Data Agent toolset
da_toolset = DataAgentToolset(
    credentials_config=credentials_config,
    data_agent_tool_config=tool_config,
    tool_filter=[
        "list_accessible_data_agents",
        "get_data_agent_info",
        "ask_data_agent",
    ],
)
root_agent = Agent(
    name="caa_agent",
    model=Gemini(
        model="gemini-flash-latest",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    description="Agent to answer user questions using Data Agents.",
    instruction=f"You are a helpful assistant that answers user questions using Data Agents. \n * Project ID: {os.environ.get('GOOGLE_CLOUD_PROJECT')} \n * Location: {os.environ.get('GOOGLE_CLOUD_LOCATION')} \n * Data Agent ID: {os.environ.get('DATA_AGENT_ID')}",
    tools=[da_toolset],
)

app = App(
    root_agent=root_agent,
    name="app",
)
