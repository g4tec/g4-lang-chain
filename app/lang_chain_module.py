from flask import Blueprint,request,jsonify
from dotenv import load_dotenv
from modules.weaviate import weaviate
from modules.lang_chain_chatbot import lang_chain_chatbot
from flasgger import swag_from
from werkzeug.utils import secure_filename

load_dotenv()

lang_chain_bp = Blueprint('main_v2', __name__)


@lang_chain_bp.route('/prediction', methods=['POST'])
@swag_from('api_docs/prediction.yml')
def prediction():
    data = request.get_json()
    question = data['question']
    overrideConfig = data['overrideConfig']
    weaviateIndex = overrideConfig['weaviateIndex']
    docs = weaviate.get_docs(question, weaviateIndex)

    chain = lang_chain_chatbot.run_bot_open_ai(docs, question)
    return jsonify({"text": chain}), 200




@lang_chain_bp.route('/insert_file', methods=['POST'])
@swag_from('api_docs/insert_file.yml')
def insert_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file:
        try:
            vectorstore = weaviate.add_docs(file)        
            return jsonify({"answer": "Documents successfully added to Weaviate"}), 200
        except Exception as e:
            return jsonify({"error": f"Error processing file: {str(e)}"}), 400
    