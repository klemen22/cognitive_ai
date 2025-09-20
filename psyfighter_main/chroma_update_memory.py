# simple code for modifying collection from chroma database

from chroma_manager import collection, addLongTermMemory


def addMemory():
    allData = collection.get()
    ids = allData["ids"]
    index = f"'doc_{str(len(ids))}'"
    saveText = ""

    print(ids)
    print(f"current index: {index}")

    humanInput = input("Enter Human text (enter / to skip): ")
    aiInput = input("Enter AI text (enter / to skip): ")

    if "/" in humanInput and "/" in aiInput:
        print("Nothing was entered")
        return

    if not "/" in humanInput:
        saveText = f"Human: {humanInput}"
    else:
        saveText = f"Human: "

    if not "/" in aiInput:
        saveText = saveText + f"\nAI: {aiInput}"
    else:
        saveText = saveText + f"\nAI: "

    print(f"\nFinal text to save into database: \n\n{saveText}")
    addLongTermMemory(saveText)

    return


def updateMemory(textID, newText):
    collection.update(ids=textID, documents=newText)
    return


def getTextID(text):
    textID = collection.query(query_texts=[text], n_results=1)
    return textID["ids"][0][0]


def deleteMemory():
    # TODO: finish this function.
    return


if __name__ == "__main__":
    print("nothing to see here")
