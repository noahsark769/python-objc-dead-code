import re
from parsers.utils import comments_scrubbed

DEFINE_RE = re.compile(r"\#define\s+(\w+).*?\n*")

@comments_scrubbed
def parse(content):
	return list(set(DEFINE_RE.findall(content)))