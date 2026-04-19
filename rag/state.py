from typing import TypedDict, Optional

data_store = {}
class AgentState(TypedDict):
    user_query: str
    intent: Optional[str]
    sql_query: Optional[str]
    result: Optional[dict]
    response: Optional[str]
    
    