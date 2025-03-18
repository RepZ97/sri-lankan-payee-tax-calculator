@echo off
echo Installing dependencies...
pip install -r requirements.txt

echo Building executable...
pyinstaller --onefile --windowed --icon=gc_icon.ico --name=GovernmentsCut main.py

echo Build complete! Find your .exe in the 'dist' folder.
pause
