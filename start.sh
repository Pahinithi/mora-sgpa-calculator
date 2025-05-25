#!/bin/bash

# Add the current directory to PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Start FastAPI in the background
echo "Starting FastAPI..."
uvicorn app.main:app --reload &

# Start Streamlit (in foreground)
echo "Starting Streamlit..."
streamlit run app/frontend/streamlit_app.py
