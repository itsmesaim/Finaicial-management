
from difflib import restore
from fastapi import FastAPI, Request, Form
from fastapi import FastAPI, Request, Form, Depends
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

def send_email_to_user(receiver_email, subject, body):
    EMAIL_ADDRESS = os.getenv("SMTP_EMAIL")
    EMAIL_PASSWORD = os.getenv("SMTP_PASSWORD")

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = receiver_email
    msg.set_content(body)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

def notify_all_users(transaction_info):
    all_users = FirestoreService.get_all_users()

    
    user_details = FirestoreService.get_user(transaction_info.get('user_id'))
    user_name = user_details.get('name') if user_details else "Unknown User"

    subject = "⚡ Important: High Value Transaction Alert"
    body = f"A new transaction exceeded 100 euros!\n\nDetails:\nUser: {user_name}\nAmount: {transaction_info.get('amount')} €"

    for user in all_users:
        email = user.get('email')
        if email:
            send_email_to_user(email, subject, body)



#home
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
        "measurementId": "G-BJXVNHZ404"
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
    print(f"Verification code for {email}: {code}")# (for debugging)

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
        return RedirectResponse("/", status_code=303)# login successful, go home
    else:
        return templates.TemplateResponse("verify-code.html", {
            "request": request,
            "error_message": "Invalid code. Please try again."
        })
#connecting bank account route

@app.get("/connect-bank-account", response_class=HTMLResponse)
async def connect_bank_account_page(request: Request):
    id_token = request.cookies.get("token")
    user_token = validate_firebase_token(id_token)
    
    if not user_token:
        return RedirectResponse("/", status_code=303)
    
    return templates.TemplateResponse("connect-bank-account.html", {
        "request": request,
        "user_token": id_token 
    })

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
    user_id = user_info.get('uid') or user_info.get('user_id') or user_info.get('sub')
    FirestoreService.save_bank_account_info(user_id, account_holder_name, account_last4)

    account_last4 = account_number[-4:]
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



@app.get("/graph-data/summary")
async def get_graph_summary(request: Request):
    """Returns summary data for graphs (e.g., pie or bar chart)."""
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return JSONResponse(status_code=401, content={"message": "Authorization header missing or invalid"})

    id_token = auth_header.split(" ")[1]
    user_info = validate_firebase_token(id_token)
    if not user_info:
        return JSONResponse(status_code=401, content={"message": "Invalid or expired token"})

    user_id = user_info["uid"]
    transactions = BudgetRecommendationService.get_transactions(user_id)

    summary = {
        "income": 0.0,
        "expense": 0.0,
        "labels": [],
        "values": []
    }

    category_totals = {}

    for tx in transactions:
        amount = float(tx.get("amount", 0))
        tx_type = tx.get("type")
        category = tx.get("category", "Uncategorized")

        if tx_type == "income":
            summary["income"] += amount
        elif tx_type == "expense":
            summary["expense"] += amount
            category_totals[category] = category_totals.get(category, 0) + amount

    summary["labels"] = list(category_totals.keys())
    summary["values"] = list(category_totals.values())

    return JSONResponse(content=summary)

# route to transction page
@app.get("/transaction-page", response_class=HTMLResponse)
async def transaction_page(request: Request):
    return templates.TemplateResponse("transaction.html", {"request": request})

@app.get("/transaction-success", response_class=HTMLResponse)
async def transaction_success_page(request: Request):
    return templates.TemplateResponse("transaction-success.html", {"request": request})

#to record the transaction
@app.post("/transaction")
async def new_transaction(request: Request):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return RedirectResponse(url="/", status_code=303)

    id_token = auth_header.split(" ")[1]
    user_info = validate_firebase_token(id_token)
    
    if not user_info:
        return RedirectResponse(url="/", status_code=303)

    user_id = user_info['uid']

    data = await request.json()
    amount = data.get('amount')

    if amount is None:
        return JSONResponse({"error": "Missing amount"}, status_code=400)

    transaction_info = {
        "user_id": user_id,
        "amount": amount
    }

    if amount > 100:
        notify_all_users(transaction_info)

    FirestoreService.save_transaction(user_id, amount)

    return JSONResponse({"message": "Transaction recorded successfully."})

