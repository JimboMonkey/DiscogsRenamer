# These are mostly only invalid filename characters on Windows
# systems, with only the forward slash applying to Unix systems
# However I've decided to not make the list platform dependent
# to make smoother cross platform shares of tracks easier and
# the fact that most characters are rarely used in filenames anyway
INVALID_CHARS_REPLACEMENTS = [
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

MAX_FILENAME_LENGTH = 255


# Return a shallow copy to avoid risk of mutation
def get_invalid_filename_characters() -> list[tuple[str, str]]:
    return list(INVALID_CHARS_REPLACEMENTS)
