import weaviate
from langchain.vectorstores import Weaviate
import os
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
import pdfplumber


load_dotenv()


WEAVIATE_KEY =  os.environ.get('WEAVIATE_KEY')
WEAVIATE_URL =  os.environ.get('WEAVIATE_URL')
OPENAI_KEY =  os.environ.get('OPENAI_KEY')


def add_docs(file):

    with pdfplumber.open(file) as pdf:
        text_content = ""
        for page in pdf.pages:
            text_content += page.extract_text() or ""
    
    filename = file.filename
    documents = [Document(page_content=text_content, metadata={"filename": filename})]

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)

    class_name = "ABDBBCBFFZZ"
    # connect Weaviate Cluster
    auth_config = weaviate.AuthApiKey(api_key=WEAVIATE_KEY)

    client = weaviate.Client(
        url=WEAVIATE_URL,
        additional_headers={"X-OpenAI-Api-Key": OPENAI_KEY},
        # auth_client_secret=auth_config,
        startup_period=10
    )
    # define input structure
    client.schema.delete_all()

    schema = {
        "classes": [
            {
                "class": class_name,
                "description": "Documents for chatbot",
                "vectorizer": "text2vec-transformers",
                # "moduleConfig": {"text2vec-openai": {"model": "ada", "type": "text"}},
                # "properties": [
                #     {
                #         "dataType": ["text"],
                #         "description": "The content of the paragraph",
                #         "moduleConfig": {
                #             "text2vec-openai": {
                #                 "skip": False,
                #                 "vectorizePropertyName": False,
                #             }
                #         },
                #         "name": "text",
                #     },
                # ],
            },
        ]
    }
    if not client.schema.exists(class_name):
        client.schema.create(schema)


    vectorstore = Weaviate(client, class_name, "text")

    text_meta_pair = [(doc.page_content, doc.metadata) for doc in docs]
    texts, meta = list(zip(*text_meta_pair))
    vectorstore.add_texts(texts, meta)
    return vectorstore

def get_docs(query, weaviateIndex):

    auth_config = weaviate.AuthApiKey(api_key=WEAVIATE_KEY)

    client = weaviate.Client(
        url=WEAVIATE_URL,
        startup_period=10
    )
    
    vectorstore = Weaviate(client, weaviateIndex, "text")

    docs = vectorstore.similarity_search(query, k=4)
    return docs 

