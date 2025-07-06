#!/bin/bash

# Load environment variables from .env file
if [ -f .env.local ]; then
    export $(cat .env.local | grep -v '^#' | xargs)
fi

# Set default ports if not defined in .env
BACKEND_PORT=${BACKEND_PORT:-5050}
FRONTEND_PORT=${FRONTEND_PORT:-3000}

echo "Starting news aggregation system..."

# Start FastAPI backend
cd backend
source venv/bin/activate
echo "Starting FastAPI backend on port $BACKEND_PORT..."
echo "Note: News aggregator scheduler will start automatically with the backend"
uvicorn main:app --reload --port $BACKEND_PORT > ../backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# Start Next.js frontend
cd frontend
echo "Starting Next.js frontend on port $FRONTEND_PORT..."
npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

# Save PIDs
echo $BACKEND_PID > .backend.pid
echo $FRONTEND_PID > .frontend.pid

echo "Both servers are running."
echo "Backend: http://localhost:$BACKEND_PORT"
echo "Frontend: http://localhost:$FRONTEND_PORT"
echo ""
echo "The news aggregator scheduler is running in the background and will:"
echo "- Aggregate news every 15 minutes"
echo "- Process articles with LLM for event compilation"
echo "- Maintain up to 12 active events"
echo "- Deactivate events older than 2 days"
echo ""
echo "Check backend.log for aggregator activity and any errors."
