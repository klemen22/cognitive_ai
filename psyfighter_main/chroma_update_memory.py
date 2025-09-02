# simple code for modifying collection from chroma database

from chroma_manager import collection


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

    return


def editMemory():
    # TODO: finish this function.
    return


def deleteMemory():
    # TODO: finish this function.
    return


if __name__ == "__main__":
    addMemory()
