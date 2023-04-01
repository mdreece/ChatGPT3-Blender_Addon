@echo off
setlocal enabledelayedexpansion

for /L %%x in (10, -1, 1) do (
    for /L %%y in (9, -1, 0) do (
        set "BLENDER_PATH=C:\Program Files\Blender Foundation\Blender %%x.%%y\%%x.%%y\python\bin\python.exe"
        if exist !BLENDER_PATH! (
            set "BLENDER_VERSION=%%x.%%y"
            echo Found Python.exe at: !BLENDER_PATH!
            cd "C:\Program Files\Blender Foundation\Blender %%x.%%y\%%x.%%y\python\bin"
            python.exe -m pip install openai
            goto :done
        )
    )
)

echo Python.exe not found.
exit /b 1
cls
:done
echo Installation completed.

:: Check if curl is installed
where curl >nul 2>nul
if %errorlevel% neq 0 (
    echo curl not found, downloading and installing curl...

    :: Download curl
    set curl_url=https://curl.se/windows/dl-7.79.1/curl-7.79.1-win64-mingw.zip
    set curl_zip=curl.zip

    powershell -Command "& { (New-Object System.Net.WebClient).DownloadFile('%curl_url%', '%curl_zip%') }"

    :: Extract curl
    set curl_folder=curl
    powershell -Command "& { Add-Type -AssemblyName System.IO.Compression.FileSystem; [System.IO.Compression.ZipFile]::ExtractToDirectory('%curl_zip%', '%curl_folder%') }"

    :: Add curl to PATH
    set PATH=%cd%\%curl_folder%\bin;%PATH%

    echo curl installed.
)

:: Download file
set url=https://raw.githubusercontent.com/mdreece/ChatPGT3-Blender_Addon/main/chat_gpt3_addon.py
set output_file=%appdata%\Blender Foundation\Blender\!BLENDER_VERSION!\scripts\addons\chat_gpt3_addon.py

@echo off
curl -L -o "%output_file%" %url%
cls
echo :: INSTALLATION OF CHAT_GPT3_ADDON COMPLETE ::
echo		- OPENAI PYTHON LIBRARY 
echo		- CURL 
echo		- CHAT_GPT3_ADDON (V0.9.2)
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

start "" "C:\Program Files\Blender Foundation\Blender !BLENDER_VERSION!\blender.exe" --python-use-system-env --addons chat_gpt3_addon

TIMEOUT /T 3 >NUL
CLS

start "" "https://raw.githubusercontent.com/mdreece/ChatPGT3-Blender_Addon/main/README.md"

CLOSE

