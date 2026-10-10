import re

def clean_text(text: str) -> str:
    """Normalize text while preserving punctuation important to technical skills."""
    text = text.replace("\u00a0", " ")
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    # Do not strip +, #, or . because these occur in C++, C#, and .NET.
    return text.strip()
