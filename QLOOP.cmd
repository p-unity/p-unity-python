@echo off
:main
cls
q p_unity\FORTH.py p_unity\BASIC.py p_unity\CORE\*.py p_unity\*.py
python forth.py
if errorlevel 1 goto end
goto main
:end
