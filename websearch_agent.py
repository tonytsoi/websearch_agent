from langchain.chat_models import init_chat_model
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
import streamlit as st
import credentials
import os
import uuid

os.environ['AWS_DEFAULT_REGION'] = "us-east-1"
os.environ["AWS_ACCESS_KEY_ID"] = credentials.access_key
os.environ["AWS_SECRET_ACCESS_KEY"] = credentials.secret_key

tavily_api_key = credentials.tavily_api_key
thread_id = uuid.uuid4()
config = {"configurable": {"thread_id": thread_id}}

def generate_response(input_text):
    # Create the agent
    memory = MemorySaver()
    model = init_chat_model("amazon.nova-pro-v1:0",
                            model_provider="bedrock_converse")
    search = TavilySearchResults(max_results=2, tavily_api_key=tavily_api_key)
    tools = [search]
    agent_executor = create_react_agent(model, tools, checkpointer=memory)

    # Use the agent
    # for step in agent_executor.stream(
    #         {"messages": [HumanMessage(content=f"{input_text}")]},
    #         config,
    #         stream_mode="values",
    # ):
    #
    #     yield step["messages"][-1]

    # Output only the last message
    response = agent_executor.invoke(
            {"messages": [HumanMessage(content=f"{input_text}")]},
            config
    )

    yield response["messages"][-1].content
        
st.title("AI Web Search Agent")
st.caption("Powered by Amazon Nova Pro")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    
# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message['content'])
        
# Accept user input
if prompt := st.chat_input("What do you want to ask?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = st.write_stream(generate_response(prompt))
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})