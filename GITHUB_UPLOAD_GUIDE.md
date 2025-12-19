# Complete Step-by-Step Guide: Upload ADEGuard Project to GitHub

This guide walks you through uploading your 10GB+ project to GitHub using Git LFS for large files.

---

## PREREQUISITE: Install Required Tools

### 1. Install Git (if not already installed)
- Download from: https://git-scm.com/download/win
- Run the installer with default settings
- Verify installation:
```cmd
git --version
```

### 2. Install Git LFS (Large File Storage)
- Download from: https://git-lfs.github.com/
- Run the installer
- Or use Chocolatey (if installed):
```cmd
choco install git-lfs
```
- Verify installation:
```cmd
git lfs --version
```

### 3. Have a GitHub Account
- Go to https://github.com/join if you don't have one
- Create and verify your account

---

## STEP 1: Clean Up Your Project (Remove Unnecessary Large Files)

These virtual environments and cache files take up 3-5GB and can be recreated on any machine.

### 1.1: Remove Virtual Environments

Open Command Prompt and run:

```cmd
cd c:\all-codes\temp_ade_guard
```

Remove backend virtual environment:
```cmd
rmdir /s /q adeguard_backend\venv
```
- Type `Y` and press Enter when prompted to confirm
- This removes the entire venv folder (~2-3GB)

Remove Streamlit virtual environment:
```cmd
rmdir /s /q adeguard_streamlit_dashboard\streamlit_venv
```
- Type `Y` and press Enter when prompted to confirm

### 1.2: Remove Python Cache Files

Remove all `__pycache__` folders:
```cmd
for /d /r . %d in (__pycache__) do @if exist "%d" rmdir /s /q "%d"
```
- This recursively finds and removes all Python cache directories

Remove pytest cache:
```cmd
rmdir /s /q adeguard_backend\tests\.pytest_cache 2>nul
```
- The `2>nul` suppresses errors if the folder doesn't exist

### 1.3: (Optional) Remove Logs

If logs are not important:
```cmd
rmdir /s /q adeguard_backend\logs
```

### Current Size After Cleanup
Your project should now be around **6-7GB** (down from 10GB+)

---

## STEP 2: Create `.gitignore` File

The `.gitignore` file tells Git which files to ignore (not upload).

### 2.1: Create the File

Using Notepad:
```cmd
cd c:\all-codes\temp_ade_guard
notepad .gitignore
```

A Notepad window will open.

### 2.2: Copy and Paste This Content

```
# ========== Virtual Environments ==========
venv/
env/
ENV/
streamlit_venv/
.venv/

# ========== Python Cache ==========
__pycache__/
*.py[cod]
*$py.class
*.egg-info/
*.egg
dist/
build/
.eggs/

# ========== Testing ==========
.pytest_cache/
.coverage
htmlcov/
.tox/

# ========== IDE and Editors ==========
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store
Thumbs.db
*.sublime-project
*.sublime-workspace

# ========== Logs and Temporary Files ==========
logs/
*.log
.log/
tmp/
temp/

# ========== Environment Variables ==========
.env
.env.local
.env.*.local

# ========== OS Files ==========
.DS_Store
Thumbs.db
desktop.ini

# ========== Jupyter Notebooks ==========
.ipynb_checkpoints/
*.ipynb_checkpoints

# ========== MacOS ==========
.AppleDouble
.LSOverride

# ========== Node (if applicable) ==========
node_modules/
npm-debug.log
```

### 2.3: Save and Close

- Press `Ctrl + S` to save
- Close Notepad

---

## STEP 3: Initialize Git LFS

Git LFS handles large files separately to keep your repository fast.

### 3.1: Initialize Git LFS in Your Project

```cmd
cd c:\all-codes\temp_ade_guard
git lfs install
```

You should see:
```
Git LFS initialized.
```

### 3.2: Configure Which File Types Should Use Git LFS

This tells Git LFS to track these large files:

```cmd
git lfs track "*.safetensors"
git lfs track "*.bin"
git lfs track "*.pt"
git lfs track "*.pth"
git lfs track "*.npy"
git lfs track "*.csv"
git lfs track "*.pkl"
git lfs track "*.joblib"
```

