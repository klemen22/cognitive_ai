import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from langchain_core.messages import HumanMessage
import json
from itertools import zip_longest
import uuid

chromaClient = chromadb.PersistentClient(path="./data/psyfighter_memory/chroma")
collection = chromaClient.get_or_create_collection(name="psyfighter_long_term_memory")

# ----------------------------------------------------------------------------------------------#
#                                         Add memory                                            #
# ----------------------------------------------------------------------------------------------#

# embedding
embedding = SentenceTransformer("all-MiniLM-L6-v2")


def embedText(text: str):
    return embedding.encode(text).tolist()


# filter information for long term memory
def textJudge(llm, text: str, threshold=0.75):
    # search for similiar documents
    documents = collection.query(query_texts=[text], n_results=1)
    if documents["documents"][0]:
        similarity = 1 - documents["distances"][0][0]
        if similarity > threshold:
            print("Skipping similar info...")
            return

    # ask AI to determin if the text should be saved
    if shouldRemember(llm, text) == "yes":
        addLongTermMemory(text)
        print("Text added to long term memory")
    else:
        print("Text was not added to long term memory")
        return


def shouldRemember(llm, text: str):
    prompt = f"""You are a strict judge that must decide if this conversation text should be remembered in long-term memory.
                 Answer strictly with ONLY one word: "Yes" or "No". Do not add anything else.

                 Conversation text:
                 {text}
             """
    response = llm.invoke([HumanMessage(content=prompt)])
    print("LLM Judge response:", response.content.strip().lower().replace(".", ""))
    return response.content.strip().lower().replace(".", "")


def addLongTermMemory(text: str):

    if hasattr(text, "content"):
        SaveText = text.content
    else:
        SaveText = str(text)

    embeddedText = embedText(SaveText)
    documentID = f"doc_{uuid.uuid4().hex[:8]}"
    collection.add(ids=[documentID], documents=[text], embeddings=[embeddedText])
    return


# ----------------------------------------------------------------------------------------------#
#                                         Get memory                                            #
# ----------------------------------------------------------------------------------------------#


def getReleventMemories(query: str, n=3):
    results = collection.query(query_texts=[query], n_results=n)

    if results["documents"]:
        return [doc for doc in results["documents"][0]]
    else:
        return []


def retrieveMemory():
    allData = collection.get()
    finalData = []

    for y in allData["documents"]:
        finalData.append(y)

    return finalData


# ----------------------------------------------------------------------------------------------#
#                                        Update dump                                            #
# ----------------------------------------------------------------------------------------------#


def updateMemory(textID, newText):
    collection.update(ids=textID, documents=newText)
    return


def getTextID(text):
    textID = collection.query(query_texts=[text], n_results=1)
    return textID["ids"][0][0]


def deleteMemory(textID):
    collection.delete(ids=[textID])
    return


# ----------------------------------------------------------------------------------------------#
#                                        Memory dump                                            #
# ----------------------------------------------------------------------------------------------#

output = "./data/psyfighter_memory/chroma_dump/chroma_memory_dump.json"


def memoryDump():
    allData = collection.get()
    filteredData = []

    for x, y in zip_longest(allData["ids"], allData["documents"]):
        print(f"\n{x}, {y}")
        filteredData.append(y)

    with open(output, "w", encoding="utf-8") as w:
        json.dump(filteredData, w, ensure_ascii=False, indent=2)

    print(f"\nMemory dump was saved to: {output}")

    return filteredData
