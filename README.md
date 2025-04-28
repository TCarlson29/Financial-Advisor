# Financial-Advisor

To use: 
download venv
at root, activate .venv: .\.venv\Scripts\activate.bat
(only once needed for every run now and future) pip install -r requirements.txt

cd backend, then 'uvicorn main:app --reload'
new terminal, cd frontend, and 'npm run dev'
visit: http://localhost:5173

database usage:
python database.py or python backend/database.py