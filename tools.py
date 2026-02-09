# tools.py
# This file holds the "skills" of our agent. These are the real-world actions it can perform by running Python code.
import json
import random
from langchain.tools import tool
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine


analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()




# --- Find florist tool ---
@tool
def find_best_florist(address: str, flower_type: str, quantity: int) -> str:
    """
    Finds a suitable florist based on address, flower type, and quantity.
    Returns a JSON string with the florist's details.
    """
    print(f"🔍 Searching florist near {address} for {quantity} {flower_type}...")


    # --- ADDED ERROR LOGIC ---
    if "kadıköy" not in address.lower():
        error_data = {"status": "error", "message": f"Sorry, we do not have any florists in the {address} area."}
        return json.dumps(error_data)
    
    # Simulate finding a real florist with a structured ID
    florist_data = {
        "florist_id": "FLR_123",
        "name": "Kadıköy Flowers",
        "specialty": flower_type,
        "status": "success"
    }
    # Return a machine-readable JSON string, NOT a human-readable sentence.
    return json.dumps(florist_data)


# --- Create flower order tool ---
@tool
def create_flower_order(florist_id: str, address: str, flower_type: str, quantity: int, note: str) -> str:
    """
    Creates a final flower order using a valid florist_id.
    The address MUST be a full, specific street address
    Returns a JSON string with the order confirmation details.
    """
    print(f"🪷 Creating order at {florist_id} for {quantity} {flower_type} to {address}.")

    # --- ADDED VALIDATION LOGIC ---
    if len(address.split()) < 3: # A simple check for a real address
        error_data = {
            "status": "error",
            "message": "The address provided is incomplete. I need a full street address to create an order."
        }
        return json.dumps(error_data)

    
    # Simulate creating a real order with a structured ID
    order_confirmation = {
        "order_id": f"ORD_{random.randint(1000, 9999)}",
        "florist_id": florist_id,
        "status": "confirmed",
        "message": "Order has been successfully placed."
    }
    # Return a machine-readable JSON string.
    return json.dumps(order_confirmation)



# --- RAG Tool for Answering Questions ---
@tool
def get_flower_recommendations(user_query: str) -> str:
    """
    Use this tool to answer general questions about flower recommendations,
    such as what flowers are good for an anniversary, birthday, or expressing sympathy.
    It can also answer questions about flower care.
    """
    print(f"🧠 RAG Tool: Searching knowledge base for '{user_query}'...")
    
    # Initialize the same embedding model we used to create the store
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    
    # Load the local vector store
    vector_store = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

    # Perform a similarity search
    docs = vector_store.similarity_search(user_query, k=2) # k=2 means get the top 2 most relevant chunks
    
    if not docs:
        return "I'm sorry, I couldn't find any specific recommendations for that in my knowledge base."
    
    # Combine the content of the relevant documents to create the answer
    context = "\n---\n".join([doc.page_content for doc in docs])
    return f"Based on my knowledge base, here is some information about '{user_query}':\n{context}"


# --- Tool that redacts PII, replaces it with a placeholder, and stores the real value locally ---
@tool
def redact_pii_and_get_address(text_with_address: str) -> str:
    """
    Extracts and redacts PII like names and addresses from text.
    Returns a clean version of the address for other tools to use.
    This should be the FIRST tool called when a user mentions an address.
    """
    print(f"🕵️ PII Tool: Analyzing text for PII...")
    analyzer_results = analyzer.analyze(
        text=text_with_address,
        language="en") # Use "tr" for Turkish
    
    anonymized_text = anonymizer.anonymize(
        text=text_with_address,
        analyzer_results=analyzer_results
    )

    # In a real system, you would save the real address linked to a session ID
    # For now, we'll just simulate extracting the important part
    address_part = next((res.text for res in analyzer_results if res.entity_type == "LOCATION"), None)
    
    if not address_part:
        return "No valid address found in the text."
        
    print(f"   Address found: '{address_part}'. Text sent to LLM: '{anonymized_text.text}'")
    return f"Address has been processed and saved securely. The address is: {address_part}"

