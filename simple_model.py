import os
import asyncio

# See AgentConfig model for full list of parameters to configure the agent
from pyneuphonic import Neuphonic, Agent, AgentConfig  # noqa: F401


async def main():
    client = Neuphonic(api_key="50d15a31056af1cf8e4a4ecf050896dbe60b5ad43147e6ddebf9ef6c7219b3b4.da8db507-e24d-4a7a-82cc-35414f5a5c50")

    agent_id = client.agents.create(
        name='Agent 1',
        prompt='You are fluent in english and spanish, respond to my english in spanish',
        greeting='Hi, how can I help you today?',
    ).data['agent_id']

    # All additional keyword arguments (such as `agent_id`) are passed as
    # parameters to the model. See AgentConfig model for full list of parameters.
    agent = Agent(client, agent_id=agent_id)

    try:
        await agent.start()

        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        await agent.stop()


asyncio.run(main())