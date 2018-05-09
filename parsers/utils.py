import re

SINGLE_LINE_RE = re.compile(r"\/\/.*\n")
MULTI_LINE_RE = re.compile(r"\/\*.*?\*\/", re.DOTALL)
PREPROCESSOR_RE = re.compile(r"\#.*\n")

def scrub_comments(string):
    result = SINGLE_LINE_RE.sub("\n", string)
    result = MULTI_LINE_RE.sub("", result)
    return result

def scrub_preprocessor(string):
    result = PREPROCESSOR_RE.sub("\n", string)
    return result

def comments_scrubbed(func):
    def scrub_and_call(string):
        return func(scrub_comments(string))
    return scrub_and_call
