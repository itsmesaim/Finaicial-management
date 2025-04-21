from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.auth.authentication import validate_firebase_token
# from app.services.firestore_service import FirestoreService
import os

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
        "apiKey": os.getenv("FIREBASE_API_KEY"),
        "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
        "projectId": os.getenv("FIREBASE_PROJECT_ID"),
        "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
        "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
        "appId": os.getenv("FIREBASE_APP_ID"),
    }
    return JSONResponse(config)
