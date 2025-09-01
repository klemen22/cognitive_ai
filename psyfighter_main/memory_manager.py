import json
import os
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import HumanMessage, AIMessage

memory_path = "./data/psyfighter_memory/psyfighter_short_memory.json"
maxMsg = 50  # max number of messages to prevent reaching token limit


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

            for x in data:
                if x["type"] == "human":
                    memory.chat_memory.add_user_message(x["content"])

                elif x["type"] == "ai":
                    memory.chat_memory.add_ai_message(x["content"])

    return memory


def saveMemory(memory):
    messages = memory.chat_memory.messages

    if len(messages) > maxMsg:
        messages = messages[-maxMsg:]  # keep only last message
        memory.chat_memory.message = messages

    saveData = []

    for x in memory.chat_memory.messages:
        if isinstance(x, HumanMessage):
            saveData.append({"type": "human", "content": x.content})
        elif isinstance(x, AIMessage):
            saveData.append({"type": "ai", "content": x.content})

    os.makedirs(os.path.dirname(memory_path), exist_ok=True)
    with open(memory_path, "w", encoding="utf-8") as f:
        json.dump(saveData, f, ensure_ascii=False, indent=2)
