@echo off
title Push Crime Project to GitHub
cd /d "C:\Users\bbone\Downloads\crime_project\crime_project"
echo =======================================================
echo Pushing project to https://github.com/varshithBoneni/crime-_project
echo =======================================================
echo.
git push -u origin main
echo.
echo =======================================================
if %ERRORLEVEL% EQU 0 (
    echo [SUCCESS] Project successfully pushed to GitHub!
) else (
    echo [ERROR] Push failed. Check your GitHub permissions or sign-in.
)
echo =======================================================
pause
