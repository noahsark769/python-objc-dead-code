from itertools import chain
from parsers import utils

import re

STRUCT_RE = re.compile(r'struct[^\{]*?\{([^\}]+?)}\W*?(?:(\w+)\W*)?;')
STRUCT_CONTENT_RE = re.compile(r'([A-Za-z]\w*)\s*[:]')

def get_struct_content_symbols(struct_content):
    struct_content = utils.scrub_preprocessor(struct_content)
    finditer = STRUCT_CONTENT_RE.finditer(struct_content)
    return [m.group(1) for m in finditer]

def struct_match_iter(content, regexpr):
    for match in regexpr.finditer(content):
        if match:
            match_content = (match.group(2), match.group(1))
            yield match_content

@utils.comments_scrubbed
def parse(content):
    symbols = []
    for struct_symbol, struct_content in struct_match_iter(content, STRUCT_RE):
        if struct_symbol:
            symbols.append(struct_symbol)
        symbols.extend(get_struct_content_symbols(struct_content))

    return symbols


