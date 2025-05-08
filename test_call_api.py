# --- Imports ---
import os
from dotenv import load_dotenv
# -------------
import datasets
import aiohttp
import openai
import instructor
import pydantic
import json, hashlib, inspect
from typing import Any
from pydantic import BaseModel, ValidationError, Field
import diskcache
import time
import datasets
import enum
from itertools import zip_longest
import numpy as np
from dataclasses import dataclass
from typing import Literal
from openai import AsyncAzureOpenAI

# Load environment variables from .env file
load_dotenv()

# Access the variables
api_key = os.getenv("API_KEY")
endpoint = os.getenv("ENDPOINT")
model = os.getenv("MODEL")
deployment = os.getenv("DEPLOYMENT")

# You can now use these variables in your code
print(f"API Key: {api_key}")
print(f"Endpoint: {endpoint}")
print(f"Model: {model}")
print(f"Deployment: {deployment}")

azure_client = AsyncAzureOpenAI(
    api_version="2024-12-01-preview",
    azure_endpoint=endpoint,
    api_key=api_key
)
async def  main():
    response = await azure_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Quien fue el primer premio Nobel argentino?",
            }
        ],
        # When using Azure, you should use the DEPLOYMENT rather than the MODEL
        model=deployment
    )

    print(response.choices[0].message.content)
import asyncio
asyncio.run(main()) 