@echo off

for /f "delims=" %%i in ('git rev-parse --show-toplevel') do set REPO_ROOT=%%i
cd /d "%REPO_ROOT%"

:: System dependencies (ig pre-installed)
:: choco install msmpi

python -m pip install --upgrade pip
python -m pip install numpy cython jinja2 setuptools wheel mpi4py

python setup.py build_ext --inplace

:: Verify
dir /s /b gprMax\cython\*.pyd > nul 2>&1
if %ERRORLEVEL% NEQ 0 exit /b 1

:: python -c "from gprMax.cython.fields_updates_normal import update_magnetic"
:: python -c "from gprMax.cython.pml_build import pml_average_er_mr"
