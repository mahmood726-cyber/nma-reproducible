@echo off
setlocal
echo === Enter archive root
cd /d "%~dp0"
if errorlevel 1 exit /b 1
echo === Use inherited R binary directory when provided
if defined R_BIN set "PATH=%R_BIN%;%PATH%"
echo === Use inherited R_LIBS_USER and R_LIBS unchanged; disable user Renviron
set "R_ENVIRON_USER=NUL"
echo === Use UTF-8 Python console output
set "PYTHONUTF8=1"
echo === Verify source, protected originals and release manifest before running
python scripts/recut_integrity.py
if errorlevel 1 exit /b 1
echo === Preserve prior full results and outputs as full.prev-N
python scripts/recut_run.py rotate
if errorlevel 1 exit /b 1
echo === Original full validation with original version pins and tolerances
python reproduce.py --allow-version-mismatch
if errorlevel 1 exit /b 1
echo === Report actual original-validation N/N
python scripts/recut_run.py summary
if errorlevel 1 exit /b 1
echo === Numerical extras scope
python scripts/recut_run.py extras
if errorlevel 1 exit /b 1
echo === Browser usability smoke and existing archived-corpus replay
python scripts/recut_run.py ui
if errorlevel 1 exit /b 1
echo === Verify manifests and protected originals after the run
python scripts/recut_integrity.py
if errorlevel 1 exit /b 1
echo === RUN_PLAN completed successfully
exit /b 0
