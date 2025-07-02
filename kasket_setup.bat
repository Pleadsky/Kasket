@echo off
color 0A
echo ----------------------------------------
echo       Kasket Script Installer
echo ----------------------------------------

echo.
echo KASKET SCRIPT MANUAL:
echo ---------------------
echo COMMANDS:
echo PRINT "text"        - Display message
echo INPUT "text" TO &var - Store user input
echo COLOR number        - Change text color (1-50)
echo DELAY{time.Xunit}   - Pause execution (units: sec/min/hour/day)
echo END                 - Required at end of every script
echo.
echo EXAMPLE USAGE:
echo PRINT "Hello World!"
echo INPUT "Enter name:" TO &NAME
echo PRINT "Hello &NAME!"
echo DELAY{time.2sec}
echo END
echo.
echo Thank you for choosing Kasket Script!
echo Press any key to begin installation...
pause >nul

:: Create Kasket runner
echo @echo off > kasket.bat
echo if "%%~1"=="" ( >> kasket.bat
echo     echo Error: No script specified >> kasket.bat
echo     echo Drag .kasket file onto me >> kasket.bat
echo     pause >> kasket.bat
echo     exit /b 1 >> kasket.bat
echo ) >> kasket.bat
echo python "%%~dp0kasket_interpreter.py" "%%1" >> kasket.bat
echo pause >> kasket.bat

:: Create sample script
echo PRINT "Welcome to Kasket Script!" > test.kasket
echo INPUT "Enter your name:" TO ^&NAME >> test.kasket
echo PRINT "Hello ^&NAME!" >> test.kasket
echo DELAY{time.2sec} >> test.kasket
echo END >> test.kasket

:: Create script wizard
echo @echo off > create_kasket.bat
echo setlocal enabledelayedexpansion >> create_kasket.bat
echo :start >> create_kasket.bat
echo cls >> create_kasket.bat
echo -------------------------------
echo     Kasket Script Creator
echo -------------------------------
echo echo. >> create_kasket.bat
echo set /p filename=Enter script name: >> create_kasket.bat
echo if not "%%filename:~-7%%"==".kasket" set filename=%%filename%%.kasket >> create_kasket.bat
echo echo PRINT "Your script" > "%%filename%%" >> create_kasket.bat
echo echo END >> "%%filename%%" >> create_kasket.bat
echo notepad "%%filename%%" >> create_kasket.bat
echo exit >> create_kasket.bat

:: Register association
reg add "HKCU\Software\Classes\.kasket" /ve /d "KasketScript" /f
reg add "HKCU\Software\Classes\KasketScript\shell\open\command" /ve /t REG_SZ /d "\"%~dp0kasket.bat\" \"%%1\"" /f

echo - Success! Created:
echo - kasket.bat (runner)
echo - test.kasket (sample)
echo - create_kasket.bat (wizard)
echo.
echo Double-click test.kasket to try it!
pause