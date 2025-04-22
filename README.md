## How to Run This Project

### 1. Install Dependencies

Make sure you're in the project directory, then run:

```bash
pip install -r requirements.txt 
```
### 2. Update your varibles in .env file

Edit the .env file in the project root and add your Firebase configuration details.

## Environment Variables

Before running the app, create a `.env` file in the root of the project and add the following variables:

```env
FIREBASE_API_KEY=your_firebase_api_key
FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
FIREBASE_PROJECT_ID=your_project_id
FIREBASE_STORAGE_BUCKET=your_project.appspot.com
FIREBASE_MESSAGING_SENDER_ID=your_sender_id
FIREBASE_APP_ID=your_firebase_app_id
```

📝 **Note:**
- All values can be found in your Firebase Console under **Project Settings → General → Your apps**.
- These variables are required to load Firebase configuration dynamically from the backend.

Make sure `.env` is **NOT** committed to Git. It's already listed in `.gitignore`.


### 3. Run the FastAPI Server
Since the main.py file is inside the app/ folder, use this exact command:
```bash
uvicorn app.main:app --reload 
```
Important:
Do not run uvicorn main:app --reload — it will fail because main.py is not in the root directory.


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

##  How to Work with Git (Team Workflow)


Follow these steps to create your own branch, work safely, and contribute to the project.  
**⚠️ Do not push directly to `main`. All changes must go through branches and Pull Requests.**

---

###  1. Create and Switch to Your Own Branch

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

###  2. Commit and Push Changes

After making your changes:

```bash
git add .
git commit -m "Clear message describing what you did"
git push -u origin feature/your-feature-name
```

---

###  3. Open a Pull Request

Go to your Git platform (GitHub, GitLab, etc.):

- Open a Pull Request **from your branch into `develop`**
- Assign a teammate as a reviewer
- Wait for approval and merge if approved

---

## ⚠️ Team Rules

 **Do NOT push to `main`.**  
 Always create and work in your own branch.  
 Pull from `develop` daily to avoid conflicts.  
 Write clear commit messages and branch names.  
 Use Pull Requests for all merges into `develop`.

---

 This ensures safe collaboration and clean version history for everyone.
