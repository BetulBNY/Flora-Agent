# main.py
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# Import the agent executor we defined in agent.py
from agent import agent_executor, tools

print("🌸 Welcome to FloraAgent! 🌸")
print("I can help you order flowers or answer questions about our products.")
print("Type 'quit' or 'exit' to end the conversation.")
print("-" * 50)

# This is our in-memory store for the conversation history
# For a real application, you would use a database like Redis or DynamoDB
store = {}


def get_session_history(session_id: str):
    """
    Retrieves or creates a chat history for a given session ID.
    """
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

# Wrap our agent executor in a class that automatically handles message history
conversational_agent = RunnableWithMessageHistory(
    agent_executor,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)

# A unique ID for our chat session. In a real app, this would be
# tied to a user's login, a browser cookie, etc.
session_id = "user123"

# The main chat loop
while True:
    try:
        # Get user input from the command line
        user_input = input("You: ")

        # Check for exit command
        if user_input.lower() in ["quit", "exit"]:
            print("Goodbye! 👋")
            break

        # Invoke the conversational agent
        # We must provide the 'configurable' session_id so it knows which history to use
        response = conversational_agent.invoke(
            {"input": user_input},
            config={"configurable": {"session_id": session_id}}
        )

        # Print the AI's response
        print(f"AI: {response['output']}")

    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("\nGoodbye! 👋")
        break
    except Exception as e:
        print(f"An error occurred: {e}")
        break