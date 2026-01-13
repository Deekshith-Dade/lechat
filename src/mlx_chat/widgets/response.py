from dataclasses import dataclass
from textual.reactive import reactive
from textual.message import Message
from textual.widgets import Markdown
from textual.widgets.markdown import MarkdownStream


@dataclass
class ResponseUpdate(Message):
    text: str

class Response(Markdown):
    BORDER_TITLE = "AI"
    

    def __init__(self, markdown: str | None = None) -> None:
        super().__init__(markdown)
        self._stream: MarkdownStream | None = None

    @property
    def stream(self) -> MarkdownStream:
        if self._stream is None:
            self._stream = self.get_stream(self)
        return self._stream
    
    async def append_fragment(self, fragment: str) -> None:
        await self.stream.write(fragment)
