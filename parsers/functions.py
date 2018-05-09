import re

from parsers import utils

FUNCTION_RE = re.compile(r'([\+\-@]*.*?)([A-Za-z]\w*)(?=\s*\([^\^])')

RESERVED_TOKENS = {
	"@", "typedef", "#define", "while", "if", "switch"
}

@utils.comments_scrubbed
def parse(content):
    symbols = []
    for m in FUNCTION_RE.finditer(content):
    	# if there's no match, or there is but we see a reserved word as the match or as part of the
    	# string up to the match, we don't add the symbol. this filters out things like @property(...),
    	# while(0) in #defines, etc
        if not m.group(1) or (all([token not in m.group(1) and token != m.group(2) for token in RESERVED_TOKENS])):
            symbols.append(m.group(2))
    return symbols

