# Development Guide

This document walks you through setting up a **development environment** for the Financial‑Advisor project, so you can make changes, run the app in watch mode, and execute tests.

---

## 1. Prerequisites

- **Git** (to clone and branch the repo)
- **Node.js** ≥ 18 and **npm** (for the frontend)
- **Python** ≥ 3.11 and **pip** (for the backend)
- *(Optional but recommended)* **VS Code** or your favorite editor
- *(Optional)* **Docker** (to spin up services in containers)

---

## 2. Clone the Repository

```bash
# Clone the main repo and enter it
git clone https://github.com/TCarlson29/Financial-Advisor.git
cd Financial-Advisor
```

Branch off `main` for your work:

```bash
git checkout -b feature/<your-feature-name>
```

---

## 3. Backend Setup (Local Python)

1. **Create a virtual environment** in the `backend/` folder:
   ```bash
   cd backend
   python3 -m venv .venv
   ```
2. **Activate the venv**:
   - PowerShell: `.\.venv\Scripts\Activate.ps1`  
   - CMD:       `.\.venv\Scripts\activate.bat`  
   - Bash:      `source .venv/bin/activate`
3. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the backend in reload mode from the root directoy**:
   ```bash
   cd .. # If currently in /backend
   uvicorn backend.main:app --reload --port 8000
   ```

The FastAPI server will now reload on file changes at **http://localhost:8000**.

---

## 4. Frontend Setup (Vue)

1. **Open a new terminal** and make sure you’re in the repo root:
   ```bash
   cd frontend
   ```
2. **Install npm packages**:
   ```bash
   npm install
   ```
3. **Run the dev server from the root directory**:
   ```bash
   cd .. # If currently in /frontend
   npm run frontend:dev 
   ```

Vite will start the hot‑reload server on **http://localhost:5173**.

---
