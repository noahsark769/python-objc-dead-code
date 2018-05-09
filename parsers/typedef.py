import re

from parsers import utils

TYPEDEF_RE = re.compile(r'typedef[^\(]*\([^\^]*\^\s*([A-Za-z]\w*)(?=[^;]*;)|typedef.*?([A-Za-z]\w*)(?=\W*;)')

@utils.comments_scrubbed
def parse(content):
    result = []
    for match in TYPEDEF_RE.finditer(content):
        result.extend([s for s in match.groups() if s])
    return result