### 3.3: Verify `.gitattributes` File Was Created

```cmd
type .gitattributes
```

You should see output similar to:
```
*.safetensors filter=lfs diff=lfs merge=lfs -text
*.bin filter=lfs diff=lfs merge=lfs -text
*.npy filter=lfs diff=lfs merge=lfs -text
*.csv filter=lfs diff=lfs merge=lfs -text
```

---

## STEP 4: Initialize Git Repository

### 4.1: Initialize Git

```cmd
cd c:\all-codes\temp_ade_guard
git init
```

You should see:
```
Initialized empty Git repository in c:\all-codes\temp_ade_guard\.git\
```

### 4.2: Configure Git User (First Time Only)

Tell Git who you are:

```cmd
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

Example:
```cmd
git config --global user.name "John Doe"
git config --global user.email "john.doe@gmail.com"
```

### 4.3: Add All Files to Git

```cmd
cd c:\all-codes\temp_ade_guard
git add .
```

This stages all files for commit (respecting `.gitignore`).

### 4.4: Verify What Will Be Uploaded

```cmd
git status
```

You should see a list of files to be committed. Verify:
- Virtual environments are NOT listed
- `__pycache__` folders are NOT listed
- `.gitignore` and `.gitattributes` ARE listed

---

## STEP 5: Create Initial Commit

A commit is like a snapshot of your project.

### 5.1: Create the First Commit

```cmd
git commit -m "Initial commit: ADEGuard project with ML models, datasets, and Streamlit dashboard"
```

Wait for the command to complete. You'll see:
```
[main (root-commit) abc123d] Initial commit: ADEGuard project...
 XXX files changed, XXX insertions(+)
