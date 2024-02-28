@echo off
setlocal enabledelayedexpansion

REM Prompt for the starting number
set /p start_number="Enter the starting number: "

REM List up jpg files in the current folder
for %%F in (*.jpg) do (
    REM Rename the file
    ren "%%F" "!start_number!.jpg"
    REM Increment the starting number
    set /a start_number+=1
)

echo The operation is complete.
pause