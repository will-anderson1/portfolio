#!/bin/bash

# Load environment variables from .env file
if [ -f .env.local ]; then
    export $(cat .env.local | grep -v '^#' | xargs)
fi

# Set default ports if not defined in .env
BACKEND_PORT=${BACKEND_PORT:-5050}
FRONTEND_PORT=${FRONTEND_PORT:-3000}

echo "=== News Aggregation System Status ==="
echo ""

# Check if PID files exist and processes are running
if [ -f .backend.pid ]; then
    BACKEND_PID=$(cat .backend.pid)
    if kill -0 $BACKEND_PID 2>/dev/null; then
        echo "✅ FastAPI Backend: Running (PID: $BACKEND_PID)"
        
        # Check if backend is responding
        if curl -s http://localhost:$BACKEND_PORT/api/stats > /dev/null 2>&1; then
            echo "✅ Backend API: Responding"
            
            # Get stats from backend
            STATS=$(curl -s http://localhost:$BACKEND_PORT/api/stats 2>/dev/null)
            if [ $? -eq 0 ]; then
                echo "📊 Active Events: $(echo $STATS | grep -o '"active_articles":[0-9]*' | cut -d: -f2)"
                echo "📊 Total Articles: $(echo $STATS | grep -o '"total_articles":[0-9]*' | cut -d: -f2)"
            fi
        else
            echo "❌ Backend API: Not responding"
        fi
    else
        echo "❌ FastAPI Backend: Not running (stale PID file)"
    fi
else
    echo "❌ FastAPI Backend: Not started"
fi

echo ""

if [ -f .frontend.pid ]; then
    FRONTEND_PID=$(cat .frontend.pid)
    if kill -0 $FRONTEND_PID 2>/dev/null; then
        echo "✅ Next.js Frontend: Running (PID: $FRONTEND_PID)"
        
        # Check if frontend is responding
        if curl -s http://localhost:$FRONTEND_PORT > /dev/null 2>&1; then
            echo "✅ Frontend: Responding"
        else
            echo "❌ Frontend: Not responding"
        fi
    else
        echo "❌ Next.js Frontend: Not running (stale PID file)"
    fi
else
    echo "❌ Next.js Frontend: Not started"
fi

echo ""

# Check recent log activity
echo "=== Recent Activity ==="
if [ -f backend.log ]; then
    echo "📝 Backend Log (last 5 lines):"
    tail -5 backend.log | sed 's/^/  /'
else
    echo "📝 Backend Log: No log file found"
fi

echo ""

if [ -f frontend.log ]; then
    echo "📝 Frontend Log (last 3 lines):"
    tail -3 frontend.log | sed 's/^/  /'
else
    echo "📝 Frontend Log: No log file found"
fi

echo ""
echo "=== Quick Commands ==="
echo "Start: ./start.sh"
echo "Stop:  ./stop.sh"
echo "Status: ./status.sh"
echo "Manual Aggregation: curl -X POST http://localhost:$BACKEND_PORT/api/aggregate" 