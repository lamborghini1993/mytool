@echo off

set codepath=%~dp0%
set toolpath=%codepath%..\mytool

mklink /j %codepath%mytool %toolpath%
pause