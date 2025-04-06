import os
import asyncio

# See AgentConfig model for full list of parameters to configure the agent
from pyneuphonic import Neuphonic, Agent, AgentConfig  # noqa: F401
from pyneuphonic.models import APIResponse, AgentResponse


def on_message(message: APIResponse[AgentResponse]):
    word = message.data.text
    if(message.data.type == 'llm_response'):
        words = word.split()
        if words[0][0] == 'C':
            print("Correct!")
        else:
            print("Incorrect")
        print("Agent: " + words[-1].strip(""))
    elif (message.data.type == 'user_transcript'):
        print("User: " + word)


async def main():
    client = Neuphonic(api_key="50d15a31056af1cf8e4a4ecf050896dbe60b5ad43147e6ddebf9ef6c7219b3b4.da8db507-e24d-4a7a-82cc-35414f5a5c50")

    agent_id = client.agents.create(
        name='Agent 1',
        prompt='Only speak by saying randomly generated Spanish words, getting gradually harder. If the user gets the answer correct, then say Correct, followed by the next word. The first word you say in the greeting should be part of this.',
        greeting='Hola',
    ).data['agent_id']

    # All additional keyword arguments (such as `agent_id`) are passed as
    # parameters to the model. See AgentConfig model for full list of parameters.
    agent = Agent(
        client,
        agent_id=agent_id,
        lang_code='es',
        voice_id='3c8d7261-b917-4085-90ad-e7de015b3030',
        on_message = on_message,
    )


    try:
        await agent.start()

        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        await agent.stop()


asyncio.run(main())