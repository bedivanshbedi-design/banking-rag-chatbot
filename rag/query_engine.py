import duckdb
from rag.state import data_store

def run_query(query: str):
    con = duckdb.connect()
    
    for name,df in data_store.items():
        con.register(name.replace(". ", "_"), df)
        

    result = con.execute(query).fetchdf()
    return result
  
    
