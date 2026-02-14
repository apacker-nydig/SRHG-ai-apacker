# Core imports
import os
import getpass
import json
import operator
from typing import Annotated, List, Literal, Sequence, TypedDict
from uuid import uuid4

import certifi
from langchain.agents import create_agent
from langchain_anthropic import ChatAnthropic
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from pydantic import BaseModel
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

# Zscaler SSL setup for corporate network
zscaler_cert = "/Users/ari.packer/repos/sidekick/zscaler.pem"
combined_cert = "/tmp/combined_certs.pem"

with open(combined_cert, "w") as outfile:
    with open(certifi.where(), "r") as certifi_file:
        outfile.write(certifi_file.read())
    with open(zscaler_cert, "r") as zscaler_file:
        outfile.write(zscaler_file.read())

os.environ['REQUESTS_CA_BUNDLE'] = combined_cert
os.environ['SSL_CERT_FILE'] = combined_cert
os.environ['CURL_CA_BUNDLE'] = combined_cert

print("Zscaler SSL certificates configured")

# Set Anthropic API Key
os.environ["ANTHROPIC_API_KEY"] = os.environ.get("ANTHROPIC_API_KEY", "")

# Tavily API Key for web search
os.environ["TAVILY_API_KEY"] = os.environ.get("TAVILY_API_KEY", "")

# Initialize LLMs - Claude Sonnet 4.5 for supervisors, Claude Haiku for investment specialist agents

# Supervisor model - better reasoning for routing and orchestration
supervisor_llm = ChatAnthropic(model="claude-sonnet-4-5-20250929", temperature=0)

# Specialist model - cost-effective for domain-specific tasks
specialist_llm = ChatAnthropic(model="claude-haiku-4-5-20250929", temperature=0)

# Test both models
print("Testing models...")
supervisor_response = supervisor_llm.invoke("Say 'Supervisor ready!' in exactly 2 words.")
specialist_response = specialist_llm.invoke("Say 'Specialist ready!' in exactly 2 words.")

print(f"Supervisor (Claude Sonnet 4.5): {supervisor_response.content}")
print(f"Specialist (Claude Haiku 4.5): {specialist_response.content}")

print("LangGraph and LangChain components imported!")

# First, let's set up our RAG system for the investment knowledge base

# Load and chunk the investor letter
loader = PyMuPDFLoader("data/Stone Ridge 2025 Investor Letter.pdf")
documents = loader.load()

# Preprocess documents to remove Risk Disclosures section
# Risk disclosures were causing irrelevant context retrievals
for doc in documents:
    if 'Risk Disclosures' in doc.page_content:
        doc.page_content = doc.page_content.split('Risk Disclosures')[0]

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)
chunks = text_splitter.split_documents(documents)

print(f"Loaded and split into {len(chunks)} chunks")

# Set up vector store for investment knowledge base
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
embedding_dim = len(embedding_model.embed_query("test"))

qdrant_client = QdrantClient(":memory:")
qdrant_client.create_collection(
    collection_name="investment_multiagent",
    vectors_config=VectorParams(size=embedding_dim, distance=Distance.COSINE)
)

vector_store = QdrantVectorStore(
    client=qdrant_client,
    collection_name="investment_multiagent",
    embedding=embedding_model
)
vector_store.add_documents(chunks)

retriever = vector_store.as_retriever(search_kwargs={"k": 3})
print(f"Vector store ready with {len(chunks)} investment documents")

# Create specialized tools for each investment agent domain

@tool
def search_market_outlook(query: str) -> str:
    """Search for market trends, economic conditions, and macro outlook from the Stone Ridge investor letter.
    Use this for questions about market environment, economic forecasts, and market analysis.
    """
    results = retriever.invoke(f"market trends economic conditions macro {query}")
    if not results:
        return "No market outlook information found."
    return "\n\n".join([f"[Source {i+1}]: {doc.page_content}" for i, doc in enumerate(results)])

@tool
def search_investment_strategy(query: str) -> str:
    """Search for investment strategy, portfolio positioning, and asset allocation information from the Stone Ridge investor letter.
    Use this for questions about investment approach, portfolio construction, and strategic decisions.
    """
    results = retriever.invoke(f"investment strategy portfolio allocation positioning {query}")
    if not results:
        return "No investment strategy information found."
    return "\n\n".join([f"[Source {i+1}]: {doc.page_content}" for i, doc in enumerate(results)])

