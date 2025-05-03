from difflib import restore
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.auth.authentication import validate_firebase_token
from app.services.firestore_service import FirestoreService
import os
from dotenv import load_dotenv
from datetime import datetime

from google.cloud import firestore

firestore_db = restore.Client()

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




class BudgetRecommendationService:
    @staticmethod
    def get_transactions(user_id: str):
        """Fetch all transactions for the given user."""
        try:
            transactions_ref = firestore_db.collection("transactions").where("user_id", "==", user_id)
            transactions = transactions_ref.stream()
            return [t.to_dict() for t in transactions]
        except Exception as e:
            print(f"Error fetching transactions: {e}")
            return []

    @staticmethod
    def calculate_expenses_and_income(user_id: str):
        """Calculate the total expenses and income for the user."""
        transactions = BudgetRecommendationService.get_transactions(user_id)
        total_expenses = 0
        total_income = 0

        for transaction in transactions:
            amount = float(transaction.get("amount", 0))
            if transaction.get("type") == "expense":
                total_expenses += amount
            elif transaction.get("type") == "income":
                total_income += amount
        
        return total_income, total_expenses

    @staticmethod
    def recommend_budget(user_id: str):
        """Provide budget recommendations based on user's income and expenses."""
        total_income, total_expenses = BudgetRecommendationService.calculate_expenses_and_income(user_id)

        savings_goal = 0.2 * total_income  # Save 20% of income

        if total_expenses > total_income:
            return f"Your expenses are higher than your income. Try cutting down on discretionary expenses. Aim to save at least {savings_goal:.2f}."
        elif total_expenses > total_income * 0.8:
            return f"You're spending about 80% of your income. Consider saving {savings_goal:.2f} or adjusting your budget."
        else:
            return f"Your spending seems healthy. Keep it up! Aim for a saving goal of {savings_goal:.2f}."

    @staticmethod
    def set_financial_goal(user_id: str, goal_name: str, target_amount: float):
        """Set a financial goal for the user."""
        goal_data = {
            "goal_name": goal_name,
            "target_amount": target_amount,
            "user_id": user_id,
            "created_at": firestore.SERVER_TIMESTAMP
        }
        return firestore_db.collection('financial_goals').add(goal_data)
