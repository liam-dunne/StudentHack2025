import os
import asyncio

# See AgentConfig model for full list of parameters to configure the agent
from pyneuphonic import Neuphonic, Agent, AgentConfig  # noqa: F401
from pyneuphonic.models import APIResponse, AgentResponse


print("Select an option:")
print("1 - Translate English spoken words to Spanish")
print("2 - Translate English spoken words to German")
print("3 - Translate English spoken words to Spanish")

lang = int(input(""))

async def main():
    client = Neuphonic(api_key="50d15a31056af1cf8e4a4ecf050896dbe60b5ad43147e6ddebf9ef6c7219b3b4.da8db507-e24d-4a7a-82cc-35414f5a5c50")

    if lang == 1:
        agent_id = client.agents.create(
            name='Alejandra',
            prompt='You are a translator. We will speak to you in English and repeat back a Spanish sentence of the same meaning. You must not say a single word that is not a direct translation of something we have said to you.',
            greeting='Hola',
        ).data['agent_id']

        agent = Agent(
            client,
            agent_id=agent_id,
            lang_code='es',
            voice_id='3c8d7261-b917-4085-90ad-e7de015b3030',
        )

    elif opt == 2:
        agent_id = client.agents.create(
            name='Klaus',
            prompt='You are a translator. We will speak to you in English and repeat back a German sentence of the same meaning. You must not say a single word that is not a direct translation of something we have said to you.',
            greeting='',
        ).data['agent_id']

        opt = Agent(
            client,
            agent_id=agent_id,
            lang_code='de',
            voice_id='052c4c9e-c8c3-42f8-966e-e041979fd056',
        )

        

    try:
        await agent.start()

        while True:
            await asyncio.sleep(1)

    except KeyboardInterrupt:
        await agent.stop()


asyncio.run(main())