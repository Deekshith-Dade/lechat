from typing import Iterable

from rich.text import Text

from textual import containers
from textual.app import ComposeResult
from textual.highlight import highlight
from textual.widgets import Static

from le_chat.menus import MenuItem
from le_chat.widgets.non_selectable_label import NonSelectableLabel
from le_chat.widgets.prompt import RE_MATCH_FILE_PROMPT, TextualHighlightTheme


class HighlightedContent(Static):
    """A Static widget that highlights file references like @filename."""
    
    def __init__(self, content: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self._raw_content = content
    
    def on_mount(self) -> None:
        self.update(self._render_highlighted())
    
    def _render_highlighted(self) -> Text:
        """Render content with file references highlighted."""
        content = highlight(
            self._raw_content,
            language="markdown",
            theme=TextualHighlightTheme
        )
        content = content.highlight_regex(
            RE_MATCH_FILE_PROMPT, 
            style="bold #00d9ff"  # Cyan color for file refs
        )
        rendered = list(content.render_segments(self.visual_style))
        return Text.assemble(
            *[(text, style) for text, style, _ in rendered],
            end="",
        )


class UserInput(containers.HorizontalGroup):
    def __init__(self, content: str) -> None:
        super().__init__()
        self.content = content

    def compose(self) -> ComposeResult:
        yield NonSelectableLabel("❯", id="prompt")
        yield HighlightedContent(self.content, id="content")

    def get_block_menu(self) -> Iterable[MenuItem]:
        yield from ()

    def get_block_content(self, destination: str) -> str | None:
        return self.content