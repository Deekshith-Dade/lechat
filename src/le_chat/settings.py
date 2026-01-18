from dataclasses import dataclass
from typing import Required, Sequence, TypedDict


@dataclass
class Setting:
    
    key: str
    title: str
    type: str = "object"
    help: str = ""
    choices: list[str] | None = None
    validate: list[dict] | None = None
    children: dict[str, "Setting"] | None = None 
    editable: bool = True

class SchemaDict(TypedDict, total=False):
    key: Required[str]
    title: Required[str]
    type: Required[str]
    help: str
    choices: list[str] | list[tuple[str, str]] | None
    default: object
    fields: list["SchemaDict"]
    validate: list[dict]
    editable: bool

type SettingsType = dict[str, object]

def prase_key(key: str) -> Sequence[str]:
    return key.split(".")


