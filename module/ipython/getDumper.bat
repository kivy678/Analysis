@echo off

echo Start getDumper.py localhost 22222 %1 %2

::				 il2cppFunc HOST PORT PID SAVE_PATH
idat.exe -t -B -S"%cd%\module\ipython\getDumper.py localhost 22222 %1 %2"

echo End Processing...
::pause
