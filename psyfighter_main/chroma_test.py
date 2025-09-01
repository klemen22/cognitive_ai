import chromadb
from chromadb.config import Settings


chromaClient = chromadb.Client()
collection = chromaClient.create_collection(name="test_collection")

# TODO: create an embedding system
collection.add(
    ids=["id1", "id2", "id3"],
    documents=[
        "This text is about dogs.",
        "This text is about cats.",
        "This text is about rabbits",
    ],
)

# query example
result = collection.query(query_texts=["Do you have a text about dogs?"], n_results=1)
print("\n", result["documents"], result["distances"][0][0])
