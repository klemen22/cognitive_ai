from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

# simple code for testing LLM memory stored in RAM

# initialize LLM
llm = ChatOpenAI(
    openai_api_base="http://localhost:1234/v1",
    openai_api_key="sk-...",  # dummy key
    model="cognitivecomputations_dolphin-mistral-24b-venice-edition",
)

# create RAM buffer
memory = ConversationBufferMemory(return_messages=True)

# connect LLM and memory
conversation = ConversationChain(llm=llm, memory=memory, verbose=True)

print(conversation.predict(input="Hello, my name is Steve."))
print(conversation.predict(input="What is my name?"))
print(conversation.predict(input="What did I ask you before?"))
