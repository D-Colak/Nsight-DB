taskkill /F /IM uvicorn.exe
taskkill /F /IM sqlite_web.exe
del database.db
start "" .venv\Scripts\activate
start "" uvicorn main:app --reload
start "" sqlite_web database.db
