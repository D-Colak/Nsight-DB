this is a database written in SQLite that is intended to integrate with a fastAPI backend for the Nsight Chemformations Project. The database is SQLite and is connected via SQLModel and SQLAlchemy.

# Requirements
- Python 3.10 or higher

# Usage
1. Clone the repository:
   ```bash
   git clone https://github.com/D-Colak/Nsight-DB.git
   ```

2. Navigate to the project directory:
   ```bash
    cd Nsight-DB
    ```

3. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv .venv
   ```

   For MacOS/Linux:
   ```bash
    source .venv/bin/activate
    ```

    For Windows:
    ```bash
    .venv\Scripts\activate
    ```
4. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

5. Start the FastAPI server:
    ```bash
    uvicorn main:app --reload
    ```

6. Access the endpoints and documentation at http://localhost:8000/docs

7. View the database in real time with this command:
   ```bash
   sqlite_web database.db
   ```