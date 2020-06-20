REM To switch user on Windows:
REM  Control Panel >> User Account >> Credential Manager >> Windows Credential >> Git Credential
REM remove git credential.
REM next time when you'll push repo it'll ask you for credential.
git config --global user.name "CypressPointStrata"
git config --global user.email "cypressnw2050@gmail.com"
git add --all
git commit -m "update"
git push -u origin master
