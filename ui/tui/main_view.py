#ui/tui/main_view.py
from textual.app import App, ComposeResult
from textual.widgets import Static, Input
from textual.containers import Vertical, VerticalScroll
from textual.events import Key
from core.log_parser import read_kernel_log
from core.crash_analyzer import detect_crashes
from core.timeline_builder import build_timeline, format_timeline

class KernelLabTUI(App):
    def __init__(self, **kwargs)->None:
        super().__init__(**kwargs)
        self.command_history: list[str] = []
        self.history_index: int | None = None

    CSS_PATH = "tui.tcss"

    def compose(self) -> ComposeResult:
        yield Vertical(
            Input(id="input", placeholder="Scrivi il tuo comando"),
            VerticalScroll(Static("", id="output", markup=False, expand=True), id="scroll_output"),
            id="menu"
        )

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        command = event.value.strip()
        if command:
            self.command_history.append(command)
        self.history_index = None
        output_static = self.query_one("#output", Static)
        scroll_view = self.query_one("#scroll_output")
        input_str = self.query_one("#input", Input)

        command = input_str.value.strip().split()
        if not command:
            return

        if command[0] == "help" or (len(command) > 1 and command[1] in ("-h", "--help")):
            result = (
                "Comandi disponibili:\n"
                "  >show-kernel-log [-t | --total] / [-l | --length] N \n"
                "  >show-crash-log [-t | --total] / [-l | --length] N\n"
                "  >show-timeline [-t | --total] / [-l | --length] N\n"
                "  >help -h | --help\n"
                "  >clear\n"
                "  >version\n"
                "  -exit"
            )
        elif command[0] == "clear":
            output_static.update("")
            result = ""
        elif command[0] == "version":
            result = "KernelLab TUI v1.0"
        elif command[0] == "show-kernel-log":
            if len(command) > 1 and command[1] in ("-t", "--total"):
                result = "\n".join(read_kernel_log())
            elif len(command) > 2 and command[1] in ("-l", "--length"):
                try:
                    n = int(command[2])
                    result = "\n".join(read_kernel_log()[:n])
                except (IndexError, ValueError):
                    result = "Errore: specifica un numero valido dopo -l, es. `show-kernel-log -l 10`"
            else:
                result = "Sintassi non valida. Usa `show-kernel-log -t` o `-l <num>`"
        elif command[0] == "show-crash-log":
            logs = detect_crashes()
            if not logs:
                result = "Nessun crash rilevato"
            elif len(command) > 1 and command[1] in ("-l", "--length") and len(command) > 2:
                try:
                    n = int(command[2])
                    result = "\n".join(f"[{entry['category']}] {entry['message']}" for entry in logs[:n])
                except ValueError:
                    result = "Errore: specifica un numero valido dopo -l, es. `show-crash-log -l 10`"
            else:
                result = "\n".join(f"[{entry['category']}] {entry['message']}" for entry in logs)
        elif command[0] == "show-timeline":
            logs = read_kernel_log()
            timeline = build_timeline(logs)
            if not timeline:
                result = "Nessuna timeline rilevata"
            elif len(command) > 1 and command[1] in ("-l", "--length") and len(command) > 2:
                try:
                    n = int(command[2])
                    result = format_timeline(timeline[:n])
                except ValueError:
                    result = "Errore: specifica un numero valido dopo -l, es. `show-timeline -l 10`"
            else:
                result = format_timeline(timeline)
        elif command[0] == "exit":
            self.exit(0)
            result = ""
        else:
            result = f"Comando non riconosciuto: '{command[0]}'"

        if isinstance(result, list):
            result = "\n".join(result)
        output_static.update(output_static.renderable + "\n> " + " ".join(command) + "\n" + result)
        input_str.value = ""
        scroll_view.scroll_end(animate=True)

    async def on_key(self, event: Key) -> None:
        scroll_view = self.query_one("#scroll_output")
        input_widget = self.query_one("#input", Input)
        if input_widget.has_focus:  
            if event.key == "up":
                if not self.command_history: return  
                if self.history_index is None:
                    self.history_index = len(self.command_history) - 1
                else:
                    self.history_index = max(0, self.history_index - 1)
                input_widget.value = self.command_history[self.history_index]
                event.stop()
            elif event.key == "down":
                if self.history_index is None:
                    return
                if self.history_index >= len(self.command_history) - 1:
                    self.history_index = None
                    input_widget.value = ""
                else:
                    self.history_index += 1
                    input_widget.value = self.command_history[self.history_index]
                event.stop()
        if event.key == "down":
            scroll_view.scroll_down()
            scroll_view.scroll_down()
            scroll_view.scroll_down()
            event.stop()
        elif event.key == "up":
            scroll_view.scroll_up()
            scroll_view.scroll_up()
            scroll_view.scroll_up()
            event.stop()
        elif event.key == "right":
            scroll_view.scroll_right()
            scroll_view.scroll_right()
            scroll_view.scroll_right()
        elif event.key == "left":
            scroll_view.scroll_left()
            scroll_view.scroll_left()
            scroll_view.scroll_left()

KernelLabTUI().run()
