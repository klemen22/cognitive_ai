# simple code for modifying collection from chroma database

from chroma_manager import collection, addLongTermMemory


def updateMemory(textID, newText):
    collection.update(ids=textID, documents=newText)
    return


def getTextID(text):
    textID = collection.query(query_texts=[text], n_results=1)
    return textID["ids"][0][0]


def deleteMemory(textID):
    collection.delete(ids=[textID])
    return


if __name__ == "__main__":
    print("nothing to see here")
