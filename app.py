# app.py
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# Import the agent executor we defined in agent.py
# Make sure agent.py does not have a running loop at the bottom
from agent import agent_executor

# --- 1. SET UP THE FLASK APP ---
app = Flask(__name__, template_folder='templates')
CORS(app) # This allows our frontend to communicate with our backend

# --- 2. SET UP CONVERSATIONAL MEMORY ---
# This is our in-memory store for chat histories
# For production, you would replace this with Redis, DynamoDB, or a file-based DB
store = {}

def get_session_history(session_id: str):
    """Retrieves or creates a chat history for a given session ID."""
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

# --- 3. WRAP THE AGENT WITH MEMORY ---
# This is the same logic from our old main.py file
conversational_agent = RunnableWithMessageHistory(
    agent_executor,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)

# --- 4. DEFINE THE API ROUTES ---

@app.route('/')
def index():
    """Serves the frontend HTML file."""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """The main chat endpoint that receives user messages and returns AI responses."""
    try:
        data = request.get_json()
        user_message = data.get("message")
        session_id = data.get("session_id")

        if not user_message or not session_id:
            return jsonify({"error": "Missing message or session_id"}), 400

        # Invoke the conversational agent with the user's message and session_id
        response = conversational_agent.invoke(
            {"input": user_message},
            config={"configurable": {"session_id": session_id}}
        )

        # Return the agent's output as a JSON response
        return jsonify({"response": response['output']})

    except Exception as e:
        print(f"Error in /chat: {e}")
        return jsonify({"error": "An internal error occurred"}), 500


# --- 5. RUN THE APP ---
if __name__ == '__main__':
    # This makes the Flask app run
    # The app will be accessible at http://127.0.0.1:5000
    app.run(host='0.0.0.0', port=5000)