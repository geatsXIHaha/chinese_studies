#!/bin/bash
# Setup and run script for Chinese Academic AI Study System

echo "========================================="
echo "Chinese Academic AI Study System Setup"
echo "========================================="
echo ""

# Backend setup
echo "🔧 Setting up Backend..."
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "✓ Virtual environment ready"

# Install dependencies
echo "📥 Installing Python dependencies..."
pip install -r requirements.txt -q

# Initialize database
echo "📚 Initializing database..."
python init_db.py

echo "✓ Backend setup complete!"
echo ""
echo "To start backend server, run:"
echo "  cd backend"
echo "  source venv/bin/activate  (macOS/Linux) or venv\\Scripts\\activate (Windows)"
echo "  python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
echo ""

# Frontend setup
cd ../frontend
echo "🔧 Setting up Frontend..."
echo "📥 Installing npm dependencies..."
npm install -q

echo "✓ Frontend setup complete!"
echo ""
echo "To start frontend development server, run:"
echo "  cd frontend"
echo "  npm start"
echo ""

echo "========================================="
echo "✅ Setup Complete!"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Start Backend: cd backend && uvicorn app.main:app --reload"
echo "2. Start Frontend: cd frontend && npm start"
echo "3. Open http://localhost:3000 in your browser"
echo ""
