import re
from parsers.utils import scrub_comments

PROTOCOL_RE = re.compile(r"@protocol\s*(\w+)\s*[:\<\s]")

def parse(content):
	scrubbed = scrub_comments(content)
	return list(set(PROTOCOL_RE.findall(scrubbed)))