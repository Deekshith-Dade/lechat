import llm
from textual import containers, getters, on, work
from textual.app import ComposeResult
from textual.reactive import reactive, var
from textual.widgets import Input

from mlx_chat.widgets.throbber import Throbber
from mlx_chat.widgets.user_input import UserInput
from mlx_chat.widgets.response import Response, ResponseUpdate


SYSTEM = "You are the HAL 9000 the AI from the movie 2001 Space Odyssey and you are sentient. Have fun with user pretending you are this."

class Conversation(containers.Vertical):
    
    BINDING_GROUP_TITLE = "Conversation"
    model_name = var("gpt-4o")
    busy_count = var(0)
    
    throbber: getters.query_one(Throbber) = getters.query_one("#throbber")
    

    def __init__(self, model_name: str):
        super().__init__()
        self.model_name = model_name
    
    async def on_mount(self) -> None:
        def start_agent() -> None:
            self.agent = llm.get_model(self.model_name) 
            self.agent.key = "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"
        
        self.call_after_refresh(start_agent)
    
    def compose(self) -> ComposeResult:
        yield Throbber(id="throbber")
        with containers.Vertical(id="chat-view"):
            yield Response("INTERFACE 2037 READY FOR INQUIRY")
            yield Input(placeholder="How can I help you?", id="input-area")
 
    @on(Input.Submitted)
    async def on_input(self, event: Input.Submitted) -> None:
        self.busy_count += 1
        chat_view = self.query_one("#chat-view")
        event.input.clear()
        await chat_view.mount(UserInput(event.value))
        self._agent_response = response = Response()
        await chat_view.mount(response)
        response.anchor()
        response.border_title = self.model_name.upper()
        self.send_prompt(event.value)
    
    @on(ResponseUpdate)
    async def on_response_update(self, event: ResponseUpdate) -> None:
        event.stop()
        if self._agent_response is not None:
            await self._agent_response.append_fragment(event.text)
        
    def watch_model_name(self, model_name: int) -> None:
        try:
            self.agent = llm.get_model(model_name)
        except Exception as e:
            print(f"Model name not found")
            raise 

    def watch_busy_count(self, busy: int) -> None:
        self.throbber.set_class(busy > 0, "-busy")
        
    @work(thread=True)
    def send_prompt(self, prompt: str) -> None:
        response_content = ""
        llm_response = self.agent.prompt(prompt, system=SYSTEM)
        for chunk in llm_response:
            response_content += chunk

            self.post_message(ResponseUpdate(text=chunk))
        
        self._agent_response = None
        self.busy_count -= 1
        return response_content
