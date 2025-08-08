import json
import os
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import HumanMessage, AIMessage

memory_path = "data/memory.json"


# helper function for loading memory
def loadMemory():
    memory = ConversationBufferMemory(
        return_messages=True,
        ai_prefix="AI",
        human_prefix="Human",
        input_key="input",
        output_key="response",
    )

    if os.path.exists(memory_path) and os.path.getsize(memory_path) > 0:
        with open(memory_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for m in data:
            if m["type"] == "human":
                memory.chat_memory.add_user_message(m["content"])
            elif m["type"] == "ai":
                memory.chat_memory.add_ai_message(m["content"])

    return memory


# helper function for saving memory
def saveMemory(memory):
    save_memory = []

    for x in memory.chat_memory.messages:
        if isinstance(x, HumanMessage):
            save_memory.append({"type": "human", "content": x.content})
        elif isinstance(x, AIMessage):
            save_memory.append({"type": "ai", "content": x.content})

    with open(memory_path, "w", encoding="utf-8") as f:
        json.dump(save_memory, f, ensure_ascii=False, indent=2)


# initialize LLM
llm = ChatOpenAI(
    openai_api_base="http://192.168.64.114:1234/v1",
    openai_api_key="sk-...",  # dummy key
    model="cognitivecomputations_dolphin-mistral-24b-venice-edition",
)

# load memory
memory = loadMemory()

# create agent
conversation = ConversationChain(llm=llm, memory=memory, verbose=False)

# main loop
print("Started converstion with an AI (write 'exit' to end the conversation)")

while True:
    userInput = input("Human: ")

    if userInput.lower() in ["exit", "quit"]:
        saveMemory(memory)
        print("Conversation was saved. Ending conversation.")
        break

    response = conversation.predict(input=userInput)
    print(f"AI: {response}")
