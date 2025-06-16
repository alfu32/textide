import re
from typing import Optional, Dict, Pattern

from textide.utils.language_extensions import language_patterns

def detect_language(filename: str, content: str) -> str:
    """
    Return the first matching language identifier based on filename or content;
    default to 'markdown'.
    """
    for lang, patterns in language_patterns.items():
        fn_re = patterns["filename"]
        ct_re = patterns["content"]
        if fn_re and fn_re.match(filename):
            return lang
        if ct_re and ct_re.search(content):
            return lang
    return "markdown"