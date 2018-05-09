from itertools import chain
from parsers import utils

import re

ENUM_CONTENT_RE = re.compile(r'([A-Za-z]\w*)')
NS_ENUM_RE = re.compile(r'NS_ENUM[^\(]*?\(\W*?\w+[^,]*?,\W*?(\w+)[^\)]*?\)[^\{]*?\{([^\}]+?)}[^;]*?;')
NS_OPTIONS_RE = re.compile(r'NS_OPTIONS[^\(]*?\(\W*?\w+[^,]*?,\W*?(\w+)[^\)]*?\)[^\{]*?\{([^\}]+?)}[^;]*?;')
ENUM_RE = re.compile(r'enum[^\{]*?\{([^\}]+?)}\W*?(?:(\w+)\W*)?;')

def get_enum_content_symbols(enum_content):
    enum_content = utils.scrub_preprocessor(enum_content)
    finditer = ENUM_CONTENT_RE.finditer(enum_content)
    return [m.group(1) for m in finditer]

def enum_match_iter(content, regexpr, old_style):
    for match in regexpr.finditer(content):
        if match:
            match_content = (match.group(1), match.group(2))
            if old_style:
                match_content = tuple(reversed(match_content))
            yield match_content

@utils.comments_scrubbed
def parse(content):
    symbols = []
    enum_iter = chain(enum_match_iter(content, NS_ENUM_RE, False),
                      enum_match_iter(content, NS_OPTIONS_RE, False),
                      enum_match_iter(content, ENUM_RE, True))
    for enum_symbol, enum_content in enum_iter:
        if enum_symbol:
            symbols.append(enum_symbol)
        symbols.extend(get_enum_content_symbols(enum_content))

    return symbols


