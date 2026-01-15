Add-Type -AssemblyName System.Windows.Forms
Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
public class WinAPI {
    [DllImport("user32.dll")]
    public static extern bool SetForegroundWindow(IntPtr hWnd);
}
"@

# Get the handle for Notepad
$process = Get-Process kicad
if ($process -and $process.MainWindowHandle -ne [IntPtr]::Zero) {
    [WinAPI]::SetForegroundWindow($process.MainWindowHandle)
}
