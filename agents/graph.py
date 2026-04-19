from langgraph.graph import StateGraph, END

# from agents.state import AgentState
from agents.aggregation_agent import aggregation_agent
from agents.account_agent import account_agent 
from agents.general_agent import general_agent
from agents.intent_classifier import classify_intent
from agents.scheduler_agent import scheduler_agent
from agents.loan_agent import loan_agent

def route_intent(state):
    intent = state["intent"]
    
    if intent == "loan":
        return loan_agent(state)
    
    elif intent == "account":
        return account_agent(state)
    
    elif intent == "aggregation":
        return aggregation_agent(state)
    
    elif intent == "scheduler":
        return scheduler_agent(state)
    
    else:
        return general_agent(state)
    
from rag.state import AgentState

def build_graph():
    builder =StateGraph(AgentState)
    
    #Nodes
    builder.add_node("classifier", classify_intent)
    builder.add_node("account", account_agent)
    builder.add_node("general", general_agent)
    builder.add_node("scheduler", scheduler_agent)
    builder.add_node("loan", loan_agent)
    builder.add_node("aggregation", aggregation_agent)
    
    # Entry point
    
    builder.set_entry_point("classifier")
    
    #Conditional routing
    
    builder.add_conditional_edges(
        "classifier",
        route_intent,
        {
            "loan": "loan",
            "account": "account",
            "aggregation": "aggregation",
            "scheduler": "scheduler",
            "general": "general"
        }   
    )
    
    #End edges
    
    builder.add_edge("account", END)
    builder.add_edge("general", END)
    builder.add_edge("scheduler", END)
    builder.add_edge("loan", END)
    builder.add_edge("aggregation", END)
    
    return builder.compile()

