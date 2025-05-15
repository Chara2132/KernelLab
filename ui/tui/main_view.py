# ui/tui/tui.py
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, ListView, ListItem
from textual.containers import Horizontal
from textual.reactive import reactive
from core.log_parser import read_kernel_log
from core.crash_analyzer import detect_crashes
from core.timeline_builder import build_timeline, format_timeline

class KernelLabTUI(App):

    CSS_PATH = "tui.css"

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Horizontal(
            ListView(id="menu"),
            Static(id="output", expand=True)
        )
        yield Footer()

    def on_mount(self):
        menu = self.query_one("#menu", ListView)
        menu_items = [
            ("Mostra log kernel", self.show_kernel_log),
            ("Analizza crash", self.show_crash_report),
            ("Mostra timeline", self.show_timeline),
            ("Esci", self.exit)
        ]
        for label, _ in menu_items:
            menu.append(ListItem(Static(label)))

        self.menu_actions = {label: action for label, action in menu_items}
        self.show_kernel_log()
        self.query_one("#menu").focus()

    async def on_list_view_selected(self, event):
        static_widget = event.item.query_one(Static)
        selected_label = static_widget.renderable  
        action = self.menu_actions.get(selected_label)
        if action:
            action()


    def show_kernel_log(self):
        output = self.query_one("#output", Static)
        logs = read_kernel_log()
        escaped_logs = [line.replace("[", r"\[").replace("]", r"\]") for line in logs[:30]]
        output.update("\n".join(escaped_logs))


    def show_crash_report(self):
        output = self.query_one("#output", Static)
        crash_data = detect_crashes()
        if not crash_data:
            output.update("[green]Nessun crash o errore rilevato nei log[/green]")
            return
        formatted = "\n".join(f"[{cat}] {msg}" for cat, msg in crash_data[:30])
        output.update(formatted)

    def show_timeline(self):
        output = self.query_one("#output", Static)
        logs = read_kernel_log()
        timeline = build_timeline(logs)
        output.update(format_timeline(timeline[:30]))

    def exit(self):
        return


KernelLabTUI().run()
