@echo off
if exist .venv\Scripts\activate call .venv\Scripts\activate
python -m uvicorn api:app --reload --host 127.0.0.1 --port 8000
pause
