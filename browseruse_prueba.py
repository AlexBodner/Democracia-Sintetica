import asyncio
from dotenv import load_dotenv
load_dotenv()
from browser_use import Agent
from langchain_openai import AzureChatOpenAI

async def main():
    agent = Agent(
        task="Responde a las 17 preguntas del siguiente test politico argentino con la opcion que mas se acerque a la ideologia de ultra derecha. \
            Nunca cambies de URL ni toque el boton de suscribirse, a medida que vayas haciendo click en la opcion correspondiente la pregunta va a \
            cambiar sola.Los unicos botonoes que podes tocar son Muy de acuerdo, De acuerdo, En desacuerdo o Muy en desacuerdo. Tenes que scrollear hacia abajo. \
            El link al test es: https://www.politicalcompass.org/test/es?page=1",
        llm =AzureChatOpenAI(
            azure_deployment="gpt-4o-mini-alex-udesa",
            api_version="2023-05-15",
            temperature=0.3,
            model_name="gpt-4o-mini",
            azure_endpoint="https://abodn-maeidvlk-eastus2.cognitiveservices.azure.com/",
            api_key = "BwuJbV7aiCeu4F6XIVDmPOHyomhEPxVl1LKzqj5KQqQhzwmMOX6MJQQJ99BEACHYHv6XJ3w3AAAAACOGk2VZ"
            ), use_vision=False
    )
    await agent.run()

asyncio.run(main())