@tool
def search_risk_info(query: str) -> str:
    """Search for risk management, tail risk, and diversification information from the Stone Ridge investor letter.
    Use this for questions about risk factors, hedging strategies, and risk mitigation.
    """
    results = retriever.invoke(f"risk management tail risk hedging diversification {query}")
    if not results:
        return "No risk management information found."
    return "\n\n".join([f"[Source {i+1}]: {doc.page_content}" for i, doc in enumerate(results)])

@tool
def search_performance_info(query: str) -> str:
    """Search for performance data, returns, and benchmark information from the Stone Ridge investor letter.
    Use this for questions about investment returns, performance metrics, and historical results.
    """
    results = retriever.invoke(f"performance returns benchmark CAGR historical results {query}")
    if not results:
        return "No performance information found."
    return "\n\n".join([f"[Source {i+1}]: {doc.page_content}" for i, doc in enumerate(results)])

print("Investment specialist tools created!")

# Create investment specialist agents using create_agent (LangChain 1.0 API)
# Each specialist uses Claude Haiku for cost efficiency

market_outlook_agent = create_agent(
    model=specialist_llm,
    tools=[search_market_outlook],
    system_prompt="You are a Market Outlook Specialist. Help users understand market trends, economic conditions, and the macro environment. Always search the knowledge base before answering. Be concise and data-driven."
)

investment_strategy_agent = create_agent(
    model=specialist_llm,
    tools=[search_investment_strategy],
    system_prompt="You are an Investment Strategy Specialist. Help users with portfolio positioning, asset allocation, and investment philosophy. Always search the knowledge base before answering. Be concise and data-driven."
)

risk_management_agent = create_agent(
    model=specialist_llm,
    tools=[search_risk_info],
    system_prompt="You are a Risk Management Specialist. Help users understand risk factors, tail risks, hedging strategies, and diversification. Always search the knowledge base before answering. Be concise and data-driven."
)

performance_analysis_agent = create_agent(
    model=specialist_llm,
    tools=[search_performance_info],
    system_prompt="You are a Performance Analysis Specialist. Help users with investment returns, performance metrics, benchmarks, and historical data. Always search the knowledge base before answering. Be concise and data-driven."
)

print("Investment specialist agents created (using Claude Haiku with create_agent)!")

# Define the supervisor state and routing

def create_router_output(options: list[str]) -> type[BaseModel]:
    """Create a RouterOutput class with the given routing options."""
    options_literal = Literal[tuple(options)]  # type: ignore

    class RouterOutput(BaseModel):
        """The supervisor's routing decision."""
        next: options_literal  # type: ignore
        reasoning: str

    return RouterOutput

def create_routing_llm(options: list[str]):
    """Create an LLM bound to structured output for the given routing options."""
    router_output = create_router_output(options)
    return supervisor_llm.with_structured_output(router_output)

class SupervisorState(TypedDict):
    """State for the supervisor multi-agent system."""
    messages: Annotated[list[BaseMessage], add_messages]
    next: str

print("Supervisor state defined!")

# Create the supervisor node (using Claude Sonnet 4.5 for routing decisions)

supervisor_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an Investment Supervisor coordinating a team of specialist agents.

Your team:
- market_outlook: Handles market trends, economic conditions, macro environment questions
- investment_strategy: Handles portfolio positioning, asset allocation, investment approach questions
- risk_management: Handles risk factors, tail risks, hedging, diversification questions
- performance_analysis: Handles returns, benchmarks, performance metrics, historical data questions

Based on the user's question, decide which ONE specialist should respond.
Choose the most relevant specialist for the primary topic of the question."""),
    ("human", "User question: {question}\n\nWhich specialist should handle this?")
])

# Markets Team Lead
markets_team_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are the Markets Team Lead.
Your team has two specialists:
- market_outlook: Handles market trends, economic conditions, and macro environment
- performance_analysis: Handles returns, benchmarks, and performance metrics

Route to the most appropriate specialist for the user's question."""),
    ("human", "Question: {question}")
])

# Strategy Team Lead
strategy_team_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are the Strategy Team Lead.
Your team has two specialists:
- investment_strategy: Handles portfolio positioning, asset allocation, and investment philosophy
- risk_management: Handles risk factors, tail risks, hedging, and diversification

Route to the most appropriate specialist for the user's question."""),
    ("human", "Question: {question}")
])

director_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are the Investment Director overseeing two teams:
- markets: Markets Team (market outlook, performance analysis)
- strategy: Strategy Team (investment strategy, risk management)

