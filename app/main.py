from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.auth.authentication import validate_firebase_token
import os
import random
import smtplib
from email.message import EmailMessage

app = FastAPI()
load_dotenv()

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Temporary storage for verification codes
verification_codes = {}

def generate_verification_code():
    return ''.join(random.choices('0123456789', k=6))

def send_verification_email(receiver_email, code):
    EMAIL_ADDRESS = os.getenv("SMTP_EMAIL")
    EMAIL_PASSWORD = os.getenv("SMTP_PASSWORD")

    msg = EmailMessage()
    msg['Subject'] = 'Your Verification Code'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = receiver_email
    msg.set_content(f"Your verification code is: {code}")

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    id_token = request.cookies.get("token")
    user_token = validate_firebase_token(id_token)
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

@app.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.get("/verify-code", response_class=HTMLResponse)
async def verify_code_page(request: Request):
    return templates.TemplateResponse("verify-code.html", {"request": request})

@app.post("/send-verification")
async def send_verification(request: Request):
    form = await request.form()
    email = form.get("email")

    if not email:
        return JSONResponse({"error": "Email required"}, status_code=400)

    code = generate_verification_code()
    verification_codes[email] = code
    send_verification_email(email, code)
    print(f"Verification code for {email}: {code}")  # (for debugging)

    return JSONResponse({"message": "Verification code sent"})

@app.post("/verify-code", response_class=HTMLResponse)
async def verify_code_submit(request: Request, code: str = Form(...)):
    id_token = request.cookies.get("token")
    user_token = validate_firebase_token(id_token)
    
    if not user_token:
        return RedirectResponse("/", status_code=303)

    email = user_token.get('email')

    if not email or email not in verification_codes:
        return RedirectResponse("/", status_code=303)

    expected_code = verification_codes[email]

    if code == expected_code:
        verification_codes.pop(email, None)
        return RedirectResponse("/", status_code=303)  # login successful, go home
    else:
        return templates.TemplateResponse("verify-code.html", {
            "request": request,
            "error_message": "Invalid code. Please try again."
        })
