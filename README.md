# Financial Management System

[![Contributors](https://img.shields.io/github/contributors/itsmesaim/Finaicial-management.svg?style=for-the-badge)](https://github.com/itsmesaim/Finaicial-management/graphs/contributors)

---

## Clone the repository
```bash  
git clone https://github.com/itsmesaim/Finaicial-management.git   
```

### Navigate into the project directory 
```bash
cd Finaicial-management
```

### Switch to the develop branch 
```bash
git checkout develop 
```

### Pull latest updates from develop 
```bash
git pull origin develop
```

---

## How to Run This Project

### 1. Install Dependencies
Make sure you're in the project directory, then run:
```bash
pip install -r requirements.txt 
```

---

### 2. Setup Your Environment Variables

Before running the app, create a `.env` file in the root of the project and add the following variables:

```env
# Firebase Configuration
FIREBASE_API_KEY=your_firebase_api_key
FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
FIREBASE_PROJECT_ID=your_project_id
FIREBASE_STORAGE_BUCKET=your_project.appspot.com
FIREBASE_MESSAGING_SENDER_ID=your_sender_id
FIREBASE_APP_ID=your_firebase_app_id

# SMTP Gmail Settings for Email Verification (2FA)
SMTP_EMAIL=your_gmail_address@gmail.com
SMTP_PASSWORD=your_16_character_gmail_app_password
```

📝 **Notes:**
- Firebase values can be found in your Firebase Console under **Project Settings → General → Your apps**.
- SMTP is used to send the 6-digit verification code emails after login/signup.

---

### How to Set Up Gmail SMTP App Password
If you are using Gmail for sending verification emails:

1. Enable **2-Step Verification** on your Google account:  
   https://myaccount.google.com/security

2. Generate an **App Password** here:  
   https://myaccount.google.com/apppasswords

3. Select **"Other"** for the App type, name it like `FastAPI SMTP`, and generate.

4. Copy the 16-character password Google gives you (looks like `abcd efgh ijkl mnop`).

5. Use that password inside your `.env` under `SMTP_PASSWORD`.

🔴 Never use your normal Gmail password. Use only App Passwords for SMTP authentication.

---

### 3. Run the FastAPI Server
Since your `main.py` is inside the `app/` folder, use:

```bash
uvicorn app.main:app --reload 
```

**Important:**  
Do **not** run `uvicorn main:app --reload` — it will fail because `main.py` is inside `app/` directory.

---

##  How to Work with Git (Team Workflow)

Follow these steps to create your own branch, work safely, and contribute to the project.  
**⚠️ Do not push directly to `main`. All changes must go through branches and Pull Requests.**

---

### 1. Create and Switch to Your Own Branch

Start by updating your local code:

```bash
git checkout develop
git pull origin develop
```

Then create a new branch for your feature or bugfix:

```bash
git checkout -b feature/your-feature-name
```

**Examples:**
- `feature/login-ui`
- `feature/add-user`
- `bugfix/login-error`
- `docs/update-readme`

---

### 2. Commit and Push Changes

After making your changes:

```bash
git add .
git commit -m "Clear message describing what you did"
git push -u origin feature/your-feature-name
```

---

### 3. Open a Pull Request

Go to your GitHub repository:

- Open a Pull Request **from your branch into `develop`**
- Assign a teammate as a reviewer
- Wait for approval and merge if approved

---

## ⚠️ Team Rules

- Do **NOT** push directly to `main`.
- Always create and work in your own branch.
- Pull from `develop` daily to avoid conflicts.
- Write clear commit messages and branch names.
- Use Pull Requests for all merges into `develop`.

---

This ensures safe collaboration and clean version history for everyone.

<br/>

# 🚀 Project Owner

- [<img src="https://github.com/itsmesaim.png" width="80px"><br><sub>itsmesaim</sub>](https://github.com/itsmesaim)

---

## ✨ Contributors

Thanks to these amazing people:

| [<img src="https://github.com/ahmedbilalkhan123.png" width="100px"><br><sub>ahmedbilalkhan123</sub>](https://github.com/ahmedbilalkhan123) | [<img src="https://github.com/dhanishthayyil.png" width="100px"><br><sub>Dany</sub>](https://github.com/dhanishthayyil) | [<img src="https://github.com/Evanskiplagat.png" width="100px"><br><sub>evans kiplagat kimutai</sub>](https://github.com/Evanskiplagat) | [<img src="https://github.com/rkeesari98.png" width="100px"><br><sub>rkeesari98</sub>](https://github.com/rkeesari98) |
| :---: | :---: | :---: | :---: |
| [<img src="https://github.com/SaiSudheer5530.png" width="100px"><br><sub>SaiSudheer5530</sub>](https://github.com/SaiSudheer5530) | [<img src="https://github.com/TejeshMalepati.png" width="100px"><br><sub>TejeshMalepati</sub>](https://github.com/TejeshMalepati) | [<img src="https://github.com/vamsikiran75.png" width="100px"><br><sub>vamsikiran75</sub>](https://github.com/vamsikiran75) | [<img src="https://github.com/vineet705.png" width="100px"><br><sub>Vinit Korat</sub>](https://github.com/vineet705) |
| :---: | :---: | :---: | :---: |
