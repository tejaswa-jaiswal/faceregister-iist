from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()  # MUST be first
import imagekit_client
from typing import List
from fastapi import FastAPI, Request, HTTPException, UploadFile, File, Form
from fastapi.responses import RedirectResponse, JSONResponse
from starlette.middleware.sessions import SessionMiddleware
from auth import google
import os

app = FastAPI(title="FastAPI Backend", version="1.0.0")

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET_KEY", "super-secret-key"),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(imagekit_client.router)
app.include_router(google.router)