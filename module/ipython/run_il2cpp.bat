@echo off

echo Start il2cppFunc.py %1 %2 %3 %4 %5

::				 il2cppFunc jsonPath Script md5 DATA_PATH lib_path
idat.exe -c -A -S"%cd%\module\ipython\il2cppFunc.py %1 %2 %3 %4" %5

echo End Processing...
::pause
exit
