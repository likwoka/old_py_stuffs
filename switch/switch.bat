@echo off
set _d=
switch_.ipy %* > %TEMP%\__switch_pushd.tmp
set /p _d=<%TEMP%\__switch_pushd.tmp
del %TEMP%\__switch_pushd.tmp
if not _d=="" cd %_d%


