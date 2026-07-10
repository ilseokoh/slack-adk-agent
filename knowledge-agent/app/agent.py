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

from google.adk.agents import LlmAgent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types

from google.adk.tools import VertexAiSearchTool

from .prompts import return_instructions_root

load_dotenv()

# Initialize tools list
tools = []

datastore = os.environ.get("DATASTORE_PATH")

if datastore:
    vertex_search_tool = VertexAiSearchTool(data_store_id=datastore)
    tools.append(vertex_search_tool)

root_agent = LlmAgent(
    name="root_agent",
    model=Gemini(
        model="gemini-flash-latest",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=return_instructions_root(),
    tools=tools,
)

app = App(
    root_agent=root_agent,
    name="app",
)
