#!/bin/bash
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "${REPO_ROOT}"

if [ "$(uname -s)" == "Linux" ]; then
    sudo apt-get update -qq
    sudo apt-get install -y -qq build-essential libgomp1
fi

python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
python3 -m pip install cython setuptools wheel

python3 setup.py build_ext --inplace

# Verify
python3 -c "from gprMax.cython.fields_updates_normal import update_magnetic"
python3 -c "from gprMax.cython.pml_build import pml_average_er_mr"

# Verify (MPI)
# to avoid file lock
export HDF5_USE_FILE_LOCKING=FALSE
mpirun -n 2 python3 -m gprMax examples/cylinder_Ascan_2D.in
