from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from typing import TypedDict, Annotated, List
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage,AIMessage, HumanMessage
import os
from typing import Annotated
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv


load_dotenv() 
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
llm = ChatGroq(model="llama-3.1-8b-instant")

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    post: str
    improvements: str
    ans: str


def generate(state: AgentState):
    prompt = ChatPromptTemplate.from_template(
        "You are a Twitter post generator, generate a funny, chicky post about the content {content},provided by the user"
    )
    last_msg = state['messages'][-1].content
    chain = prompt | llm | StrOutputParser()
    post = chain.invoke({"content":last_msg})
    return {'post':post}

def reflector(state: AgentState):
    prompt1 = ChatPromptTemplate.from_template(
        "Based on the post {post} you generated, suggest 3 to 5 improvements to make the post better"
    )
    chain1 = prompt1 | llm | StrOutputParser()
    improvements = chain1.invoke({"post": state['post']})
    return {"improvements": improvements, "messages": [AIMessage(content=improvements)]}

def answer(state : AgentState):
    prompt2 = ChatPromptTemplate.from_template(
        "Now that you've provided improvements {improvements} on the post, generate a final revised post utilizing the improvements"
    )
    chain2 = prompt2 | llm | StrOutputParser()
    ans = chain2.invoke({'improvements': state['improvements']})
    return {'ans': ans, 'messages': [AIMessage(content=ans)]}

def build_graph():
    builder = StateGraph(AgentState)
    builder.add_node("generate", generate)  
    builder.add_node("reflect", reflector)  
    builder.add_node("ans", answer)   
    builder.add_edge(START, "generate")
    builder.add_edge('generate', "reflect")
    builder.add_edge('reflect', "ans")
    builder.add_edge('ans', END)
    return builder.compile()

def run_agent(user_input: str):
    graph = build_graph()
    state = {"messages": [HumanMessage(content=user_input)]}
    result = graph.invoke(state)
    return result