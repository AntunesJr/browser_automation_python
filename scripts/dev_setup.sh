#!/bin/bash
# Setup local development environment

echo "Creating Python virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

echo "Upgrading pip and setuptools..."
pip install --upgrade pip setuptools
pip install selenium
pip install pynput
pip install pyttsx3
pip install pyaudio

pip install vosk numpy soundfile
wget https://huggingface.co/Derur/vosk-stt-models/resolve/main/vosk-model-pt.7z
7z x vosk-model-pt.7z -o"vosk-model-pt

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Installing package in editable mode..."
pip install -e .

echo "Environment setup complete!"
echo "Activate with: source .venv/bin/activate"