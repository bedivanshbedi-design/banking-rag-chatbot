def is_aggregation_query(query: str):
    keywords =["total","average","count","sum","trend","breakdown"]
    
    return any(k in query.lower() for k in keywords)
