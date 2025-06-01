from typing import Annotated

from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
import os
from langchain.chat_models import init_chat_model
from langchain_ollama import ChatOllama
from dotenv import load_dotenv
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver

from langgraph.types import Command, interrupt
# This script sets up a chatbot using LangGraph with Ollama's Gemma 3 model.
# It includes a tool node for handling tool calls and streams updates to the user.

# Load environment variables from .env file
load_dotenv()

from src.tools import tools

# Initialize the LLM with the Ollama model
# Ensure you have the Ollama server running and the model downloaded
llm = ChatOllama(model="qwen3:4b", temperature=0)

# Initialize the memory saver to store the state of the graph
memory_saver = MemorySaver()

# Define the state of the graph using TypedDict
class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]
    name: str
    birthday: str

# Initialize the state graph
graph_builder = StateGraph(State)

# Modification: tell the LLM which tools it can call
# highlight-next-line
llm_with_tools = llm.bind_tools(tools)

def chatbot(state: State):
    message = llm_with_tools.invoke(state["messages"])
    assert(len(message.tool_calls) <= 1)
    return {"messages": [message]}

# def route_tools(
#     state: State,
# ):
#     """
#     Use in the conditional_edge to route to the ToolNode if the last message
#     has tool calls. Otherwise, route to the end.
#     """
#     if isinstance(state, list):
#         ai_message = state[-1]
#     elif messages := state.get("messages", []):
#         ai_message = messages[-1]
#     else:
#         raise ValueError(f"No messages found in input state to tool_edge: {state}")
#     if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
#         return "tools"
#     return END


# The first argument is the unique node name
# The second argument is the function or object that will be called whenever
# the node is used.
graph_builder.add_node("chatbot", chatbot)



tool_node = ToolNode(tools=tools)
graph_builder.add_node("tools", tool_node)

# Any time a tool is called, we return to the chatbot to decide the next step
graph_builder.add_edge("tools", "chatbot")

# The `tools_condition` function returns "tools" if the chatbot asks to use a tool, and "END" if
# it is fine directly responding. This conditional routing defines the main agent loop.
graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition
)


# Add Entry Point
graph_builder.add_edge(START, "chatbot")

graph = graph_builder.compile(checkpointer=memory_saver)
config = {"configurable": {"thread_id": "1"}}

def stream_graph_updates(user_input: str):
    for event in graph.stream(
        {"messages": [{"role": "user", "content": user_input}]},
        config, 
        stream_mode="values"
    ):
        if "messages" in event:
            event["messages"][-1].pretty_print()


while True:
    try:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break
        stream_graph_updates(user_input)
    except Exception as ex:
        # fallback if input() is not available

        print("Exiting due to an error or interruption.", ex)
        break