@echo off
call .\venv\Scripts\activate
cd .\marinheirosorders
python manage.py runserver 0.0.0.0:8000