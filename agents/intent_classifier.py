def classify_intent(state):
    query = state["user_query"].lower()
    
    if "loan" in query or "interest" in query:
        intent = "loan"
        
    elif "balance" in query or "transaction" in query:
        intent = "account"
        
    elif any(k in query for k in ["total", "average", "count", "trend"]):
        intent = "aggregation"
        
    elif "schedule" in query or "appointment" in query:
        intent = "scheduler"
        
    else:
        intent = "general"
        
    return {**state, "intent": intent}