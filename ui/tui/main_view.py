#ui/tui/main_view.py
from pathlib import Path
from textual.events import Key
from textual.widgets import Static, Input
from textual.app import App, ComposeResult
from textual.containers import Vertical, VerticalScroll
from core.cmd import shell_command
from core.log_parser import read_kernel_log
from core.crash_analyzer import detect_crashes
from core.timeline_builder import build_timeline, format_timeline

class KernelLabTUI(App):
    def __init__(self, **kwargs)->None:
        super().__init__(**kwargs,css_path="tui.tcss")
        self.command_history: list[str] = []
        self.history_index: int | None = None
        self.current_dir = Path.home()
        self.UNSUPPORTED_COMMANDS = [
            "sudo",
            "vim",
            "nano",
            "less",
            "more",
            "man",
            "top",
            "htop",
            "btop",
            "ssh",
            "su",
            "ftp",
            "sftp",
            "python",
            "ipython",
            "gdb",
            "tmux",
            "screen",
            "dialog",
            "whiptail",
            "watch",
            "yes",
            "tail -f",
            "ping",
            "read",
            "pacman",
            "apt",
            "pip",
        ]
    def compose(self) -> ComposeResult:
        yield Vertical(
            VerticalScroll(Static("", id="output", markup=False, expand=True), id="scroll_output"),
            Input(id="input", placeholder="Scrivi il tuo comando"),
            id="menu"
        )

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        scroll_view = self.query_one("#scroll_output")
        output_static = self.query_one("#output", Static)
        input_str = self.query_one("#input", Input)
        command = input_str.value.strip().split()
        self.history_index = None

        if input_str.value.strip(): self.command_history.append(input_str.value)
        if not command: return

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
        elif command[0] in self.UNSUPPORTED_COMMANDS :
            result = f"⚠️ I comandi con `{command[0]}` non sono supportati nella shell simulata."
        elif command[0] == "version":
            result = "  KernelLab TUI v1.0"
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
        elif command[0] == "clear": 
            output_static.update("")
            result=""
        elif command[0] == "exit":
            self.exit(0)
            result = ""
        else:
            command=input_str.value.strip()
            result = shell_command(command, self.current_dir)

        if isinstance(result, str) and result.startswith("__cd__"):
            self.current_dir = Path(result.replace("__cd__", ""))
            result = f"Directory attuale: {self.current_dir}"
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
        if event.key == "down":    [scroll_view.scroll_down() for _ in range(4)]
        elif event.key == "up":    [scroll_view.scroll_up() for _ in range(4)]
        elif event.key == "right": [scroll_view.scroll_right() for _ in range(4)]
        elif event.key == "left":  [scroll_view.scroll_left() for _ in range(4)]

KernelLabTUI().run()