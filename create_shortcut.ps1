$WshShell = New-Object -ComObject WScript.Shell
$Desktop = [System.Environment]::GetFolderPath("Desktop")
$Shortcut = $WshShell.CreateShortcut("$Desktop\Kobel Autoclicker.lnk")
$Shortcut.TargetPath = "pythonw.exe"
$Shortcut.Arguments = '"' + (Join-Path $PSScriptRoot "autoclicker_hub.py") + '"'
$Shortcut.WorkingDirectory = $PSScriptRoot
$Shortcut.IconLocation = (Join-Path $PSScriptRoot "kobel_icon.ico") + ",0"
$Shortcut.Description = "Kobel Autoclicker"
$Shortcut.Save()
Write-Host "Autoclicker shortcut created"
