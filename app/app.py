from lang_chain_module import lang_chain_bp
import os
from flask import Flask, jsonify, request
from flasgger import Swagger
from dotenv import load_dotenv
from flask_socketio import SocketIO
from flask_socketio import SocketIO, emit
from modules.weaviate import weaviate
from modules.lang_chain_chatbot import lang_chain_chatbot

load_dotenv()

app = Flask(__name__)
swagger = Swagger(app, template_file=f'api_docs/swagger.yml')
socketio = SocketIO(app, cors_allowed_origins="*")

server_port = os.environ.get('SERVER_PORT')


app.register_blueprint(lang_chain_bp, url_prefix='/lang_chain')


@socketio.on('connect')
def handle_connect():
    socket_id = request.sid
    print(f'Client connected with Socket ID: {socket_id}')
    emit('connected', {'socket_id': socket_id})

@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")

@socketio.on('prediction')
def handle_stream(data):
    question = data['question']
    overrideConfig = data['overrideConfig']
    weaviateIndex = overrideConfig['weaviateIndex']
    sessionId = overrideConfig['sessionId']
    weaviateHost = f"http://{overrideConfig['weaviateHost']}"
    
    docs = weaviate.get_docs(question, weaviateIndex, weaviateHost)

    full_response = ''

    for partial_response in lang_chain_chatbot.stream_bot_antropic(docs, question, sessionId):
        emit('token', partial_response)
        full_response += partial_response
    sourceDocuments = []
    for doc in docs:
        sourceDocuments.append({
                "pageContent": doc.page_content,
                "metadata": doc.metadata,
            })
    emit('full_response',  {"text": full_response,"sourceDocuments":sourceDocuments})

if __name__ == "__main__":
    app.run(debug=True, port=server_port)
