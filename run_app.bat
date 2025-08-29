@echo off
echo Starting G.Writer...

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Install requirements
echo Installing dependencies...
pip install -r requirements.txt

REM Install additional required packages
echo Installing PyAutoGUI and pynput...
pip install pyautogui pynput

REM Run the application
echo Starting G.Writer application...
python g_writer.py

pause