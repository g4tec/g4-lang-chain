from langchain.chains.question_answering import load_qa_chain
from langchain_community.llms import OpenAI
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv
from langchain.memory import RedisChatMessageHistory
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

import os
load_dotenv()


ANTHROPIC_API_KEY =  os.environ.get('ANTHROPIC_API_KEY')
OPENAI_KEY =  os.environ.get('OPENAI_KEY')
REDIS_HOST =  os.environ.get('REDIS_HOST')
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



def stream_bot_antropic(docs, query, session_id):
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You're an assistant"),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{question}\n\nDocuments:\n{documents}"),
        ]
    )

    llm = ChatAnthropic(
        model="claude-3-5-sonnet-20240620",
        temperature=0.9,
        max_tokens=2048,
        timeout=None,
        max_retries=2,
        api_key=ANTHROPIC_API_KEY        
    )
    chain = prompt | llm
    chain_with_history = RunnableWithMessageHistory(
        chain,
        lambda session_id: RedisChatMessageHistory(
            session_id, url=f'redis://{REDIS_HOST}'
        ),
        input_messages_key="question",
        history_messages_key="history",
    )

    documents_str = "\n".join([doc.page_content for doc in docs])

    input_data = {
        "question": query,
        "documents": documents_str
    }

    try:
        for token in chain_with_history.stream(input_data, {"configurable": {"session_id": session_id}}):
            yield f"{token.content}"
    except Exception as e:
        yield f"I couldn't answer your question 😞, can you try again?\nOr maybe you need a new account limit 🤗"



def summarize_documents(docs):
    return "\n".join([f"Summary of Document {i+1}: {doc.page_content[200]}" for i, doc in enumerate(docs)])