from textual import containers
from textual.app import ComposeResult
from textual.reactive import reactive
from textual.screen import ModalScreen, ScreenResultType
from textual.widgets import Static

from le_chat.widgets.throbber import Throbber


class LoadingScreen(ModalScreen):
    CSS_PATH = "loading.tcss"

    loading_text = reactive("Loading...")

    def compose(self) -> ComposeResult:
        yield Throbber(id="loading-throbber")
        with containers.Horizontal(id="loading-container"):
            yield Static(self.loading_text, id="loading-label")

    def watch_loading_text(self, text: str) -> None:
        try:
            self.query_one("#loading-label", Static).update(text)
        except Exception:
            pass

    async def action_dismiss(self, result: ScreenResultType | None = None) -> None:
        self.call_after_refresh(self.dismiss, result)