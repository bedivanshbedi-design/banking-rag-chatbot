from fastapi import FastAPI, BackgroundTasks, UploadFile, File, HTTPException
import os
from rag.ingestion import process_file
from fastapi import Depends
from backend.app.auth import get_current_user

df = None

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Backend is running"}

ALLOWED_EXTENSIONS = [".csv", ".xlsx"]

def validate_file(filename: str):
    ext = os.path.splitext(filename)[1]
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only CSV and Excel files are allowed."
        )


# from rag.state import data_store   # optional debug
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True) 

from fastapi import UploadFile, File
import pandas as pd
import io

df = None  # global

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        global df

        content = await file.read()

        # Convert to dataframe
        df = pd.read_csv(io.BytesIO(content))

        print(" DF Loaded:", df.shape)

        return {"message": "Upload successful"}

    except Exception as e:
        print("UPLOAD ERROR:", str(e))
        return {"message": f"Error: {str(e)}"}
from fastapi import Body
from rag.query_engine import run_query
from rag.intent import is_aggregation_query

@app.post("/query")
async def query_api(payload: dict = Body(...)):
    user_query = payload.get("query")

    if is_aggregation_query(user_query):
        # simple SQL generation (placeholder)
        sql = "SELECT COUNT(*) FROM data_store"  # improve later
    else:
        sql = "SELECT * FROM data_store LIMIT 5"

    result = run_query(sql)

    return {"result": result.to_dict()}

from agents.graph import build_graph

graph = build_graph()

from fastapi.responses import JSONResponse
from rag.query_engine import run_query
from rag.ingestion import data_store

from rag.state import data_store   # ✅ SAME SOURCE
from backend.app.auth import get_current_user

# @app.post("/chat")
# async def chat(data: dict, current_user: str = Depends(get_current_user)):
#     print("User:", query)
#     try:
#         print("Data store in chat:", data_store.keys())

#         if not data_store:
#             return {"response": "No data uploaded yet"}

#         query = data.get("query")

#         result = run_query(query)

#         return {"response": result.to_string(index=False)}

#     except Exception as e:
#         return {"response": str(e)}

@app.post("/chat")
async def chat(query: dict):
    try:
        global df

        q = query.get("query").lower()

        print("User query:", q)

        if df is None:
            return {"response": "No dataset uploaded"}

        # ✅ columns
        if "column" in q:
            return {"response": str(list(df.columns))}

        # ✅ dataset summary
        if "dataset" in q or "about" in q:
            return {
                "response": f"This dataset has {df.shape[0]} rows and {df.shape[1]} columns: {list(df.columns)}"
            }

        # ✅ first rows
        if "first" in q or "sample" in q:
            return {"response": str(df.head(3))}

        return {"response": "I understand basic data queries now!"}

    except Exception as e:
        print("ERROR:", str(e))
        return {"response": f"Error: {str(e)}"}

    except Exception as e:
        print("ERROR:", str(e))
        return {"response": f"Error: {str(e)}"}

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from backend.app.auth import authenticate_user, create_access_token

@app.post("/token")

async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(status_code = 401, detail="Invalid credentials")
    
    access_token = create_access_token({"sub": user["username"]})
    
    return{"access_token": access_token, "token_type": "bearer"}

