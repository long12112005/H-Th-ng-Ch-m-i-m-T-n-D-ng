@echo off
if exist .venv\Scripts\activate call .venv\Scripts\activate
python -m pytest -q
pause
