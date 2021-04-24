@echo off
:main
cls
q p_unity\FORTH.py p_unity\WORDS\F_CORE.py p_unity\WORDS\*.py p_unity\*.py
rem python -m cProfile -s ncalls forth.py | list /s
python forth.py
if errorlevel 1 goto end
goto main
:end
