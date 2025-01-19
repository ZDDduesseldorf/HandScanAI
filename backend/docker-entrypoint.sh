#!/bin/bash

# Install new packages
echo "Install new packages"
pip install -r requirements.txt

# Run Server
echo "Run Server"
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload