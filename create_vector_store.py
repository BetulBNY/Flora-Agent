# create_vector_store.py
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

print("Starting RAG pipeline setup...")

# 1. Load the knowledge base
print("Loading knowledge base...")
loader = TextLoader("knowledge_base.txt")
documents = loader.load()
print("huhu text loadr", documents)

# 2. Split the documents into smaller chunks
# This is important for better search accuracy.
print("Splitting documents into chunks...")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
texts = text_splitter.split_documents(documents)

# 3. Choose an embedding model
# This model runs locally on your CPU. It's free and private.
print("Initializing embedding model...")
embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

# 4. Create the vector store and save it locally
# FAISS is a library for efficient similarity search.
print("Creating and saving vector store...")
# This can take a moment as it downloads the embedding model for the first time.
vector_store = FAISS.from_documents(texts, embeddings)
vector_store.save_local("faiss_index") # This will create a folder named "faiss_index"

print("\n--- RAG Pipeline Setup Complete! ---")
print("A local vector store has been created in the 'faiss_index' folder.")



# "The HuggingFaceEmbeddings model produces vectors as in-memory objects. Then, FAISS takes these in-memory vectors and serializes them into a persistent binary file on the disk for fast searching later."