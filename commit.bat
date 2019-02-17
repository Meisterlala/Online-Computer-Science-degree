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
echo commit -a -m "Script commit" -m "%temp%"
git commit -a -m "Script commit" -m "%temp%"
echo --------------------------------------
echo git push
git push
echo --------------------------------------
pause