from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage
# We are using langgraph package for Conversation history
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph


import os
os.environ["GOOGLE_API_KEY"] = 'AIzaSyCEC8v-Kov_Ggd9PjbSQLpBZt_viA6EIuI'

def initialize_llm():
    llm = ChatGoogleGenerativeAI(model='gemini-pro')
    # Define a new graph
    workflow = StateGraph(state_schema=MessagesState)

    # Define the function that calls the model
    def call_model(state: MessagesState):
        response = llm.invoke(state["messages"])
        return {"messages": response}

    # Define the (single) node in the graph
    workflow.add_edge(START, "model")
    workflow.add_node("model", call_model)

    


    # Add memory
    memory = MemorySaver()
    return workflow.compile(checkpointer=memory)


def query(app, thread_id:str, query:str):
    config = {"configurable": {"thread_id": thread_id}}
    input_messages = [HumanMessage(query)]
    for chunk, metadata in app.stream({"messages": input_messages}, config, stream_mode="messages"):
        if isinstance(chunk, AIMessage):
            print(metadata)
            yield chunk.content
