$ErrorActionPreference = 'Stop'

py -3.11 -m pip install --upgrade pip
py -3.11 -m pip install -r requirements.txt
py -3.11 -m pip install pyinstaller==6.11.1
py -3.11 -m PyInstaller -wF --icon=oscicon.ico --clean --add-data "oct_app/templates;oct_app/templates" --add-data "oct_app/static;oct_app/static" osc-chat-tools.py
