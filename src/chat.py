import os
import pandas as pd
import numpy as np
from dotenv import load_dotenv
import chatlas as ctl
from querychat import QueryChat

from .utils import df_monthly

load_dotenv()

chat = ctl.ChatGithub(
    api_key=os.getenv("GITHUB_API_KEY"),
    model = "gpt-4.1-mini",
    #system_prompt = "You are a helpful weather assistant."
    # system_prompt = "You are a helpful assistant."
    system_prompt = """
        You are a climate data assistant for the TempTales dashboard.

        You help users explore historical temperature data across countries.
        This is the dataset provided for you: 
        * temperature_data:
            Monthly average temperature per country.    

        When possible:
        - Answer questions using the dataset
        - Suggest useful data queries
        - Help interpret climate trends
        - Be concise and clear
    """
)

# qc = QueryChat(
#     df_yearly,
#     "temperature_data",
#     client=chat
# )
df_monthly["AvgTemp"] = np.round(df_monthly["AvgTemp"], 2)

qc = QueryChat(
    df_monthly, 
    "temperature_data", 
    client=chat
)

