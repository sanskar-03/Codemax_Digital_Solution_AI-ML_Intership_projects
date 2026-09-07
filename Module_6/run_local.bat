@echo off

if not exist .env copy .env.example .env

.venv\Scripts\python.exe manage.py migrate

.venv\Scripts\python.exe manage.py runserver
