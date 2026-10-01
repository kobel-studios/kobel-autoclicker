' Launches Auto-Clicker Hub with no console window (uses pythonw.exe).
Set shell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)
pyScript = fso.BuildPath(scriptDir, "autoclicker_hub.py")

' Prefer pythonw on PATH; fall back to the known install location.
pythonw = "pythonw.exe"

shell.Run """" & pythonw & """ """ & pyScript & """", 0, False
