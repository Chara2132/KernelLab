# core/crash_formatter.py
from rich.console import Console
from rich.table import Table
import json

console = Console()

def print_crash_table(crash_data):
    table = Table(title="🧠 Kernel Crash Report", header_style="bold magenta")
    table.add_column("Categoria", style="cyan", no_wrap=True)
    table.add_column("Messaggio", style="white")
    table.add_column("Matched", style="green")

    for crash in crash_data:
        table.add_row(
            crash["category"],
            crash["message"],
            ", ".join(crash["matched"])
        )

    console.print(table)

def export_to_json(crash_data, filepath="crash_report.json"):
    with open(filepath, "w") as f:
        json.dump(crash_data, f, indent=4)
    console.print(f"[bold green]✔ Salvato crash report in:[/] {filepath}")
