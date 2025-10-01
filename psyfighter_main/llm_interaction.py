from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from memory_manager import loadMemory, saveMemory
from chroma_manager import getReleventMemories, textJudge


# ----------------------------------------------------------------------------------------------#
#                                     LLM initialization                                        #
# ----------------------------------------------------------------------------------------------#

llm = ChatOpenAI(
    openai_api_base="http://localhost:1234/v1",
    openai_api_key="something something...",  # dummy key
    model="llama2-13b-psyfighter2",
)

# load memory
memory = loadMemory()

# create chain
conversation = ConversationChain(llm=llm, memory=memory, verbose=False)

# ----------------------------------------------------------------------------------------------#
#                                           Main                                                #
# ----------------------------------------------------------------------------------------------#
"""
while True:
    userInput = input("Human: ")

    if userInput.lower() in ["exit", "quit"]:
        saveMemory(memory)
        print("Conversation was saved. Ending...")
        break

    # get relevent memory for given user input
    relevantMemory = getReleventMemories(userInput, n=3)

    fullContext = userInput
    if relevantMemory:
        fullContext = fullContext + f"\n\nRelevant memories:\n\n {relevantMemory}"

    response = conversation.predict(input=fullContext)
    print(f"AI: {response}\n")
    textJudge(llm, text=f"Human: {userInput}\nAI: {response}")
"""


def proccessInput(userInput: str):
    fullContext = userInput

    relevantMemory = getReleventMemories(userInput, n=3)

    if relevantMemory:
        fullContext = fullContext + f"\n\nRelevant memories:\n\n{relevantMemory}"

    response = conversation.predict(input=fullContext)
    textJudge(llm, text=f"Human: {userInput}\nAI: {response}")

    return response


def endConversation():
    saveMemory(memory)
