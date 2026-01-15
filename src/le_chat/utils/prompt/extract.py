from pathlib import Path
import re
from typing import Iterable


RE_MATCH_FILE_PROMPT = re.compile(r"@(\S+)|@\"(.*)\"")


def extract_paths_from_prompt(prompt: str) -> Iterable[tuple[str, int, int]]:
    """Find file syntax in prompts.

    Args:
        prompt: A line of prompt.

    Yields:
        A tuple of (PATH, START, END).
    """
    for match in RE_MATCH_FILE_PROMPT.finditer(prompt):
        path, quoted_path = match.groups()
        yield (path or quoted_path, match.start(0), match.end(0))


def validate_input_files(prompt: str):
    for path, _, _ in extract_paths_from_prompt(prompt):
        file_path = Path(path)
        if not file_path.exists() or not file_path.is_file:
            return False, f"{file_path} File not found."
    
    return True, "All Files Found"
     

if __name__ == "__main__":
    prompt = """This is a new thing that I'm testing let's see how it
works. There is a file @file/file.py and I will see how
the printing will happen
    """

    # Replace all file paths with the special character <special>
    result = []
    last_index = 0
    for path, a, b in extract_paths_from_prompt(prompt):
        result.append(prompt[last_index:a])
        result.append("<special>")
        last_index = b
    result.append(prompt[last_index:])
    replaced_prompt = "".join(result)

    print(replaced_prompt)
    print(type(replaced_prompt))

    print(f"Validation: {validate_input_files(prompt)}")