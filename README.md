# Financial-Advisor

To use: 
download venv:
    Windows: py -3 -m venv .venv
    IOS: python -m venv .venv

at root, activate .venv: 
powershell: .\.venv\Scripts\activate.bat
Bash/WSL: source .venv/bin/activate
(change Scripts/bin with the other as needed based on which folder has the activate file)

(only once needed for every run now and future) pip install -r backend/requirements.txt

cd backend, then 'uvicorn main:app --reload'
install npm and update it
new terminal, cd frontend, and 'npm run dev'
visit: http://localhost:5173

database usage:
python database.py or python backend/database.py