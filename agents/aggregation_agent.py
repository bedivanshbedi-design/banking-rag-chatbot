from rag.query_engine import run_query

def aggregation_agent(state):
    sql = "SELECT COUNT(*) as total_records from data_store"
    
    result = run_query(sql)
    
    return {
        **state,
        "sql_query": sql,
        "result": result.to_dict(),
        "response": f"Aggregated result: {result.to_dict()}"        
    }
    