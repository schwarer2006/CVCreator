@echo off
SET "PROJECT_DIR=C:\PythonProjects\CVCreator"
SET "VENV_DIR=%PROJECT_DIR%\venv"
SET "APP_FILE=%PROJECT_DIR%\app.py"
SET "LOG_FILE=%PROJECT_DIR%\log.txt"

:: Erstellen eines Log-Files
echo Log-Datei wird erstellt... > %LOG_FILE%

:menu
echo ================================
echo CV Creator - Menu
echo ================================
echo 1. Virtuelle Umgebung erstellen
echo 2. Virtuelle Umgebung starten
echo 3. Virtuelle Umgebung stoppen
echo 4. app.py ausführen
echo 5. Beenden
echo ================================
set /p choice="Wählen Sie eine Option (1-5): "

if %choice%==1 goto create_venv
if %choice%==2 goto start_venv
if %choice%==3 goto stop_venv
if %choice%==4 goto run_app
if %choice%==5 goto end

:create_venv
if not exist %VENV_DIR% (
    echo Erstelle virtuelle Umgebung...
    echo Erstelle virtuelle Umgebung... >> %LOG_FILE%
    python -m venv %VENV_DIR%
    echo Virtuelle Umgebung wurde erstellt.
    echo Virtuelle Umgebung wurde erstellt. >> %LOG_FILE%
) else (
    echo Virtuelle Umgebung existiert bereits.
    echo Virtuelle Umgebung existiert bereits. >> %LOG_FILE%
)
goto menu

:start_venv
if exist %VENV_DIR%\Scripts\activate.bat (
    echo Starte virtuelle Umgebung...
    echo Starte virtuelle Umgebung... >> %LOG_FILE%
    call %VENV_DIR%\Scripts\activate.bat
    echo Virtuelle Umgebung gestartet.
    echo Virtuelle Umgebung gestartet. >> %LOG_FILE%
) else (
    echo Virtuelle Umgebung nicht gefunden. Bitte zuerst erstellen.
    echo Virtuelle Umgebung nicht gefunden. >> %LOG_FILE%
)
goto menu

:stop_venv
echo Virtuelle Umgebung wird gestoppt...
echo Virtuelle Umgebung wird gestoppt... >> %LOG_FILE%
goto menu

:run_app
echo Prüfen, ob app.py existiert...
echo Prüfen, ob app.py existiert... >> %LOG_FILE%
echo Erwarteter Pfad: %APP_FILE%
echo Erwarteter Pfad: %APP_FILE% >> %LOG_FILE%
if exist %APP_FILE% (
    echo app.py gefunden.
    echo app.py gefunden. >> %LOG_FILE%
    echo Starte app.py...
    echo Starte app.py... >> %LOG_FILE%
    call %VENV_DIR%\Scripts\activate.bat
    python %APP_FILE%
    echo app.py wurde ausgeführt. >> %LOG_FILE%
) else (
    echo app.py nicht gefunden im Pfad: %APP_FILE%.
    echo app.py nicht gefunden im Pfad: %APP_FILE%. >> %LOG_FILE%
    echo Inhalt des Verzeichnisses: >> %LOG_FILE%
    dir %PROJECT_DIR% >> %LOG_FILE%
)
goto menu

:end
echo Beenden...
exit
