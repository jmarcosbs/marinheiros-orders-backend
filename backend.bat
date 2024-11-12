@echo off
cd %~dp0marinheiros-orders-backend
call .\venv\Scripts\activate
cd .\marinheirosorders
python manage.py runserver 0.0.0.0:8000