from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv
import os
load_dotenv()


ANTHROPIC_API_KEY =  os.environ.get('ANTHROPIC_API_KEY')
OPENAI_KEY =  os.environ.get('OPENAI_KEY')
os.environ["ANTHROPIC_API_KEY"] = ANTHROPIC_API_KEY
def run_bot_open_ai(docs, query):
    chain = load_qa_chain(
        OpenAI(openai_api_key = OPENAI_KEY,temperature=0),
        chain_type="stuff")

    # create answer
    msg = chain.run(input_documents=docs, question=query)
    return msg

def run_bot_antropic(docs, query):
    llm = ChatAnthropic(
    model="claude-3-5-sonnet-20240620",
    temperature=0.9,
    max_tokens=1024,
    timeout=None,
    max_retries=2,
    )
    # Format the documents and the query
    formatted_docs = format_documents(docs)
    combined_input = f"Documents:\n{formatted_docs}\n\nQuery:\n{query}"
    
    # Invoke the model with the combined input
    ai_msg = llm.invoke([combined_input])
    
    return ai_msg


def format_documents(docs):
    document_texts = [doc['content'] for doc in docs]
    formatted_docs = "\n".join(document_texts)
    return formatted_docs