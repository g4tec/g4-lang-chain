from lang_chain_module import lang_chain_bp
import os
from flask import Flask
from flasgger import Swagger
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
swagger = Swagger(app, template_file=f'api_docs/swagger.yml')

server_port = os.environ.get('SERVER_PORT')

app.register_blueprint(lang_chain_bp, url_prefix='/lang_chain')

if __name__ == "__main__":
    app.run(debug=True, port=server_port)
