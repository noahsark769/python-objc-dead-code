import re
from parsers.utils import comments_scrubbed

CONSTANT_RE = re.compile(r".*?(\w+)[\s\=\d\.]*;")

# TODO: instead of this hack, we should really just import all the other parsers and exclude
# symbols that they match from symbols that CONSTANT_RE matches
def should_exclude_line(line):
	return any([
		"#" in line,
		"typedef" in line,
		"@" in line,
		"}" in line,
		"property" in line,
		"+" in line,
		"-" in line,
		"(" in line,
		":" in line # for structs e.g. unsigned int appendUnits : 1;
	])

OBJC_AT_KEYWORDS = {
	"@interface", "@protocol", "@implementation"
}

@comments_scrubbed
def parse(content):
	lines = content.splitlines()
	symbols = []

	in_at_definition = False

	for line in lines:
		if any(keyword in line for keyword in OBJC_AT_KEYWORDS):
			in_at_definition = True
		if should_exclude_line(line) or in_at_definition:
			continue
		symbols.extend(list(set(CONSTANT_RE.findall(line))))
		if "@end" in line:
			in_at_definition = False

	return symbols