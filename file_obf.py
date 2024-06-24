#!/usr/bin/env python3

from argparse import ArgumentParser
from getpass import getpass
from pathlib import Path

from obf import obf


if __name__ == "__main__":
    argp = ArgumentParser()
    argp.add_argument("input", help="Input file", type=Path)
    argp.add_argument("output", help="Output file", type=Path)
    argp.add_argument("-d", "--decrypt", help="Decrypt", action="store_true")
    argp.add_argument("-i", "--iterations", help="Iterations (default: 4)", type=int, default=4)
    argp.add_argument("-p", "--processes", help="Parallel processes (default: 4)", type=int, default=4)
    args = argp.parse_args()
    assert args.processes > 0
    key = getpass("Key: ").encode()
    with args.input.open("rb") as i:
        with args.output.open("wb") as o:
            o.truncate(0)
            o.seek(0)
            o.write(
                obf(i.read(), key, decrypt=args.decrypt, iterations=args.iterations, processes=args.processes)
            )
            o.flush() # for good measure
