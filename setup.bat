@echo off
REM Setup and run script for Chinese Academic AI Study System (Windows)

echo =========================================
echo Chinese Academic AI Study System Setup
echo =========================================
echo.

REM Backend setup
echo 🔧 Setting up Backend...
cd backend

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating Python virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo ✓ Virtual environment ready

REM Install dependencies
echo 📥 Installing Python dependencies...
pip install -r requirements.txt -q

REM Initialize database
echo 📚 Initializing database...
python init_db.py

echo ✓ Backend setup complete!
echo.
echo To start backend server, run:
echo   cd backend
echo   venv\Scripts\activate
echo   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
echo.

REM Frontend setup
cd ..\frontend
echo 🔧 Setting up Frontend...
echo 📥 Installing npm dependencies...
call npm install -q

echo ✓ Frontend setup complete!
echo.
echo To start frontend development server, run:
echo   cd frontend
echo   npm start
echo.

echo =========================================
echo ✅ Setup Complete!
echo =========================================
echo.
echo Next steps:
echo 1. Start Backend: cd backend ^&^& python -m uvicorn app.main:app --reload
echo 2. Start Frontend: cd frontend ^&^& npm start
echo 3. Open http://localhost:3000 in your browser
echo.
pause
