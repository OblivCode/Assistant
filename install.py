import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
def install_win(package):
    subprocess.check_call([sys.executable, '-m', 'pipwin','install', package])
file = open('requirements.txt', 'r')
packages = file.readlines()

for package in packages:
    install(package)

install_win('pyaudio~=0.2')