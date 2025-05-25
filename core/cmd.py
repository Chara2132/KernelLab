import subprocess
import shlex
from pathlib import Path

def shell_command(command: str, cwd: Path) -> str | None:
    command = command.strip()
    if command.startswith("cd"):
        parts = shlex.split(command)
        if len(parts) == 1:
            return str(Path.home())  
        elif len(parts) == 2:
            new_dir = (cwd / parts[1]).resolve()
            if new_dir.exists() and new_dir.is_dir():
                return f"__cd__{str(new_dir)}"
            else:
                return f"Errore: directory '{parts[1]}' non trovata"
        else:
            return "Uso corretto: cd [directory]"
    try:
        args = shlex.split(command)
        result = subprocess.run(
            args,
            shell=False,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout.strip() or result.stderr.strip()
    except Exception as e:
        return f"Errore nell'esecuzione del comando: {e}"
