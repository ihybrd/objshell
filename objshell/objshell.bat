@echo off

REM this is the revbot starter. 
:Main
REM call readconfig function to get the pyexec
set pyexec=none
set pymain=none
call :ReadConfig "etc/python.conf" "pyexec" pyexec
call :ReadConfig "etc/python.conf" "pymain" pymain

REM if pyexec has been found, then call the main python script.
if %pyexec% neq none (
    if exist %pyexec% (
        %pyexec% %pymain%
    ) else (
        goto Err_pyexec
    )
) else (
    goto Err_pyexec
)


:ReadConfig
REM the ReadConfig function take 3 parameters:
REM   %~1 : the conf file path.
REM   %~2 : the key.
REM   %~3 : the var that receives the value.
for /f "tokens=1,2 delims==" %%i in (%~1) do (
    if "%%j" neq "" (
        if %%i==%~2 set %~3=%%j
    )
)
goto :EOF

:Err_pyexec
echo error: python interpreter not found