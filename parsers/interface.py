import re
from parsers.utils import scrub_comments

INTERFACE_RE = re.compile(r"@interface\s*(\w+)\s*[:]")

def parse(content):
	scrubbed = scrub_comments(content)
	return list(set(INTERFACE_RE.findall(scrubbed)))
