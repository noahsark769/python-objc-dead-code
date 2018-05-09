from itertools import chain
from multiprocessing import Pool
from contextlib import closing

import argparse
import os
from parsers import enum, define, constant, functions, interface, protocol, typedef


PARSERS = [
    enum,
    define,
    constant,
    functions,
    interface,
    protocol,
    typedef,
]

def iter_files(dirs, extensions=None):
    extensions = extensions or set()
    path_iters = chain(*[os.walk(d) for d in dirs])
    for dirpath, _, filenames in path_iters:
        full_path = os.path.abspath(dirpath)
        for filename in filenames:
            if os.path.splitext(filename)[-1] in extensions:
                yield os.path.join(full_path, filename)

def get_symbols(header_path):
    with open(header_path, 'r') as header:
        content = header.read()
    return header_path, list(chain(*(parser.parse(content) for parser in PARSERS)))

def main():
    parser = argparse.ArgumentParser(description='Tool to find unused code')
    parser.add_argument('dirs', nargs='+')
    parser.add_argument('--check', action="store_true")
    args = parser.parse_args()

    with closing(Pool(4)) as p:
        symbol_info = list((p.map(get_symbols, iter_files(args.dirs, {'.h'}))))

    if args.check:
        for filename, symbols in symbol_info:
            for symbol in symbols:
                if len(symbol) == 0 or len(symbol) == 1:
                    print "Problem: %s in %s" % (symbol, filename)
                if any(kw in symbol for kw in {"@", "void", "while", "if", "switch", "property", "interface", "protocol", "class", "implementation", "typedef", "#", "define"}):
                    print "Problem: %s in %s" % (symbol, filename)
    return os.EX_OK

if __name__ == '__main__':
    exit(main())
