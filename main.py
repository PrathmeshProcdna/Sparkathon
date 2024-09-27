from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from Backend.chat import Chat

app = FastAPI()
Chatbot = Chat()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],  
    allow_credentials=True,  
    allow_methods=["*"],  
    allow_headers=["*"],  
)

async def read_root():
    return {'message':'Incentive Buddy'}

@app.post('/Chat/')
async def chat(query:str):
    try:
        ans = Chatbot.exe_query(query)
        return ans
    except HTTPException as e:
        return "Unable to chat"