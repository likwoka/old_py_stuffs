''
' Recycle the particular Application Pool.
' We need to use this script because our servers are w2k3; once we upgrade
' to SP1, we can use iisapp.vbs /a appPoolName /r ...
' Reference: http://www.microsoft.com/technet/scriptcenter/scripts/iis/iis6/apps/i6apvb07.mspx 
' 2005 11 02
'
If WScript.Arguments.Count <> 1 Then
    WScript.Echo "Error: This script only takes 1 argument, no more no less!"
    WScript.Echo "Usage: cscript.exe apreset.vbs AppPoolName"
    WScript.Quit
End If
strAppPool = WScript.Arguments.Item(0)
'strAppPool = "MSSharePointAppPool"
strComputer = "."

WScript.Echo "Application Pool '" + "' is resetting... "

Set objWMIService = GetObject("winmgmts:{authenticationLevel=pktPrivacy}\\" & strComputer & "\root\microsoftiisv2")
Set colItems = objWMIService.ExecQuery("Select * From IIsApplicationPool Where Name = 'W3SVC/AppPools/" & strAppPool & "'")

For Each objItem in colItems
    objItem.Recycle
Next


WScript.Echo "Done."

