import subprocess
import sys
import os
import platform
import subprocess

sys_os = platform.platform()
APP_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(APP_PATH)
sys.path.append(MODULE_PATH)
cmd_line = str('export PYTHONPATH="${PYTHONPATH}:' + f'{MODULE_PATH}"')
os.system(cmd_line)
print(f"Current project path: {APP_PATH},\n and module path {MODULE_PATH} added to System: {sys_os}")