# to save user
@app.post("/save-user")
async def save_user(request: Request):
    data = await request.json()
    user_id = data.get("user_id")
    email = data.get("email")
    name = data.get("name")

    if not user_id or not email:
        return JSONResponse({"error": "Missing user information"}, status_code=400)

    FirestoreService.save_user(user_id, email, name)
    return JSONResponse({"message": "User saved successfully"})


# app/services/categorization_service.py

def categorize_expense(description: str) -> str:
    description = description.lower()
    
    if "uber" in description or "taxi" in description:
        return "Transportation"
    elif "coffee" in description or "starbucks" in description:
        return "Food & Beverage"
    elif "grocery" in description or "walmart" in description:
        return "Groceries"
    elif "netflix" in description or "spotify" in description:
        return "Entertainment"
    elif "rent" in description or "apartment" in description:
        return "Housing"
    else:
        return "Other"

# route to budget-analysis page
@app.get("/budget-analysis", response_class=HTMLResponse)
async def budget_analysis_page(request: Request):
    id_token = request.cookies.get("token")
    user_token = validate_firebase_token(id_token)

    if not user_token:
        return RedirectResponse("/", status_code=303)

    return templates.TemplateResponse("budget-analysis.html", {"request": request, "user_token": user_token})


# route to Personalized-Financial-Suggestions page
@app.get("/personalized-financial", response_class=HTMLResponse)
async def budget_analysis_page(request: Request):
    id_token = request.cookies.get("token")
    user_token = validate_firebase_token(id_token)

    if not user_token:
        return RedirectResponse("/", status_code=303)

    return templates.TemplateResponse("Personalized-Financial-Suggestions.html", {"request": request, "user_token": user_token})

# Create a new overspending alert
@app.post("/alerts")
async def create_alert(request: Request, user_token: dict = Depends(validate_firebase_token)):
    data = await request.json()
    budget_name = data.get("budget_name")
    budget_limit = data.get("budget_limit")
    amount_spent = data.get("amount_spent")

    if not all([budget_name, budget_limit, amount_spent]):
        return JSONResponse({"error": "Missing alert information"}, status_code=400)

    alert_data = {
        "budget_name": budget_name,
        "budget_limit": budget_limit,
        "amount_spent": amount_spent,
    }
    user_id = user_token.get("uid")
    FirestoreService.save_alert(user_id, alert_data)

    return JSONResponse({"message": "Alert created successfully."})

# Fetch all overspending alerts for a user
@app.get("/alerts")
async def get_alerts(user_token: dict = Depends(validate_firebase_token)):
    user_id = user_token.get("uid")
    alerts = FirestoreService.get_user_alerts(user_id)
    return alerts

# Delete an overspending alert
@app.delete("/alerts/{alert_id}")
async def delete_alert(alert_id: str, user_token: dict = Depends(validate_firebase_token)):
    user_id = user_token.get("uid")
    success = FirestoreService.delete_alert(user_id, alert_id)

    if not success:
        return JSONResponse({"error": "Alert not found"}, status_code=404)

    return JSONResponse({"message": "Alert deleted successfully."})




#  predictive insights logic
@app.get("/predictive-insights")
async def get_predictive_insights(user_token: dict = Depends(validate_firebase_token)):
    user_id = user_token.get("uid")

    # Simulated insights - in real scenario, you'd run ML models or statistical analysis
    Predictive_insights = {
        "user_id": user_id,
        "monthly_spending_forecast": 245.75,
        "likely_budget_exceed": True,
        "suggested_savings": 50.00,
        "next_high_expense_category": "Dining",
        "alerts": [
            "Spending on Dining is trending 20% higher than last month.",
            "You are on track to exceed your budget for 'Entertainment'."
        ]
    }

    return JSONResponse(Predictive_insights)

