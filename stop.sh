#!/bin/bash

# Load environment variables from .env file
if [ -f .env.local ]; then
    export $(cat .env.local | grep -v '^#' | xargs)
fi

echo "Stopping services..."

if [ -f .backend.pid ]; then
  BACKEND_PID=$(cat .backend.pid)
  echo "Stopping FastAPI backend (PID: $BACKEND_PID)..."
  
  # Send SIGTERM for graceful shutdown
  kill -TERM $BACKEND_PID
  
  # Wait for graceful shutdown (up to 10 seconds)
  for i in {1..10}; do
    if ! kill -0 $BACKEND_PID 2>/dev/null; then
      echo "FastAPI backend stopped gracefully"
      break
    fi
    sleep 1
  done
  
  # Force kill if still running
  if kill -0 $BACKEND_PID 2>/dev/null; then
    echo "Force killing FastAPI backend..."
    kill -KILL $BACKEND_PID
  fi
  
  rm .backend.pid
fi

if [ -f .frontend.pid ]; then
  FRONTEND_PID=$(cat .frontend.pid)
  echo "Stopping Next.js frontend (PID: $FRONTEND_PID)..."
  kill $FRONTEND_PID && echo "Next.js frontend stopped"
  rm .frontend.pid
fi

echo "All services stopped."
