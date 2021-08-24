@echo off

ver | find "5.1" > nul

if "%errorlevel%" == "0" goto xp
if "%errorlevel%" == "1" goto run


:run
where python
if "%errorlevel%" == "0" (
	python -m pip install --upgrade pip
	pip install virtualenv
	virtualenv .env
	%cd%\.env\Scripts\activate.bat
	pip install -r requirements.txt
	pause
    exit
) else (
	echo can't find python
	pause
    exit
)


:xp
echo XP...
pause
exit