Route to the appropriate team based on the user's question."""),
    ("human", "Question: {question}")
])


def create_supervisor_node(options: list[str], prompt: ChatPromptTemplate):
    """Create a supervisor node that routes to the given options."""
    routing_llm = create_routing_llm(options)

    def supervisor_node(state: SupervisorState):
        """The supervisor decides which agent to route to."""
        user_question = ""
        for msg in reversed(state["messages"]):
            if isinstance(msg, HumanMessage):
                user_question = msg.content
                break

        prompt_value = prompt.invoke({"question": user_question})
        result = routing_llm.invoke(prompt_value)

        print(f"[Supervisor] Routing to: {result.next}")
        print(f"  Reason: {result.reasoning}")

        return {"next": result.next}

    return supervisor_node


print("Supervisor node created (using Claude Sonnet 4.5)!")

def create_agent_node(agent, name: str):
    """Create a node that runs a specialist agent and returns the final response."""
    def agent_node(state: SupervisorState):
        print(f"[{name.upper()} Agent] Processing request...")

        # Invoke the specialist agent with the conversation
        result = agent.invoke({"messages": state["messages"]})

        # Get the agent's final response
        agent_response = result["messages"][-1]

        # Add agent identifier to the response
        response_with_name = AIMessage(
            content=f"[{name.upper()} SPECIALIST]\n\n{agent_response.content}",
            name=name
        )

        print(f"[{name.upper()} Agent] Response complete.")
        return {"messages": [response_with_name]}

    return agent_node

# Create nodes for the supervisors
director_node = create_supervisor_node(["markets", "strategy"], director_prompt)
strategy_lead_node = create_supervisor_node(["investment_strategy", "risk_management"], strategy_team_prompt)
markets_lead_node = create_supervisor_node(["market_outlook", "performance_analysis"], markets_team_prompt)
print("Supervisor nodes created!")

# Create nodes for each investment specialist
market_outlook_node = create_agent_node(market_outlook_agent, "market_outlook")
investment_strategy_node = create_agent_node(investment_strategy_agent, "investment_strategy")
risk_management_node = create_agent_node(risk_management_agent, "risk_management")
performance_analysis_node = create_agent_node(performance_analysis_agent, "performance_analysis")
print("Agent nodes created!")

# Build the supervisor graph
# KEY: Specialists go directly to END (no loop back to supervisor)

def route_to_agent(state: SupervisorState) -> str:
    """Route to the next agent based on supervisor decision."""
    return state["next"]

# Create the graph
supervisor_workflow = StateGraph(SupervisorState)

# Add nodes
supervisor_workflow.add_node("director", director_node)
supervisor_workflow.add_node("strategy", strategy_lead_node)
supervisor_workflow.add_node("markets", markets_lead_node)
supervisor_workflow.add_node("market_outlook", market_outlook_node)
supervisor_workflow.add_node("investment_strategy", investment_strategy_node)
supervisor_workflow.add_node("risk_management", risk_management_node)
supervisor_workflow.add_node("performance_analysis", performance_analysis_node)

# Add edges: START -> supervisor
supervisor_workflow.add_edge(START, "director")

# Conditional routing from director to managers
supervisor_workflow.add_conditional_edges(
    "director",
    route_to_agent,
    {
        "strategy": "strategy",
        "markets": "markets"
    }
)

# Conditional routing from director to managers
supervisor_workflow.add_conditional_edges(
    "strategy",
    route_to_agent,
    {
        "investment_strategy": "investment_strategy",
        "risk_management": "risk_management",
    }
)

# Conditional routing from director to managers
supervisor_workflow.add_conditional_edges(
    "markets",
    route_to_agent,
    {
        "market_outlook": "market_outlook",
        "performance_analysis": "performance_analysis",
    }
)

# KEY FIX: Each specialist goes directly to END (no looping!)
supervisor_workflow.add_edge("market_outlook", END)
supervisor_workflow.add_edge("investment_strategy", END)
supervisor_workflow.add_edge("risk_management", END)
supervisor_workflow.add_edge("performance_analysis", END)

# Compile
supervisor_graph = supervisor_workflow.compile()

response = supervisor_graph.invoke({
    "messages": [HumanMessage(content="What is Stone Ridge's view on the current market environment?")]
})

print("\nFinal Response:")
print("=" * 50)
print(response["messages"][-1].content)
