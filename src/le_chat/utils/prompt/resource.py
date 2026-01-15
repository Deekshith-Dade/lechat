from dataclasses import dataclass
import mimetypes
from pathlib import Path
from typing import Literal

ResourceType = Literal["text", "image", "audio"]


@dataclass
class Resource:
    path: Path
    mime_type: str
    resource_type: ResourceType
    text: str | None
    data: bytes | None


class ResourceError(Exception):
    """An error occurred reading a resource."""


class ResourceNotRelative(ResourceError):
    """Attempted to read a resource, not in the project directory."""


class ResourceReadError(ResourceError):
    """Failed to read the resource."""


class ResourceUnsupportedType(ResourceError):
    """Unsupported file type."""


# Mime types that should be read as text
TEXT_MIME_PREFIXES = ("text/",)
TEXT_MIME_TYPES = {
    "application/json",
    "application/xml",
    "application/javascript",
    "application/typescript",
    "application/x-python",
    "application/x-sh",
    "application/toml",
    "application/yaml",
}

# Mime types that should be read as binary (images, audio)
IMAGE_MIME_PREFIXES = ("image/",)
AUDIO_MIME_PREFIXES = ("audio/",)


def load_resource(path: Path) -> Resource:
    """Load a resource from the project directory.

    Only text, image, and audio files are supported.

    Args:
        path: Path to the resource file.

    Returns:
        A Resource with either text or data populated.

    Raises:
        ResourceReadError: If the file cannot be read.
        ResourceUnsupportedType: If the file type is not text, image, or audio.
    """
    resource_path = path

    mime_type, _ = mimetypes.guess_file_type(resource_path)
    if mime_type is None:
        mime_type = "text/plain"  # Default to text for unknown types

    data: bytes | None = None
    text: str | None = None

    # Determine the resource type
    resource_type: ResourceType
    if mime_type.startswith(IMAGE_MIME_PREFIXES):
        resource_type = "image"
    elif mime_type.startswith(AUDIO_MIME_PREFIXES):
        resource_type = "audio"
    elif mime_type.startswith(TEXT_MIME_PREFIXES) or mime_type in TEXT_MIME_TYPES:
        resource_type = "text"
    else:
        raise ResourceUnsupportedType(
            f"Unsupported file type {mime_type!r} for {str(path)!r}. "
            "Only text, image, and audio files are allowed."
        )

    try:
        if resource_type in ("image", "audio"):
            data = resource_path.read_bytes()
        else:
            text = resource_path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        raise ResourceReadError(f"File not found {str(path)!r}")
    except Exception as error:
        raise ResourceReadError(f"Failed to read {str(path)!r}; {error}")

    resource = Resource(
        resource_path,
        mime_type=mime_type,
        resource_type=resource_type,
        text=text,
        data=data,
    )
    return resource