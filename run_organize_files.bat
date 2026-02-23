@echo off
REM Launcher for organize_files.py — double-click to run
setlocal
set SCRIPT_DIR=%~dp0
pushd "%SCRIPT_DIR%"
if exist "%SCRIPT_DIR%organize_files.py" (
    where py >nul 2>&1 && (py "%SCRIPT_DIR%organize_files.py" %* & goto :eof)
    where python >nul 2>&1 && (python "%SCRIPT_DIR%organize_files.py" %* & goto :eof)
    echo Python not found. Install Python or add it to PATH.
    pause
) else (
    echo organize_files.py not found in this folder.
    pause
)
popd
endlocal
