#!/bin/bash

trap 'kill $(jobs -p)' EXIT

echo "Starting backend..."
source venv/bin/activate
uvicorn src.api.api:app --reload &

echo "Starting frontend..."
cd frontend
npm run dev &

wait
