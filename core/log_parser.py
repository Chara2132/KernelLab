# core/log_parser.py
import subprocess

def read_dmesg():
    """
    Tenta di leggere i log del kernel con dmesg.
    Ritorna una lista di linee di log.
    """
    try:
        output = subprocess.check_output(["dmesg"], text=True, stderr=subprocess.DEVNULL)
        return output.splitlines()
    except subprocess.CalledProcessError:
        return []

def read_journalctl():
    """
    Fallback: legge i log del kernel tramite journalctl -k.
    Ritorna una lista di linee di log.
    """
    try:
        output = subprocess.check_output(["journalctl", "-k", "--no-pager"], text=True, stderr=subprocess.DEVNULL)
        return output.splitlines()
    except subprocess.CalledProcessError:
        return []

def read_kernel_log():
    """
    Funzione unica per leggere i log del kernel usando dmesg o journalctl.
    Se dmesg fallisce (es. permessi), usa journalctl.
    Ritorna una lista di linee di log.
    """
    logs = read_dmesg()
    if not logs:
        logs = read_journalctl()
    return logs
