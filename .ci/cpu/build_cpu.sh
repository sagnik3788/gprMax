#!/bin/bash
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "${REPO_ROOT}"

OS="$(uname -s)"

case "${OS}" in
    Linux)
        sudo apt-get update -qq
        sudo apt-get install -y -qq \
            build-essential \
            libgomp1 \
            libopenmpi-dev \
            openmpi-bin
        ;;
    Darwin)
        brew install gcc open-mpi
        ;;
    *)
        exit 1
        ;;
esac

python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
python3 -m pip install cython setuptools wheel

python3 setup.py build_ext --inplace

# Verify
python3 -c "from gprMax.cython.fields_updates_normal import update_magnetic"
python3 -c "from gprMax.cython.pml_build import pml_average_er_mr"
