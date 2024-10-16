from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph

from langchain.utilities import DuckDuckGoSearchAPIWrapper
from langchain.chains.llm_math.base import LLMMathChain
from langchain.tools import Tool
from langchain.prompts import PromptTemplate
from langgraph.prebuilt import create_react_agent

import os
os.environ["GOOGLE_API_KEY"] = 'AIzaSyCEC8v-Kov_Ggd9PjbSQLpBZt_viA6EIuI'

legal_advisor_prompt_text = '''
You are a knowledgeable and helpful Indian legal advisor who provides advice and guidance on various legal matters. You assist users in understanding legal issues, interpreting laws, and navigating the legal system according to the Indian Penal code and Indian Laws. You also help them define the best course of action for their situation and provide resources or tools where needed.

Use the tools only when necessary; otherwise, feel free to respond directly. Maintain a professional and approachable tone.

Always start by introducing yourself and asking for the user's name.

Ask for details about the user's legal concerns or case along the way to tailor your advice effectively.

Always give small answers and ask the user if additional information is required or do they want a longer answer

Begin!
'''

def math_tool(llm):
    math_chain = LLMMathChain(llm=llm)
    return Tool(
        name="math_tool",
        func=math_chain.run,
        description="Useful for when you need to answer questions about math. This tool is only for math questions and nothing else. Only input math expressions."
    )

def search_tool():
    search = DuckDuckGoSearchAPIWrapper()
    return Tool(
        name="search_tool",
        func=search.run,
        description="Searches the web for the provided query"
    )

def legal_search_tool():
    legal_database = {
        "contract law": "Contract law in India is governed by the Indian Contract Act, 1872. Case: Mohori Bibee v. Dharmodas Ghose (1903).",
        "intellectual property": "Intellectual property law in India is protected under various statutes like the Indian Patents Act, 1970, and the Copyright Act, 1957. Case: R.G. Anand v. M/S Deluxe Films (1978).",
        "employment law": "Employment law in India includes statutes like the Industrial Disputes Act, 1947, and the Payment of Wages Act, 1936. Case: Bangalore Water Supply v. A Rajappa (1978).",
        "criminal law": "Criminal law in India is primarily governed by the Indian Penal Code (IPC), 1860. Case: State of Maharashtra v. Salman Salim Khan (2004).",
        "family law": "Family law in India covers various personal laws like the Hindu Marriage Act, 1955, and the Muslim Personal Law. Case: Shah Bano Case (1985)."
    }

    def search_legal_database(query: str) -> str:
        for keyword, result in legal_database.items():
            if keyword in query.lower():
                return f"Found result in legal database for '{keyword}': {result}"

        # If no result found in the mock database
        return f"No results found in the legal database for: {query}. Please refine your query."

    return Tool(
        name="legal_search_tool",
        func=search_legal_database,
        description="Searches legal databases for the provided query. Use this tool to find relevant cases and statutes in Indian law, such as contract law, intellectual property law, employment law, criminal law, and family law."
    )

def case_summarizer_tool():
    def get_summary(document: str) -> str:
        prompt_text = f"Please summarize it and give only the key points that seem important.\n\n{document}"
        return f"Gemini summary: {prompt_text}"

    return Tool(
        name="case_summarizer_tool",
        func=get_summary,
        description="Gets the summary of documents passed and returns a short and concise summary."
    )

def precedent_checker_tool():
    indian_precedents = {
        "contract breach": "Precedent: Nandganj Sihori Sugar Co. v. Badri Nath Dixit (1991) - Breach of contract by failing to deliver goods; damages awarded to the plaintiff.",
        "intellectual property theft": "Precedent: R.G. Anand v. Delux Films (1978) - The Supreme Court held that there was no copyright infringement.",
        "wrongful termination": "Precedent: Air India v. Nergesh Meerza (1981) - The Supreme Court ruled against discriminatory termination of air hostesses."
    }

    def get_precedent_case(case_description: str) -> str:
        for keyword, result in indian_precedents.items():
            if keyword in case_description.lower():
                return f"Found relevant precedent: {result}"

        return f"No relevant precedents found for case description: {case_description[:100]}..."

    return Tool(
        name="precedent_checker_tool",
        func=get_precedent_case,
        description="Checks for relevant legal precedents based on case description."
    )

def initialize_llm():
    llm = ChatGoogleGenerativeAI(model='gemini-pro')
    workflow = StateGraph(state_schema=MessagesState)

    def call_model(state: MessagesState):
        config = {"configurable": {"thread_id": "abc123"}}
        math = math_tool(llm)
        search = search_tool()
        legal_search = legal_search_tool()
        case_summarizer = case_summarizer_tool()
        precedent_checker = precedent_checker_tool()

        tools = [math, search, legal_search, case_summarizer, precedent_checker]

        agent = create_react_agent(llm, tools)

        print(f"DEBUG: call_model received messages: {state['messages']}\n\n")
        
        try:
            res = [chunk for chunk in agent.stream(
                    {"messages": [HumanMessage(content="My husband died as a result of chemotherapy. Can I sue the hospital or doctors?")]}, config
                )]
            print(f"DEBUG: agent response: {res}\n\n")
        except Exception as e:
            print(f"ERROR: agent.invoke failed with error: {e} \n\n")
            res = "An error occurred while processing the request."
        
        return {"messages": res}


    workflow.add_edge(START, "model")
    workflow.add_node("model", call_model)

    memory = MemorySaver()
    return workflow.compile(checkpointer=memory)

def query(app, thread_id: str, query: str):
    config = {"configurable": {"thread_id": thread_id}}
    input_messages = [HumanMessage(query)]
    for chunk, metadata in app.stream({"messages": input_messages}, config, stream_mode="messages"):
        if isinstance(chunk, AIMessage):
            yield chunk.content
