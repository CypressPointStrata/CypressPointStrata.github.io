REM To switch user on Windows:
git config --global user.name CypressPointStrata
git config --global user.email cypressnw2050@gmail.com
REM YOU MIGHT HAVE TO WAIT A WHILE IF SWITCHING USERS
REM Might have to do this too:
REM Control Panel >> User Account >> Credential Manager >> Windows Credential >> Git Credential
REM or from cmd prompt: rundll32.exe keymgr.dll, KRShowKeyMgr
REM remove git credentials.
REM next time when you'll push repo it'll ask you for credential.
git add --all
git commit -m "update"
git push -u origin master
