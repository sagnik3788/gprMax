import os
import subprocess
import sys


# TODO: Refactor this,it looks weird
# os.environ["PATH"] = f"/usr/local/cuda/bin:{os.environ.get('PATH', '')}"
# os.environ["CPATH"] = f"/usr/local/cuda/include:{os.environ.get('CPATH', '')}"
# os.environ["LD_LIBRARY_PATH"] = f"/usr/local/cuda/lib64:{os.environ.get('LD_LIBRARY_PATH', '')}"


def run(command):
    print(f"\n>>> {' '.join(command)}")
    subprocess.check_call(command)


# run(["apt-get", "update", "-qq"])
# run(["apt-get", "install", "-y", "-qq", "libopenmpi-dev"])

# Clone the repo
REPO = os.environ.get("REPO_URL", "https://github.com/sagnik3788/gprMax.git")
BRANCH = os.environ.get("BRANCH", "feature/cicd-automation")
run(["git", "clone", "--branch", BRANCH, "--depth", "1", REPO])
os.chdir("gprMax")
# install deps
run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

# cpu files
run([sys.executable, "setup.py", "build_ext", "--inplace", "-j", "2"])

# verify nvcc
run(["nvcc", "--version"])
run([sys.executable, "-c", "import pycuda.driver as drv; drv.init(); print(f'[OK] GPU detected: {drv.Device(0).name()}')"])

# Run  simulation
run([sys.executable, "-m", "gprMax", "examples/cylinder_Ascan_2D.in", "-gpu"])

print("\nAll gprMax GPU tests passed on Kaggle!")
