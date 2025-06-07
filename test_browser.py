import asyncio
from dotenv import load_dotenv
load_dotenv()
from browser_use import Agent
from langchain_openai import AzureChatOpenAI

async def main():
    agent = Agent(
        task="Busca el vuelo mas barato a santorini saliendo entre el 1 y 4 de agosto",
        llm =AzureChatOpenAI(
            azure_deployment="gpt-4o-mini-alex-udesa",
            api_version="2023-05-15",
            temperature=0.05    ,
            model_name="gpt-4o-mini",
            azure_endpoint="https://abodn-maeidvlk-eastus2.cognitiveservices.azure.com/",
            api_key = "BwuJbV7aiCeu4F6XIVDmPOHyomhEPxVl1LKzqj5KQqQhzwmMOX6MJQQJ99BEACHYHv6XJ3w3AAAAACOGk2VZ"
            )
    )
    await agent.run()

asyncio.run(main())