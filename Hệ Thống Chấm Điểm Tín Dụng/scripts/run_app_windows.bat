@echo off
if exist .venv\Scripts\activate call .venv\Scripts\activate
python -m streamlit run app.py
pause
