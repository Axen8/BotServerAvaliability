import psutil
import subprocess
import time

server_command = "E:\\Server\\ServerForge\\run.bat"
for process in psutil.process_iter(['cmdline']):
    try:
        cmdline = process.info['cmdline']
        if cmdline and server_command in " ".join(cmdline):
            print("Server is running")
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass
