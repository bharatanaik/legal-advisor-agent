from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage
# We are using langgraph package for Conversation history
from langgraph.checkpoint.memory import MemorySaver

from langchain.chains.llm_math.base import LLMMathChain
from langchain_core.tools import tool, Tool
from langchain_core.prompts.prompt import PromptTemplate
from langchain.chains.llm import LLMChain

from langchain_community.utilities.wikipedia import WikipediaAPIWrapper
from langgraph.prebuilt import create_react_agent
from main.utils import LEGAL_ADVISOR_PROMPT
from main.tools import search, legal_search, precedent_checker


import os
os.environ["GOOGLE_API_KEY"] = 'AIzaSyCEC8v-Kov_Ggd9PjbSQLpBZt_viA6EIuI'

def initialize_llm():
    llm = ChatGoogleGenerativeAI(
        model="gemini-pro",
        #convert_system_message_to_human=True,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        handle_parsing_errors=True,
        temperature=0.6,
        # safety_settings = {
        #     HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
        #     HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH,
        #     HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
        #     HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
        # },
    )

    # Tool 1: Math tool which helps AI to calculate sums.
    problem_chain = LLMMathChain.from_llm(llm=llm)
    math_tool = Tool.from_function(name="Calculator",
                    func=problem_chain.run,
                    description="Useful for when you need to answer questions about math. This tool is only for math questions and nothing else. Only input math expressions.")

    # Add memory
    memory = MemorySaver()

    ####################### CASE SUMMARIZER - START ############################

    case_summarizer_template = """
    You are a legal assistant with expertise in summarizing case documents.
    Given the case document: {document}, provide a concise and clear summary highlighting the key points, legal issues, and outcomes.
    """
    case_summarizer_assist_prompt = PromptTemplate(input_variables=["document"], template=case_summarizer_template)
    case_summarizer_chain = LLMChain(llm=llm, prompt=case_summarizer_assist_prompt)
    case_summarizer_tool = Tool.from_function(
        name="case_summarizer_support", 
        func=case_summarizer_chain.run,
        description="Useful for summarizing case documents, highlighting key points, legal issues, and outcomes."
    )

    ####################### CASE SUMMARIZER - END ############################

    ###################### LEGAL DOCUMENT DRAFTER - START #########################

    legal_document_drafter_template = """
    You are an expert legal assistant specializing in drafting legal documents.
    Given the following information: {document}, draft a formal legal document that adheres to standard legal conventions and includes all necessary components (e.g., parties involved, legal clauses, and key provisions).
    Ensure the document is precise, structured, and uses appropriate legal terminology.
    """

    legal_document_drafter_assist_prompt = PromptTemplate(
        input_variables=["document"], 
        template=legal_document_drafter_template
    )

    legal_document_drafter_chain = LLMChain(
        llm=llm, 
        prompt=legal_document_drafter_assist_prompt
    )

    legal_document_drafter_tool = Tool.from_function(
        name="legal_document_drafter_support",
        func=legal_document_drafter_chain.run,
        description="Drafts formal legal documents using precise legal language and standard structure."
    )

    ####################### LEGAL DOCUMENT DRAFTER - END ##############################

    ####################### DAMAGE CALCULATOR TOOL - START #########################

    damage_calculator_template = """
    You are a legal assistant specializing in calculating damages for legal cases.
    Based on the provided details: {case_details}, calculate the estimated damages.
    Consider the nature of the case (e.g., breach of contract, personal injury), any financial losses, non-financial losses, punitive damages, and other relevant factors.
    Provide a breakdown of the calculation.
    """
    damage_calculator_prompt = PromptTemplate(
        input_variables=["case_details"], 
        template=damage_calculator_template
    )

    damage_calculator_chain = LLMChain(
        llm=llm, 
        prompt=damage_calculator_prompt
    )

    damage_calculator_tool = Tool.from_function(
        name="damage_calculator_support",
        func=damage_calculator_chain.run,
        description="Calculates estimated damages for legal cases by considering financial and non-financial losses, and punitive damages."
    )

    ####################### DAMAGE CALCULATOR TOOL - END ##############################


    tools=[ math_tool, search, legal_search, case_summarizer_tool, precedent_checker, legal_document_drafter_tool, damage_calculator_tool]
    
    agent = create_react_agent(llm, tools, checkpointer=memory)

    return agent



def query(app, thread_id:str, query:str):
    config = {"configurable": {"thread_id": thread_id}}
    input_messages = [HumanMessage(query)]
    for chunk, metadata in app.stream({"messages": input_messages}, config, stream_mode="messages"):
        if isinstance(chunk, AIMessage):
            is_stop = chunk.response_metadata.get("finish_reason") == 'STOP'
            yield chunk.content, metadata["checkpoint_ns"], is_stop
