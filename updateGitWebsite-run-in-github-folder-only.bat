REM To switch user on Windows:
REM see: https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-personal-account-on-github/managing-your-personal-account/managing-multiple-accounts
REM
git config --global user.name CypressPointStrata
git config --global user.email cypressnw2050@gmail.com
REM YOU MIGHT HAVE TO WAIT A WHILE IF SWITCHING USERS
REM Might have to do this too:
REM Control Panel >> User Accounts >> Manage your Credentials >> Windows Credential >> Git Credential
REM or from cmd prompt: rundll32.exe keymgr.dll, KRShowKeyMgr
REM remove git credentials.
REM next time when you'll push repo it'll ask you for credential.
REM
REM The GIT commands must be run in the GIT project home directory
cd "D:\UserFilesDdrive\Documents\Cypress Point\websiteGitHubCypressPointStrata\CypressPointStrata.github.io"
git add --all
git commit -m "update"
git push -u origin master
