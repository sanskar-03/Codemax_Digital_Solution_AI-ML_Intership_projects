@echo off
.venv\Scripts\celery.exe -A config worker -l info
