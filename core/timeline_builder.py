# core/timeline_builder.py
import re
from datetime import datetime

TIMESTAMP_REGEX = re.compile(r"\[(\d+\.\d+)\]")

def parse_timestamp(line):
    """
    Estrae il timestamp in secondi dalla linea di log.
    Restituisce un float o None se non trova il timestamp.
    """
    match = TIMESTAMP_REGEX.search(line)
    if match:
        return float(match.group(1))
    return None

def build_timeline(log_lines):
    """
    Riceve una lista di log lines.
    Estrae timestamp e linea, filtra le linee senza timestamp.
    """
    timeline = []
    for line in log_lines:
        ts = parse_timestamp(line)
        if ts is not None:
            timeline.append({"timestamp": ts, "line": line})
    timeline.sort(key=lambda x: x["timestamp"])
    return timeline

def format_timeline(timeline):
    """
    Formatta la timeline per una stampa leggibile.
    """
    lines = []
    for event in timeline:
        ts = event["timestamp"]
        line = event["line"]
        lines.append(f"{ts:010.3f} - {line}")
    return "\n".join(lines)


