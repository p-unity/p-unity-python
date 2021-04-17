@echo off
del build\*.* /F /Q /S /Y 2> nul
python setup.py clean
python setup.py install
python smoke_0.py
python smoke_1.py
