from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
import os
import asyncio

# See AgentConfig model for full list of parameters to configure the agent
from pyneuphonic import Neuphonic, Agent, AgentConfig  # noqa: F401
from pyneuphonic.models import APIResponse, AgentResponse


app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

def on_message(message: APIResponse[AgentResponse]):
        global speaker
        if(message.data.type == 'llm_response') or (message.data.type == 'audio_response'):
            print("HE")
            speaker = 0
            socketio.emit("update", {"talking": False})
        else:
            print("YA")
            speaker = 1
            socketio.emit("update", {"talking": True})


@app.route("/api/translate", methods=["POST"])
def translate():
    global speaker
    speaker = 0
    socketio.emit("update", {"talking": False})
    
    print("Select an option:")
    print("1 - Translate English spoken words to Spanish")
    print("2 - Translate English spoken words to German")

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
                on_message = on_message,
            )

        elif lang == 2:
            agent_id = client.agents.create(
                name='Klaus',
                prompt='You are a translator. We will speak to you in English and repeat back a German sentence of the same meaning. You must not say a single word that is not a direct translation of something we have said to you.',
                greeting='',
            ).data['agent_id']

            agent = Agent(
                client,
                agent_id=agent_id,
                lang_code='de',
                voice_id='052c4c9e-c8c3-42f8-966e-e041979fd056',
                on_message = on_message,
            )

        try:
            await agent.start()

            while True:
                await asyncio.sleep(0.3)
                print("Speaker = " + str(speaker))

        except KeyboardInterrupt:
            await agent.stop()


    asyncio.run(main())

app.run(debug=True)
