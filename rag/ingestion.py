import pandas as pd 
import duckdb
import os

data_store = {}

def process_file(file_path: str):
    
    global data_store
    
    ext = os.path.splitext(file_path)[1]
    file_name = os.path.basename(file_path)
    if ext == '.csv':
        df = pd.read_csv(file_path)
        
        data_store[file_name] = df
        
        print("Stored:", file_name)
        print("Shape:", df.shape)
        
        return{
            "rows": len(df),
            "columns": list(df.columns),
            # "sheets" : 1
        }
        
    elif ext == '.xlsx':
        sheets = pd.read_excel(file_path, sheet_name=None   )
        
        sheets_info = {}
        
        for sheet_name, df in sheets.items():
            key = f"{file_name}_{sheet_name}"
            
            sheets_info[sheet_name] = {
                "rows": len(df),
                "columns": list(df.columns)
            }   
            
        return {
            "sheets": len(sheets),
            "details": sheets_info  
        }
        
    else:
        raise ValueError("Unsupported file")
    
