# a simple code for inspecting the contents of long term memory
import json
from chroma_manager import (
    collection,
)  # use existing collection and client

output = "./data/psyfighter_memory/chroma_dump/chroma_memory_dump.json"


def memoryDump(output):
    allData = collection.get()
    filteredData = []

    for x in allData["documents"]:
        print(f"\n{x}")
        filteredData.append(x)

    with open(output, "w", encoding="utf-8") as w:
        json.dump(filteredData, w, ensure_ascii=False, indent=2)

    print(f"\nMemory dump was saved to: {output}")


if __name__ == "__main__":
    memoryDump(output)
