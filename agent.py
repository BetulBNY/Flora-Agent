# agent.py
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


# Import our custom functions from the other file
from tools import find_best_florist, create_flower_order, get_flower_recommendations, redact_pii_and_get_address

# This line loads the GOOGLE_API_KEY from your .env file
load_dotenv()

# 1. Initialize the LLM (Gemini Pro)
llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0)



tools = [find_best_florist, create_flower_order, get_flower_recommendations, redact_pii_and_get_address]


# 3. Create the prompt template
# This is a critical step that tells the agent how to behave.
prompt = ChatPromptTemplate.from_messages([ # "You are a helpful assistant that helps users order flowers. You have access to tools to find florists and create orders. You must get all the required information from the user before calling the final create_flower_order tool."
    ("system","You are a helpful and conversational flower ordering assistant. "
               "You have access to tools to redact pii and get address, find florists, create orders, and provide recommendations. "
               "If you don't have enough information to use a tool, ask the user for clarification. "
               
               "**Core Rules:**"
               "1. **Grounding:** You MUST base your answers on the factual information provided by the tools. If a tool returns an error or says something is not available, you must accept that as a fact and not contradict it. "
               "2. **Address Validation:** You MUST NOT call the `create_flower_order` tool unless you have a complete and specific street address from the user. A district name alone is not enough. "
               "3. **Tone:** Maintain a professional and confident tone. If you make a mistake, acknowledge it briefly and clearly state the correct information without excessive apologies."
                ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        # The 'agent_scratchpad' is a special variable where the agent stores its thoughts.
        ("placeholder", "{agent_scratchpad}"),
])

# 4. Create the agent by binding the LLM, prompt, and tools together
agent = create_tool_calling_agent(llm, tools, prompt)

# in our code, the "router" is the internal logic of the create_tool_calling_agent. 
# Specifically, it's the LLM, guided by our prompt, that performs this routing. It reads the user's input and the descriptions of all available tools, and its output is a decision: "I should route this task to the find_best_florist tool."

# 5. Create the Agent Executor, which is the runtime environment for the agent
# 'verbose=True' is amazing for debugging. It shows you the agent's step-by-step reasoning.
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 6. Run the agent with a user request
if __name__ == "__main__":
    print("--- FloraAgent Initialized. Processing your request... ---")
    
    user_request = "I want to send 5 roses to my daughter at 123 Akasya Sokak, Kadıköy, İstanbul. Please add this note: 'Happy birthday my dear daughter, I love you so much!'"
    user_request1 = "I want to send 5 daisies to my daughter at 123 Akasya Sokak, Kadıköy, İstanbul. Please add this note: 'Happy birthday my dear daughter, I love you so much!'"
    user_request2 ="What flowers are good for an anniversary?"
    user_request3 ="Tomorrow is my best friends birthday. Actually, I can't decide which flower should I bought. So can you select the best one for her and send it to 5 Asil Sokak, Bakırköy, İstanbul please. Also add this note: Happy birthday my dear bf you are my hardworking cow bee..."
    user_request4 = "A friend's family member passed away. What kind of flowers are appropriate?"

    # The .invoke() method runs the agent and waits for the final answer
    result = agent_executor.invoke({"input": user_request4})

    print("\n--- FINAL AGENT RESPONSE ---")
    print(result["output"])