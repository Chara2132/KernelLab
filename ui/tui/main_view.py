from textual.app import App, ComposeResult
from textual.widgets import Static, Button, Input
from textual.containers import Vertical, Horizontal
from core.log_parser import read_kernel_log
from core.crash_analyzer import detect_crashes
from core.timeline_builder import build_timeline, format_timeline

class KernelLabTUI(App):

    CSS_PATH = "tui.css"

    def compose(self) -> ComposeResult:
        yield Vertical(
            Button("Mostra log kernel", id="show-log"),
            Button("Analizza crash", id="analyze-crash"),
            Button("Mostra timeline eventi", id="show-timeline"),
            Button("Esci", id="exit"),
            Horizontal(
                Static(id="output", expand=True, markup=False),
                Input(placeholder="Inserisci comando", id="input")
            ),
            id="menu"
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        output = self.query_one("#output", Static)
        button_id = event.button.id

        if button_id == "show-log":
            logs = read_kernel_log()
            output.update("\n".join(logs[:30]))

        elif button_id == "analyze-crash":
            crash_data = detect_crashes()
            if not crash_data:
                output.update("Nessun crash rilevato")
            else:
                formatted = "\n".join(f"[{entry['category']}] {entry['message']}" for entry in crash_data[:30])
                output.update(formatted)

        elif button_id == "show-timeline":
            logs = read_kernel_log()
            timeline = build_timeline(logs)
            if not logs:
                output.update("Nessuna timeline rilevata")
            else:
                output.update(format_timeline(timeline[:30]))

        elif button_id == "exit":
            self.exit(0)

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        output = self.query_one("#output", Static)
        input_widget = self.query_one("#input", Input)
        command = event.value.strip()

        if not command:
            return

        if command == "help":
            result = "Comandi disponibili:\n  help\n  clear\n  version\n  show-log"
        elif command == "clear":
            result = ""
        elif command == "version":
            result = "KernelLab TUI v1.0"
        elif command == "show-log":
            logs = read_kernel_log()
            result = "\n".join(logs[:10])
        else:
            result = f"Comando non riconosciuto: '{command}'"

        output.update(output.renderable.plain + "\n> " + command + "\n" + result)
        input_widget.value = ""

KernelLabTUI().run()
