# helper.py

import os
import re
import subprocess

def read_kernel_log_journalctl() -> list[str]:
    """Legge i log del kernel usando journalctl (sistemi con systemd)"""
    try:
        logs = subprocess.check_output(['journalctl', '-k', '--no-pager'], text=True)
        return logs.splitlines()
    except FileNotFoundError:
        return ["[Errore] journalctl non trovato. systemd potrebbe non essere in uso."]
    except subprocess.CalledProcessError as e:
        return [f"[Errore] journalctl ha fallito: {e}"]
    except Exception as e:
        return [f"[Errore] {e}"]

def filter_logs(log_lines, keyword=None)->list[str]:
    """Filtra i log per una parola chiave"""
    if keyword:
        return [line for line in log_lines if keyword.lower() in line.lower()]
    return log_lines

def extract_timestamps(log_lines)->list[str]:
    """Estrae i timestamp dalle righe di log (formato tipico: 'Jan  1 12:00:00')"""
    timestamps = []
    for line in log_lines:
        match = re.match(r"^\w{3} +\d{1,2} \d{2}:\d{2}:\d{2}", line)
        if match:
            timestamps.append(match.group())
    return timestamps

def summarize_logs(log_lines)->dict[str,int]:
    """Conta quanti errori/warning/info ci sono"""
    summary = {"error": 0, "warning": 0, "info": 0}
    for line in log_lines:
        lower = line.lower()
        if "error" in lower:
            summary["error"] += 1
        elif "warn" in lower:
            summary["warning"] += 1
        elif "info" in lower:
            summary["info"] += 1
    return summary
