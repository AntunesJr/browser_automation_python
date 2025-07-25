#!/bin/bash
# Setup local development environment

echo "Creating Python virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

echo "Upgrading pip and setuptools..."
pip install --upgrade pip setuptools

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Installing package in editable mode..."
pip install -e .

echo "Environment setup complete!"
echo "Activate with: source .venv/bin/activate"