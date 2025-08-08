from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    openai_api_base="http://192.168.64.114:1234/v1",
    openai_api_key="sk-...",  # dummy key
    model="cognitivecomputations_dolphin-mistral-24b-venice-edition",
)

response = llm.invoke([HumanMessage(content="What is an artificial intelligence?")])
print(response.content)
