@echo off
setlocal

py -3.11 -m pip install --upgrade pip
py -3.11 -m pip install -r requirements.txt
py -3.11 -m pip install pyinstaller==6.11.1
py -3.11 -m PyInstaller -wD --icon=oscicon.ico --clean osc-chat-tools.py

endlocal
