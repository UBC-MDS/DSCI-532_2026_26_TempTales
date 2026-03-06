import os
import pandas as pd
from dotenv import load_dotenv
import chatlas as ctl
from querychat import QueryChat

from .utils import df_yearly

load_dotenv()

chat = ctl.ChatGithub(
    api_key=os.getenv("GITHUB_API_KEY"),
    model = "gpt-4.1-mini",
    #system_prompt = "You are a helpful weather assistant."
    system_prompt = "You are a helpful assistant."
)

qc = QueryChat(
    df_yearly,
    "temperature_data",
    client=chat
)


