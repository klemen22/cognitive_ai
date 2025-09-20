# a simple code for inspecting the contents of long term memory
import json
from itertools import zip_longest
from chroma_manager import collection  # use existing collection

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


def retrieveMemory():
    allData = collection.get()
    finalData = []

    for y in allData["documents"]:
        finalData.append(y)

    return finalData


if __name__ == "__main__":
    # memoryDump()

    memories = retrieveMemory()
    for x in memories:
        print(f"\n{x}")
