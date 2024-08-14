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
        api_key=ANTHROPIC_API_KEY
    )
    chain = load_qa_chain(llm, chain_type="stuff")

    answer = chain.run(input_documents=docs, question=query)
    
    return answer


def stream_bot_antropic(docs, query):
    llm = ChatAnthropic(
        model="claude-3-5-sonnet-20240620",
        temperature=0.9,
        max_tokens=1024,
        timeout=None,
        max_retries=2,
        api_key=ANTHROPIC_API_KEY
    )
    chain = load_qa_chain(llm, chain_type="stuff")

    for token in chain.run(input_documents=docs, question=query, return_generator=True):
        yield f"{token}"