Set WshShell = CreateObject("WScript.Shell")
cmdStr = ".venv\Scripts\activate.bat & python main.py"
WshShell.Run cmdStr, 0
Set WshShell = Nothing