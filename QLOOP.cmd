@echo off
:main
cls
q p_unity\FORTH.py p_unity\STD\*.py p_unity\*.py
python ide.py
if errorlevel 1 goto end
goto main
:end
