import sys

WINDOWS_INVALID_CHARS_REPLACEMENTS = [
    ("<", "("),
    (">", ")"),
    (":", ""),
    ('"', ""),
    ("/", ","),
    ("\\", ","),
    ("|", ","),
    ("?", ""),
    ("*", ""),
]
UNIX_INVALID_CHARS_REPLACEMENTS = [("/", ",")]


def get_platform_invalid_characters() -> list[tuple[str, str]]:
    if sys.platform.startswith("win"):
        return WINDOWS_INVALID_CHARS_REPLACEMENTS
    else:
        return UNIX_INVALID_CHARS_REPLACEMENTS
