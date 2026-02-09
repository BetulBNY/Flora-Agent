# 🌸 FloraAgent - AI-Powered Flower Ordering Assistant

FloraAgent is an intelligent conversational AI agent built with LangChain and Google's Gemini AI that helps users order flowers, get recommendations, and find florists. The system features multi-modal deployment options including a command-line interface, web application, and AWS Lambda serverless architecture.

## 🎯 Features

- **Intelligent Flower Ordering**: Complete end-to-end flower ordering workflow with validation
- **RAG-Powered Recommendations**: Uses Retrieval-Augmented Generation to provide contextual flower recommendations for different occasions
- **PII Protection**: Automatically detects and redacts personally identifiable information using Microsoft Presidio
- **Conversational Memory**: Maintains chat history across conversations for natural dialogue flow
- **Multi-Platform Support**: Deploy as CLI, web app, or serverless function
- **Florist Finder**: Location-based florist search and availability checking
- **Smart Validation**: Ensures complete address information before order placement

## 🏗️ Architecture

### Core Components

```
FloraAgent/
│
├── agent.py                    # Main agent definition with LLM and tools
├── tools.py                    # Custom tool implementations
├── knowledge_base.txt          # RAG knowledge base for recommendations
├── create_vector_store.py      # Vector store creation script
│
├── main.py                     # CLI interface
├── app.py                      # Flask web application
├── lambda_function.py          # AWS Lambda handler
│
└── templates/
    └── index.html              # Web UI
```

### Technology Stack

- **LLM**: Google Gemini 2.5 Pro
- **Framework**: LangChain
- **Vector Store**: FAISS
- **Embeddings**: HuggingFace Sentence Transformers
- **PII Detection**: Microsoft Presidio
- **Web Framework**: Flask
- **Cloud**: AWS Lambda + DynamoDB 

## 🚀 Getting Started

### Prerequisites

```bash
Python 3.8+
Google API Key (Gemini)
```

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd FloraAgent
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Create a `.env` file**
```bash
GOOGLE_API_KEY=your_google_api_key_here
```

4. **Build the vector store**
```bash
python create_vector_store.py
```

This will create a `faiss_index` folder containing the vector database for RAG.

## 💻 Usage

### Option 1: Command Line Interface

Run the interactive CLI:

```bash
python main.py
```

Example conversation:
```
You: I want to send 5 roses to my daughter at 123 Akasya Sokak, Kadıköy, Istanbul
AI: I'll help you order those roses. Let me find a suitable florist...

You: What flowers are good for an anniversary?
AI: Based on my knowledge base, Red Roses and Lilies are perfect for anniversaries...
```

### Option 2: Web Application

1. **Start the Flask server**
```bash
python app.py
```

2. **Access the web interface**
```
http://127.0.0.1:5000
```

The web UI provides a modern chat interface with persistent session history.

### Option 3: AWS Lambda Deployment

1. **Set up DynamoDB table**
```bash
aws dynamodb create-table \
    --table-name FloraAgentChatHistory \
    --attribute-definitions AttributeName=SessionId,AttributeType=S \
    --key-schema AttributeName=SessionId,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST
```

2. **Package the Lambda function**
```bash
zip -r floraagent.zip . -x "*.git*" "*.env*" "__pycache__/*"
```

3. **Deploy to Lambda**
- Upload the ZIP file to AWS Lambda
- Set environment variables: `GOOGLE_API_KEY`, `DYNAMODB_TABLE`
- Configure API Gateway trigger

4. **Test the endpoint**
```bash
curl -X POST https://your-api-gateway-url/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "session_id": "user123"}'
```

## 🛠️ Available Tools

### 1. `find_best_florist`
Searches for florists based on location, flower type, and quantity.

**Parameters:**
- `address` (str): Delivery address
- `flower_type` (str): Type of flower requested
- `quantity` (int): Number of flowers

**Returns:** JSON with florist details or error message

### 2. `create_flower_order`
Creates a flower order with a validated florist.

**Parameters:**
- `florist_id` (str): ID from `find_best_florist`
- `address` (str): Full street address (validated)
- `flower_type` (str): Type of flower
- `quantity` (int): Number of flowers
- `note` (str): Personal message

**Returns:** JSON with order confirmation

### 3. `get_flower_recommendations`
Uses RAG to provide flower recommendations for occasions.

**Parameters:**
- `user_query` (str): Question about flowers or occasions

**Returns:** Contextual recommendations from knowledge base

### 4. `redact_pii_and_get_address`
Detects and redacts PII while extracting addresses.

**Parameters:**
- `text_with_address` (str): User input containing address

**Returns:** Cleaned address for processing

## 📚 Knowledge Base

The `knowledge_base.txt` file contains curated information about:
- Anniversary flower recommendations
- Birthday flower suggestions
- Sympathy and condolence flowers
- Flower care instructions

To update the knowledge base:
1. Edit `knowledge_base.txt`
2. Run `python create_vector_store.py`

## 🔒 Security & Privacy

- **PII Redaction**: Names and addresses are automatically detected and handled securely using Microsoft Presidio
- **Data Isolation**: Each user session maintains separate conversation history
- **Environment Variables**: Sensitive credentials stored in `.env` (not committed to repository)

## 🧪 Testing Examples

### Test Case 1: Complete Order Flow
```python
user_request = "I want to send 5 roses to my daughter at 123 Akasya Sokak, Kadıköy, Istanbul. Please add this note: 'Happy birthday my dear daughter!'"
```

### Test Case 2: Recommendations Query
```python
user_request = "What flowers are good for an anniversary?"
```

### Test Case 3: Unavailable Location
```python
user_request = "I want to send flowers to 5 Cicek Sokak, Bakırköy, Istanbul"
# Expected: Error message about service unavailability
```

### Test Case 4: Sympathy Flowers
```python
user_request = "A friend's family member passed away. What kind of flowers are appropriate?"
```

## 🔧 Configuration

### Agent Behavior
Edit the system prompt in `agent.py` to customize:
- Tone and personality
- Validation rules
- Response format
- Tool calling strategy

### LLM Settings
```python
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-pro",
    temperature=0  # Adjust for creativity (0-1)
)
```

### RAG Configuration
```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,      # Adjust chunk size
    chunk_overlap=50     # Adjust overlap
)
```

## 📊 Dependencies

Create a `requirements.txt`:
```
langchain
langchain-google-genai
langchain-community
langchain-huggingface
faiss-cpu
sentence-transformers
presidio-analyzer
presidio-anonymizer
flask
flask-cors
python-dotenv
boto3  # For AWS deployment
```
