@echo off
:main
cls
rem q p_unity\FORTH.py p_unity\WORDS\F_CORE.py p_unity\WORDS\*.py p_unity\*.py
q test.uni.md p_unity\BASIC.py p_unity\FORTH.py p_unity\SCRPT.py p_unity\UNITY.py p_unity\WORDS\F_CORE.py p_unity\WORDS\*.py p_unity\*.py
rem python -m cProfile -s ncalls forth.py | list /s
rem python basic.py
python unity.py -f test.uni.md
pause
if errorlevel 1 goto end
goto main
:end
