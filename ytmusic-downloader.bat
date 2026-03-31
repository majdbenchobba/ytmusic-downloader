@echo off
title YouTube Music High Quality Downloader
setlocal enabledelayedexpansion

set "SCRIPT_DIR=%~dp0"
set "AUTO_UPDATE_YTDLP=1"

:: Set save folder
set "SAVE_DIR=C:\Users\%USERNAME%\Desktop\High Quality"
if not exist "%SAVE_DIR%" mkdir "%SAVE_DIR%"

:menu
cls
echo ============================================
echo    YouTube Music Downloader (WAV Format)
echo    Files will be saved in:
echo    %SAVE_DIR%
echo ============================================
echo.

set /p URL=Paste the YouTube Music link here: 
if "%URL%"=="" goto end

:: Prefer the local yt-dlp.exe next to this script, otherwise fall back to PATH
if exist "%SCRIPT_DIR%yt-dlp.exe" (
  if "%AUTO_UPDATE_YTDLP%"=="1" "%SCRIPT_DIR%yt-dlp.exe" -U
  "%SCRIPT_DIR%yt-dlp.exe" -o "%SAVE_DIR%\%%(artist)s - %%(title)s.%%(ext)s" -x --audio-format wav --audio-quality 0 "%URL%"
) else (
  if "%AUTO_UPDATE_YTDLP%"=="1" yt-dlp -U
  yt-dlp -o "%SAVE_DIR%\%%(artist)s - %%(title)s.%%(ext)s" -x --audio-format wav --audio-quality 0 "%URL%"
)

echo.
choice /m "Download another track?"
if errorlevel 2 goto end
if errorlevel 1 goto menu

:end
echo.
echo Goodbye! Closing...
timeout /t 2 >nul
exit
