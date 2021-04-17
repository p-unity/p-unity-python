@echo off
python setup_pypi.py sdist bdist_wheel
python -m twine upload dist/*
