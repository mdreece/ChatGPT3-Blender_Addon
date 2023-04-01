@echo off
setlocal enabledelayedexpansion

set "BLENDER_EXE_PATH="

for /L %%x in (10, -1, 1) do (
    for /L %%y in (9, -1, 0) do (
        for /L %%z in (9, -1, 0) do (
            set "BLENDER_PATH=C:\Program Files\Blender Foundation\Blender %%x.%%y\%%x.%%y\python\bin\python.exe"
            if exist !BLENDER_PATH! (
                set "BLENDER_VERSION=%%x.%%y"
                set "BLENDER_EXE_PATH=C:\Program Files\Blender Foundation\Blender %%x.%%y\blender.exe"
                goto :install
            ) else (
                set "BLENDER_PATH=C:\Program Files\Blender Foundation\Blender %%x.%%y.%%z\%%x.%%y\python\bin\python.exe"
                if exist !BLENDER_PATH! (
                    set "BLENDER_VERSION=%%x.%%y.%%z"
                    set "BLENDER_EXE_PATH=C:\Program Files\Blender Foundation\Blender %%x.%%y.%%z\blender.exe"
                    goto :install
                )
            )
        )
    )
)

echo Python.exe not found.
exit /b 1

:install
echo Found Python.exe at: !BLENDER_PATH!
cd /d "!BLENDER_PATH!\.."
python.exe -m pip install openai


echo Installation completed.





:: Download curl
set curl_url=https://curl.se/windows/latest.cgi?p=win64-mingw.zip
set curl_zip=%userprofile%\Documents\curl.zip

powershell -Command "& { Invoke-WebRequest -Uri '%curl_url%' -OutFile '%curl_zip%' }"

:: Extract curl
set curl_folder=%userprofile%\Documents\curl
powershell -Command "& { Add-Type -AssemblyName System.IO.Compression.FileSystem; [System.IO.Compression.ZipFile]::ExtractToDirectory('%curl_zip%', '%curl_folder%') }"

:: Add curl to PATH
set PATH=%curl_folder%\bin;%PATH%

echo curl installed.
)

CLS


:: Download file
set url=https://raw.githubusercontent.com/mdreece/ChatPGT3-Blender_Addon/main/chat_gpt3_addon.py

:: Extract major and minor version numbers
for /F "tokens=1,2 delims=." %%a in ("!BLENDER_VERSION!") do (
    set "major_version=%%a"
    set "minor_version=%%b"
)

:: Combine major and minor version numbers to form the correct path
set "addon_folder=%appdata%\Blender Foundation\Blender\!major_version!.!minor_version!\scripts\addons"
set "output_file=!addon_folder!\chat_gpt3_addon.py"

:: Ensure addon folder exists
if not exist "!addon_folder!" (
    mkdir "!addon_folder!"
)

curl -L -o "!output_file!" %url%
cls
echo :: INSTALLATION OF CHAT_GPT3_ADDON COMPLETE ::
echo        - OPENAI PYTHON LIBRARY 
echo        - CURL 
echo        - CHAT_GPT3_ADDON (V0.9.2)
echo.
echo :: BLENDER WILL OPEN WHEN HITTING ENTER ::
echo ::  - ENABLE ADDON                      ::
echo ::  - ENTER API KEY                     ::
echo ::  - SELECT AI MODEL                   ::
echo.
echo. 
echo :: README.MD will open ::
pause >nul

cls

:: Automatically enable the addon
if not "!BLENDER_EXE_PATH!"=="" (
    start "" "!BLENDER_EXE_PATH!" --python-use-system-env --addons chat_gpt3_addon
) else (
    echo Blender.exe not found.
)

TIMEOUT /T 3 >NUL
CLS

start "" "https://raw.githubusercontent.com/mdreece/ChatPGT3-Blender_Addon/main/README.md"

CLOSE

