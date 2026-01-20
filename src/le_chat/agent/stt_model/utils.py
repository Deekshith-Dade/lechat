from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional

from le_chat.utils.prompt.extract import extract_paths_from_prompt
from le_chat.utils.prompt.resource import load_resource


@dataclass
class STTInput:
    prompt: str
    audio: List[str]


def build(prompt: str) -> STTInput:
    """Extract audio file paths from a prompt.
    
    Args:
        prompt: The user prompt potentially containing @file references.
        
    Returns:
        STTInput with the cleaned prompt and list of audio file paths.
    """
    result = []
    last_index = 0
    audio = []
    
    for path, a, b in extract_paths_from_prompt(prompt):
        resource = load_resource(Path(path))
        additional_token = ""
        
        if resource.resource_type == 'audio':
            audio.append(str(resource.path))
            additional_token = f"[Audio: {Path(path).name}]"
        else:
            # Keep non-audio file references as-is
            additional_token = prompt[a:b]
        
        result.append(prompt[last_index:a])
        result.append(additional_token)
        last_index = b
    
    result.append(prompt[last_index:])
    replaced_prompt = "".join(result)
    
    return STTInput(
        prompt=replaced_prompt,
        audio=audio
    )


def extract_audio_paths(prompt: str) -> List[str]:
    """Extract only audio file paths from a prompt.
    
    Args:
        prompt: The user prompt potentially containing @file references.
        
    Returns:
        List of audio file paths found in the prompt.
    """
    audio_paths = []
    
    for path, _, _ in extract_paths_from_prompt(prompt):
        resource = load_resource(Path(path))
        if resource.resource_type == 'audio':
            audio_paths.append(str(resource.path))
    
    return audio_paths
