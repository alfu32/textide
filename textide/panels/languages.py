import re
from typing import Optional, Dict, Pattern

language_patterns: Dict[str, Dict[str, Optional[Pattern[str]]]] = {
    # "bash": {
    #     "filename": re.compile(r'^.*\.sh$', re.IGNORECASE),
    #     "content": re.compile(r'#!.*\/(bash|sh)', re.IGNORECASE),
    # },
    # "c": {
    #     "filename": re.compile(r'^.*\.(c|h)$', re.IGNORECASE),
    #     "content": None,
    # },
    # "c-sharp": {
    #     "filename": re.compile(r'^.*\.cs$', re.IGNORECASE),
    #     "content": None,
    # },
    # "cpp": {
    #     "filename": re.compile(r'^.*\.(cpp|cc|cxx|hpp|hh|hxx)$', re.IGNORECASE),
    #     "content": None,
    # },
    # "commonlisp": {
    #     "filename": re.compile(r'^.*\.(lisp|cl)$', re.IGNORECASE),
    #     "content": None,
    # },
    "css": {
        "filename": re.compile(r'^.*\.css$', re.IGNORECASE),
        "content": None,
    },
    # "dockerfile": {
    #     "filename": re.compile(r'^Dockerfile$', re.IGNORECASE),
    #     "content": None,
    # },
    # "dot": {
    #     "filename": re.compile(r'^.*\.(dot|gv)$', re.IGNORECASE),
    #     "content": None,
    # },
    # "elisp": {
    #     "filename": re.compile(r'^.*\.el$', re.IGNORECASE),
    #     "content": None,
    # },
    # "elixir": {
    #     "filename": re.compile(r'^.*\.(ex|exs)$', re.IGNORECASE),
    #     "content": None,
    # },
    # "elm": {
    #     "filename": re.compile(r'^.*\.elm$', re.IGNORECASE),
    #     "content": None,
    # },
    # "erlang": {
    #     "filename": re.compile(r'^.*\.(erl|hrl)$', re.IGNORECASE),
    #     "content": None,
    # },
    # "fortran": {
    #     "filename": re.compile(r'^.*\.(f|for|f90|f95)$', re.IGNORECASE),
    #     "content": None,
    # },
    # "fixed-form-fortran": {
    #     "filename": re.compile(r'^.*\.(f|for)$', re.IGNORECASE),
    #     "content": None,
    # },
    "go": {
        "filename": re.compile(r'^.*\.go$', re.IGNORECASE),
        "content": None,
    },
    # "go-mod": {
    #     "filename": re.compile(r'^go\.mod$', re.IGNORECASE),
    #     "content": None,
    # },
    # "hack": {
    #     "filename": re.compile(r'^.*\.(hh|hack)$', re.IGNORECASE),
    #     "content": None,
    # },
    # "haskell": {
    #     "filename": re.compile(r'^.*\.(hs|lhs)$', re.IGNORECASE),
    #     "content": None,
    # },
    # "hcl": {
    #     "filename": re.compile(r'^.*\.hcl$', re.IGNORECASE),
    #     "content": None,
    # },
    "html": {
        "filename": re.compile(r'^.*\.(html?|xhtml)$', re.IGNORECASE),
        "content": None,
    },
    "java": {
        "filename": re.compile(r'^.*\.java$', re.IGNORECASE),
        "content": None,
    },
    "javascript": {
        "filename": re.compile(r'^.*\.(js|mjs|cjs)$', re.IGNORECASE),
        "content": None,
    },
    # "jsdoc": {
    #     "filename": re.compile(r'^.*\.js$', re.IGNORECASE),
    #     "content": re.compile(r'/\*\*[\s\S]*?\*/\s*@[A-Za-z]+', re.IGNORECASE),
    # },
    "json": {
        "filename": re.compile(r'^.*\.json$', re.IGNORECASE),
        "content": None,
    },
    # "julia": {
    #     "filename": re.compile(r'^.*\.jl$', re.IGNORECASE),
    #     "content": None,
    # },
    # "kotlin": {
    #     "filename": re.compile(r'^.*\.(kt|kts)$', re.IGNORECASE),
    #     "content": None,
    # },
    # "lua": {
    #     "filename": re.compile(r'^.*\.lua$', re.IGNORECASE),
    #     "content": None,
    # },
    # "make": {
    #     "filename": re.compile(r'^(Makefile|makefile|GNUmakefile)$', re.IGNORECASE),
    #     "content": None,
    # },
    "markdown": {
        "filename": re.compile(r'^.*\.(md|markdown)$', re.IGNORECASE),
        "content": None,
    },
    # "ocaml": {
    #     "filename": re.compile(r'^.*\.(ml|mli)$', re.IGNORECASE),
    #     "content": None,
    # },
    # "objc": {
    #     "filename": re.compile(r'^.*\.(m|mm)$', re.IGNORECASE),
    #     "content": None,
    # },
    # "perl": {
    #     "filename": re.compile(r'^.*\.(pl|pm|t)$', re.IGNORECASE),
    #     "content": None,
    # },
    # "php": {
    #     "filename": re.compile(r'^.*\.(php|phtml|inc)$', re.IGNORECASE),
    #     "content": None,
    # },
    "python": {
        "filename": re.compile(r'^.*\.(py|pyw)$', re.IGNORECASE),
        "content": re.compile(r'^#!.*\bpython[0-9.]*\b', re.IGNORECASE),
    },
    # "ql": {
    #     "filename": re.compile(r'^.*\.ql$', re.IGNORECASE),
    #     "content": None,
    # },
    "regex": {
        "filename": re.compile(r'^.*\.regex$', re.IGNORECASE),
        "content": None,
    },
    # "r": {
    #     "filename": re.compile(r'^.*\.r$', re.IGNORECASE),
    #     "content": None,
    # },
    # "rst": {
    #     "filename": re.compile(r'^.*\.rst$', re.IGNORECASE),
    #     "content": None,
    # },
    "ruby": {
        "filename": re.compile(r'^.*\.(rb|ruby)$', re.IGNORECASE),
        "content": None,
    },
    "rust": {
        "filename": re.compile(r'^.*\.rs$', re.IGNORECASE),
        "content": None,
    },
    # "scala": {
    #     "filename": re.compile(r'^.*\.scala$', re.IGNORECASE),
    #     "content": None,
    # },
    "sql": {
        "filename": re.compile(r'^.*\.sql$', re.IGNORECASE),
        "content": None,
    },
    "sqlite": {
        "filename": re.compile(r'^.*\.(sqlite3?|db3?|db)$', re.IGNORECASE),
        "content": None,
    },
    # "toml": {
    #     "filename": re.compile(r'^.*\.toml$', re.IGNORECASE),
    #     "content": None,
    # },
    # "tsq": {
    #     "filename": re.compile(r'^.*\.tsql$', re.IGNORECASE),
    #     "content": None,
    # },
    # "typescript": {
    #     "filename": re.compile(r'^.*\.(ts|tsx)$', re.IGNORECASE),
    #     "content": None,
    # },
    "xml": {
        "filename": re.compile(r'^.*\.(xml)$', re.IGNORECASE),
        "content": None,
    },
    "yaml": {
        "filename": re.compile(r'^.*\.(ya?ml)$', re.IGNORECASE),
        "content": None,
    },
    # "embedded-template": {
    #     "filename": re.compile(r'^.*\.(tmpl|erb|ejs|hbs|mustache)$', re.IGNORECASE),
    #     "content": None,
    # },
}

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