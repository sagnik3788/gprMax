@echo off

for /f "delims=" %%i in ('git rev-parse --show-toplevel') do set REPO_ROOT=%%i
cd /d "%REPO_ROOT%"

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install cython setuptools wheel

python setup.py build_ext --inplace

:: Verify
python -c "from gprMax.cython.fields_updates_normal import update_magnetic"
if %ERRORLEVEL% NEQ 0 exit /b 1

:: Verify (MPI)
:: to avoid file lockling
set HDF5_USE_FILE_LOCKING=FALSE
mpiexec -n 2 python -m gprMax examples/cylinder_Ascan_2D.in
if %ERRORLEVEL% NEQ 0 exit /b 1