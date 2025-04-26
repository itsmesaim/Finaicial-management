from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.auth.authentication import validate_firebase_token
from app.services.firestore_service import FirestoreService
import os
from dotenv import load_dotenv


app = FastAPI()
load_dotenv()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates for rendering HTML
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    id_token = request.cookies.get("token")
    user_token = validate_firebase_token(id_token)
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "user_token": user_token,
        "error_message": None,
    })

# Add POST handler for root path if forms in index.html submit to "/"
@app.post("/", response_class=HTMLResponse)
async def handle_root_post(request: Request):
    id_token = request.cookies.get("token")
    user_token = validate_firebase_token(id_token)
    
    # Process the form data as needed or redirect to appropriate page
    return templates.TemplateResponse("index.html", {
        "request": request,
        "user_token": user_token,
        "error_message": None,
    })

@app.get("/firebase-config")
async def firebase_config():
    config = {
        "apiKey": "AIzaSyBQephotjyQpxZnMM1L8NlS0e09YcEy5ok",
        "authDomain": "task-manager-cbe64.firebaseapp.com",
        "projectId": "task-manager-cbe64",
        "storageBucket": "task-manager-cbe64.appspot.com",
        "messagingSenderId": "711796803171",
        "appId": "1:711796803171:web:8e2e5ae52bc3188dd05a56",
        "measurementId": "G-BJXVNHZ404"
    }
    return JSONResponse(config)

#connecting bank account route

@app.post("/connect-bank-account")
async def connect_bank_account(request: Request):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return JSONResponse(status_code=401, content={"message": "Authorization header missing or invalid"})

    id_token = auth_header.split(" ")[1]
    user_info = validate_firebase_token(id_token)
    if not user_info:
        return JSONResponse(status_code=401, content={"message": "Invalid or expired token"})

    data = await request.json()
    account_holder_name = data.get('account_holder_name')
    account_number = data.get('account_number')

    if not account_holder_name or not account_number:
        return JSONResponse(status_code=400, content={"message": "Missing account holder or account number"})

    account_last4 = account_number[-4:]  # Only store last 4 digits
    FirestoreService.save_bank_account_info(user_info['uid'], account_holder_name, account_last4)


    return JSONResponse(status_code=200, content={"message": "Bank account connected securely."})