# helper.py

import os
import re

def read_log_file(path="/var/log/kern.log")->str:
    """Legge il contenuto di un file di log del kernel"""
    try:
        with open(path, "r") as f:
            return f.readlines()
    except FileNotFoundError:
        return ["[Errore] File non trovato: " + path]
    except PermissionError:
        return ["[Errore] Permessi insufficienti per accedere a: " + path]

def filter_logs(log_lines, keyword=None)->str:
    """Filtra i log per una parola chiave"""
    if keyword:
        return [line for line in log_lines if keyword.lower() in line.lower()]
    return log_lines

def extract_timestamps(log_lines)->str:
    """Estrae i timestamp dalle righe di log (formato tipico: 'Jan  1 12:00:00')"""
    timestamps = []
    for line in log_lines:
        match = re.match(r"^\w{3} +\d{1,2} \d{2}:\d{2}:\d{2}", line)
        if match:
            timestamps.append(match.group())
    return timestamps

def summarize_logs(log_lines)->dict:
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
