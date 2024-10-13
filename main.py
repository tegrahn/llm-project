
import pysqlite3
import sys
# Fix for sqlite version
sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
from fastapi import FastAPI, Header ,Request, Query, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse
from typing import Annotated, Union

from pydantic import BaseModel
import chromadb
import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI

import time
import shutil
import os
import helpers
from pathlib import Path

#FastAPI setup
app = FastAPI()
app.mount("/static/", StaticFiles(directory="static",html=True), name="static")

#Setup for langchain prompt pipelines
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
chroma_client = chromadb.PersistentClient(path="contexts")
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.5,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)
question_history = [] #Setup history to stop repeating questions

@app.get("/", response_class=HTMLResponse)
def read_html():
    html_file_path = Path("static/index.html")
    html_content = html_file_path.read_text()
    return html_content

class TopicInput(BaseModel):
    topic: str
    attributes: str #"" If no attributes
    style: str 
    is_file: bool
    is_new_topic: bool

# Generate topic suggestions
@app.post("/topicsuggestions")
async def topic_suggestions(data: TopicInput):
    data = helpers.generate_topics(chroma_client, llm, data.topic, data.attributes, data.is_file)
    return data
    
# Generatate question
@app.post("/generatequestion")
async def topic_suggestions(data: TopicInput):
    if (data.is_new_topic):
        question_history.clear() #Empty the question_history for a new topic
    # Genereate Question
    data = helpers.generate_question(chroma_client, llm, data.topic, data.attributes, 
    data.style, data.is_file, question_history)
    # Append to history
    question_history.append(data) 
    return { "question" : data }

# Process file into chromadb
@app.post("/uploadfile")
async def upload_file(file: UploadFile = File(...)):
    file_location = f"{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    helpers.add_file(chroma_client, file.filename)
    return

# Delete file
@app.delete("/deletefile/{filename}")
async def delete_file_endpoint(filename: str):
    helpers.remove_file(chroma_client, filename)
    return