```

---

## STEP 6: Create GitHub Repository

### 6.1: Go to GitHub.com

- Open browser and go to https://github.com/new
- Or click your profile icon → "New repository"

### 6.2: Fill in Repository Details

**Repository name:** (required)
- Example: `adeguard-project` or `ade-guard`
- Use lowercase letters and hyphens

**Description:** (optional but recommended)
- Example: "ADEGuard: An AI-driven system for detecting adverse drug events using NER, clustering, and severity classification"

**Public or Private:**
- Select `Public` if you want others to see it
- Select `Private` if it's for personal use

**Initialize repository:**
- **IMPORTANT:** Leave all checkboxes UNCHECKED
  - Do NOT check "Add a README file"
  - Do NOT check "Add .gitignore"
  - Do NOT check "Choose a license"
  
(You already have these locally)

### 6.3: Create Repository

Click the green "Create repository" button.

### 6.4: Copy Your Repository URL

After creation, GitHub shows you a page with commands. Look for a line like:

```
https://github.com/YOUR_USERNAME/adeguard-project.git
```

Or via SSH:
```
git@github.com:YOUR_USERNAME/adeguard-project.git
```

**Copy the HTTPS URL** (easier for first-time users).

---

## STEP 7: Connect Local Repository to GitHub

### 7.1: Add Remote Repository

Paste your repository URL (replace with your actual URL):

```cmd
cd c:\all-codes\temp_ade_guard
git remote add origin https://github.com/YOUR_USERNAME/adeguard-project.git
```

Example:
```cmd
git remote add origin https://github.com/john-doe/adeguard-project.git
```

### 7.2: Verify Remote Was Added

```cmd
git remote -v
```

You should see:
```
origin  https://github.com/YOUR_USERNAME/adeguard-project.git (fetch)
origin  https://github.com/YOUR_USERNAME/adeguard-project.git (push)
```

### 7.3: Rename Branch to `main`

```cmd
git branch -M main
```

---

## STEP 8: Push to GitHub

### 8.1: Push Your Code

This is the big step! It uploads your project to GitHub.

```cmd
cd c:\all-codes\temp_ade_guard
git push -u origin main
```

### 8.2: Enter GitHub Credentials

If prompted, enter your GitHub username and password/token:

- **Username:** Your GitHub username
- **Password:** Your GitHub personal access token (or password if 2FA not enabled)

**To create a Personal Access Token:**
1. Go to https://github.com/settings/tokens
2. Click "Generate new token"
3. Give it a name: `GitHub Upload`
4. Check: `repo` (all), `read:user`, `user:email`
5. Click "Generate token"
6. Copy the token and use it as your password

### 8.3: Wait for Upload

The upload will take **10-30 minutes** depending on:
- Your internet speed
- Total project size
- Number of large files

You'll see progress:
```
Uploading LFS objects: 100% (145/145)
Enumerating objects: 1234, done.
Counting objects: 100% (1234/1234), done.
Delta compression using up to 8 threads
Compressing objects: 100% (890/890), done.
Writing objects: 100% (1234/1234), 2.5 GiB | 1.2 MiB/s, done.
```

### 8.4: Verify Upload Success

After completion, you'll see:
```
* [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

---

## STEP 9: Verify on GitHub

### 9.1: Go to Your Repository

Open your browser and go to:
```
https://github.com/YOUR_USERNAME/adeguard-project
```

### 9.2: Check Files Are There

You should see:
- `adeguard_backend/` folder
- `adeguard_streamlit_dashboard/` folder
- Model folders (`saved_models/`, `biobert_ner_adeguard/`)
- Dataset folders
- `requirements.txt` files
- `.gitignore` and `.gitattributes`

### 9.3: Check LFS Files

Go to your repository and you should see files marked with a small "LFS" badge next to large files like:
- `.safetensors`
- `.npy`
- `.csv`

---

## STEP 10: Create Supporting Documentation Files

These files help other developers use your project.

### 10.1: Create `.env.example`

This shows what environment variables are needed (without real secrets).

Create file `c:\all-codes\temp_ade_guard\.env.example`:

```cmd
cd c:\all-codes\temp_ade_guard
notepad .env.example
```

Paste this content:

```
# ========== Backend API Configuration ==========
API_HOST=localhost
API_PORT=8000
DEBUG=True

# ========== Database (if using) ==========
DATABASE_URL=sqlite:///./test.db

# ========== Model Paths ==========
NER_MODEL_PATH=./biobert_ner_adeguard
CLUSTERING_MODEL_PATH=./saved_models/clustering_model
SEVERITY_MODEL_PATH=./saved_models/severity_model
EXPLAINABILITY_MODEL_PATH=./saved_models/explainability_models

# ========== API Keys (if needed) ==========
API_KEY=your_api_key_here
SECRET_KEY=your_secret_key_here

# ========== Logging ==========
LOG_LEVEL=INFO
LOG_FILE=./logs/app.log
```

Save and close.

### 10.2: Create `SETUP.md` (Installation Guide)

Create file `c:\all-codes\temp_ade_guard\SETUP.md`:

```cmd
notepad SETUP.md
```

Paste this content:

```markdown
# ADEGuard Setup Guide

## Prerequisites

- Python 3.8+
- Git
- Git LFS (for large model files)

## Installation

### 1. Clone the Repository

\`\`\`bash
git clone https://github.com/YOUR_USERNAME/adeguard-project.git
cd adeguard-project
\`\`\`

### 2. Pull LFS Files

\`\`\`bash
git lfs pull
\`\`\`

### 3. Setup Backend

\`\`\`bash
cd adeguard_backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
\`\`\`

### 4. Setup Streamlit Dashboard

In a new terminal:

\`\`\`bash
cd adeguard_streamlit_dashboard
python -m venv streamlit_venv
streamlit_venv\Scripts\activate
pip install -r requirements.txt
\`\`\`

## Running the Project

### Terminal 1: Run Backend API

\`\`\`bash
cd adeguard_backend
venv\Scripts\activate
uvicorn app.main:app --reload
\`\`\`

Backend will be available at: http://localhost:8000

### Terminal 2: Run Streamlit Dashboard

\`\`\`bash
cd adeguard_streamlit_dashboard
streamlit_venv\Scripts\activate
streamlit run app.py
\`\`\`

Streamlit will open at: http://localhost:8501

## API Documentation

Once backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

- `adeguard_backend/` - FastAPI backend with ML models
- `adeguard_streamlit_dashboard/` - Streamlit web UI
- `saved_models/` - Trained model weights
- `biobert_ner_adeguard/` - BioBERT NER model
- `datasets/` - VAERS data
- `clustering_embeddings/` - Embedding data
```

Save and close.

### 10.3: Commit and Push Documentation

```cmd
cd c:\all-codes\temp_ade_guard
git add .env.example SETUP.md
git commit -m "Add documentation files: environment template and setup guide"
git push origin main
```

---

## STEP 11: Update README.md (If Needed)

### 11.1: Check Current README

```cmd
type README.md
```

### 11.2: Add Installation Instructions

Edit your `README.md` to include the setup instructions from `SETUP.md` (or link to it).

### 11.3: Commit Updates

```cmd
git add README.md
git commit -m "Update README with installation and setup instructions"
git push origin main
```

---

## TROUBLESHOOTING

### Issue 1: "fatal: Not a git repository"

**Solution:**
```cmd
cd c:\all-codes\temp_ade_guard
git init
```

### Issue 2: "error: pathspec '.gitignore' did not match any files"

**Solution:** You haven't created `.gitignore` yet. Do Step 2 first.

### Issue 3: "Authentication failed" during push

**Solution:**
- Use a Personal Access Token instead of password
- Or set up SSH keys (more advanced)

### Issue 4: Push is very slow or times out

**Solution:**
- Check internet connection
- Try:
```cmd
git config --global http.postBuffer 524288000
git config --global http.maxRequestBuffer 52428800
```

### Issue 5: "LFS pointer is not a valid file"

**Solution:** Run this before pushing:
```cmd
git lfs migrate import --include="*.safetensors,*.npy,*.csv,*.bin"
```

### Issue 6: File shows as "This file is stored with Git LFS" but is blank

**Solution:** The user needs to:
```cmd
git lfs pull
```

after cloning.

---

## AFTER UPLOAD: Sharing Your Project

### Share Repository Link

Your project is now at:
```
https://github.com/YOUR_USERNAME/adeguard-project
```

### For Collaborators to Clone

```cmd
git clone https://github.com/YOUR_USERNAME/adeguard-project.git
cd adeguard-project
git lfs pull
```

### Add Collaborators (Private Repo)

1. Go to repository Settings
2. Click "Collaborators" (Manage access)
3. Click "Add people"
4. Enter their GitHub username

---

## STEP-BY-STEP QUICK REFERENCE

```cmd
REM 1. Clean up
cd c:\all-codes\temp_ade_guard
rmdir /s /q adeguard_backend\venv adeguard_streamlit_dashboard\streamlit_venv

REM 2. Create .gitignore (use notepad, copy content from Step 2)

REM 3. Initialize LFS
git lfs install
git lfs track "*.safetensors" "*.bin" "*.npy" "*.csv"

REM 4. Initialize git repo
git init
git config --global user.name "Your Name"
git config --global user.email "your.email@gmail.com"
git add .
git status

REM 5. Create commit
git commit -m "Initial commit: ADEGuard project"

REM 6. Create repo on GitHub.com
REM (Go to https://github.com/new)

REM 7. Connect and push
git remote add origin https://github.com/YOUR_USERNAME/adeguard-project.git
git branch -M main
git push -u origin main

REM 8. Add documentation
REM (Create .env.example and SETUP.md)
git add .env.example SETUP.md
git commit -m "Add documentation"
git push origin main
```

---

## FINAL CHECKLIST

- [ ] Installed Git
- [ ] Installed Git LFS
- [ ] Removed virtual environments
- [ ] Created `.gitignore`
- [ ] Initialized Git LFS
- [ ] Created git repository locally
- [ ] Added all files
- [ ] Created initial commit
- [ ] Created GitHub repository
- [ ] Pushed to GitHub
- [ ] Verified files on GitHub
- [ ] Created `.env.example`
- [ ] Created `SETUP.md`
- [ ] Updated `README.md`
- [ ] All documentation files pushed

**You're done!** Your project is now on GitHub!

---

## NEXT STEPS

1. **Invite collaborators** (if working with others)
2. **Set up GitHub Actions** (automated testing/CI-CD)
3. **Create releases** (version your project)
4. **Add issue templates** (for bug reports)
5. **Create pull request templates** (for contributions)

Refer to GitHub documentation for these advanced features.
