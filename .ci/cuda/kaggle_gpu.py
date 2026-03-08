import os
import subprocess
import sys


# TODO: Refactor this,it looks weird
os.environ["PATH"] = f"/usr/local/cuda/bin:{os.environ.get('PATH', '')}"
os.environ["CPATH"] = f"/usr/local/cuda/include:{os.environ.get('CPATH', '')}"
os.environ["LD_LIBRARY_PATH"] = f"/usr/local/cuda/lib64:{os.environ.get('LD_LIBRARY_PATH', '')}"


def run(command):
    """Run a shell command and fail on error."""
    print(f"\n>>> {' '.join(command)}")
    result = subprocess.run(command, env=os.environ, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    if result.returncode != 0:
        print(result.stdout)
        result.check_returncode()
    print(result.stdout)


# Clone 
REPO = os.environ.get("REPO_URL", "https://github.com/sagnik3788/gprMax.git")
BRANCH = os.environ.get("BRANCH", "feature/cicd-automation")

run(["apt-get", "update", "-qq"])
run(["apt-get", "install", "-y", "-qq", "git", "libopenmpi-dev", "build-essential"])

run(["git", "clone", "--branch", BRANCH, "--depth", "1", REPO])
os.chdir("gprMax")

# Install deps
run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
run([sys.executable, "-m", "pip", "install", "cython", "setuptools", "wheel", "pycuda"])

# cpu extensions
run([sys.executable, "setup.py", "build_ext", "--inplace"])

# Verify
run(["nvcc", "--version"])
run([sys.executable, "-c", "import pycuda.driver as drv; drv.init(); print(f'[OK] GPU: {drv.Device(0).name()}')"])


run([sys.executable, "-c", "import gprMax; from gprMax.cuda_opencl import knl_fields_updates; print('[OK] CUDA kernel templates loaded')"])

# gpu simulation
run([sys.executable, "-m", "gprMax", "examples/cylinder_Ascan_2D.in", "-gpu"])

print("\n All cuda tests passeed!")

