
from dataclasses import dataclass
from typing import TYPE_CHECKING, List, Literal, Optional
from le_chat.utils.prompt.extract import extract_paths_from_prompt
from le_chat.utils.prompt.resource import load_resource

if TYPE_CHECKING:
    from pathlib import Path

@dataclass
class MLXVLMInput:
    prompt: str
    images: Optional[List[Path]]
    audio: Optional[List[Path]]

def build(prompt: str):
    result = []
    last_index = 0
    audio = []
    images = []
    for path, a, b in extract_paths_from_prompt(prompt):
        additional_token = ""
        resource = load_resource(path)
        if resource.resource_type == 'text':
            additional_token = resource.text
        elif resource.resource_type == 'audio':
            additional_token = ""
            audio.append(resource.path)

        elif resource.resource_type == "image":
            additional_token = "<image>"
            images.append(resource.path)
            
        result.append(prompt[last_index:a])
        result.append(additional_token)
        last_index = b
    result.append(prompt[last_index:])
    replaced_prompt = "".join(result)

    return MLXVLMInput(
        prompt=replaced_prompt,
        images=images,
        audio=audio
    )

    






