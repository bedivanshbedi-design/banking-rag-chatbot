from rag.query_engine import run_query

def account_agent(state):
    sql = "SELECT * FROM data_store LIMIT 5"
    
    result = run_query(sql)
    
    return {
        **state,
        "sql_query": sql,
        "result": result.to_dict(),
        "response": f"Here are some recent transactions."
    }