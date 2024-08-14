import weaviate
from langchain.vectorstores import Weaviate
import os
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
import pdfplumber
import json


load_dotenv()


WEAVIATE_KEY =  os.environ.get('WEAVIATE_KEY')
WEAVIATE_URL =  os.environ.get('WEAVIATE_URL')
OPENAI_KEY =  os.environ.get('OPENAI_KEY')


def add_docs(file, weaviateHost, weaviateIndex, metadata):

    with pdfplumber.open(file) as pdf:
        text_content = ""
        for page in pdf.pages:
            text_content += page.extract_text() or ""
    
    metadata_dict = json.loads(metadata)
    documents = [Document(page_content=text_content, metadata=metadata_dict)]

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)

    class_name = weaviateIndex

    client = weaviate.Client(
        url=f'http://{weaviateHost}',
        additional_headers={"X-OpenAI-Api-Key": OPENAI_KEY},
        startup_period=10
    )


    schema = {
        "classes": [
            {
                "class": class_name,
                "description": "Documents for chatbot",
                "vectorizer": "text2vec-transformers",
                 "moduleConfig": {
                    "text2vec-openai": {
                        "model": "ada",
                        "type": "text"
                    }
                },
                "properties": [
                    {
                        "name": "content",
                        "dataType": ["text"],
                        "description": "The content of the document"
                    },
                    {
                        "name": "filename",
                        "dataType": ["text"],
                        "description": "The name of the file from which the document was extracted"
                    },
                    {
                        "name": "source",
                        "dataType": ["text"],
                        "description": "The source of the document"
                    },
                    {
                        "name": "uuid",
                        "dataType": ["text"],
                        "description": "The uuid of the document"
                    }
                ]
            },
        ]
    }
    if not client.schema.exists(class_name):
        client.schema.create(schema)

    vectorstore = Weaviate(client, class_name, "content", attributes=["filename", "source", "uuid"])
    
    vectorstore.add_documents(documents)

    return vectorstore

def get_docs(query, weaviateIndex, weaviateHost):

    client = weaviate.Client(
        url=weaviateHost,
        startup_period=10
    )
    
    vectorstore = Weaviate(client, weaviateIndex, "content", attributes=["filename", "source", "uuid"])


    docs = vectorstore.similarity_search(query, k=4)
    return docs 

