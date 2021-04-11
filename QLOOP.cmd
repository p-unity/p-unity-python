@echo off
:main
q p_unity\FORTH.py p_unity\f*.py p_unity\*.py
python ide.py
if errorlevel 1 goto end
goto main
:end
