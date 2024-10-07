@echo off
:: Pfad zum Projektordner
set PROJECT_DIR=C:\PythonProjects\CVCreator

:: Wechsel in das Projektverzeichnis
cd %PROJECT_DIR%

:: Überprüfen, ob venv existiert, wenn nicht, dann erstellen
if not exist "venv" (
    echo Erstelle virtuelle Umgebung...
    python -m venv venv
)

:: Unterordner für Scripts (abhängig von der Plattform)
set VENV_SCRIPTS=%PROJECT_DIR%\venv\Scripts

:: Aktivieren der virtuellen Umgebung
echo Aktiviere virtuelle Umgebung...
call %VENV_SCRIPTS%\activate

:: App ausführen
if exist "app.py" (
    echo Starte app.py...
    python app.py
) else (
    echo "app.py nicht gefunden."
)

:: Stoppen der virtuellen Umgebung
echo Deaktiviere virtuelle Umgebung...
deactivate

pause
