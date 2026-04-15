import os
import chromadb
from chromadb.utils import embedding_functions

# 1. Initialize the Scientific Knowledge Vault
CHROMA_DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'science_vault')
client = chromadb.PersistentClient(path=CHROMA_DATA_PATH)
embedding_model = embedding_functions.DefaultEmbeddingFunction()

# 2. Create the collection for "All Science"
science_collection = client.get_or_create_collection(
    name="global_science_data", 
    embedding_function=embedding_model
)

def add_scientific_data(topic_id, content, metadata=None):
    """Adds a new scientific concept to the central storage."""
    if metadata is None:
        metadata = {}
    science_collection.add(
        documents=[content],
        metadatas=[metadata],
        ids=[topic_id]
    )
    print(f"[Vector Store] Instilled knowledge into vault: {topic_id}")

def search_science(query, n_results=3):
    """Searches the entire vault for the most relevant answer."""
    results = science_collection.query(
        query_texts=[query],
        n_results=n_results
    )
    
    # Return the closest matching documents as a list of strings
    if results and 'documents' in results and len(results['documents']) > 0:
         return results['documents'][0]
    return []

# Example Sandbox / Test Execution
if __name__ == "__main__":
    print("--- Initializing the Knowledge Vault ---")
    
    add_scientific_data(
        topic_id="physics_newton_2nd",
        content="Newton's second law of motion states that F = ma. The acceleration of an object depends on the mass of the object and the amount of force applied.",
        metadata={"subject": "Physics", "topic": "Dynamics", "difficulty": "Beginner"}
    )
    
    test_question = "What is the formula for force?"
    context = search_science(test_question, n_results=1)
    print(f"\nRetrieved Science Context:\n{context}")
