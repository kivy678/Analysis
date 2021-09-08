@echo off

echo Start Analysis "%cd%\module\ipython\convES\%1 %2 %3" %4

::				script md5 DATA_PATH lib_path
idat.exe -c -A -S"%cd%\module\ipython\convES\%1 %2 %3" %4

echo End Processing...
::pause
exit
