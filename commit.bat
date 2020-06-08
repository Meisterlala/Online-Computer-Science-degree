@echo off
echo --------------------------------------
echo git pull
git pull
echo --------------------------------------
echo git add .
git add .
echo --------------------------------------
echo git status
git status
echo --------------------------------------
set /p temp="Comit Message: "
echo --------------------------------------
echo commit -a -m "%temp%" -m "Script commit"
git commit -a -m "%temp%" -m "Script commit" 
echo --------------------------------------
echo git push
git push
echo --------------------------------------
pause