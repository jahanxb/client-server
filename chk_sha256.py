#!/usr/bin/python3
# Example of how to verify an SHA-256 checksum file using Python.
# Usage: python sha256check.py sha256sum.txt
import hashlib
import re
import sys

# This regular expression matches a line containing a hexadecimal
# hash, spaces, and a filename. Parentheses create capturing groups.
r = re.compile(r'(^[0-9A-Fa-f]+)\s+(\S.*)$')


def check(filename, expect):
    """Check if the file with the name "filename" matches the SHA-256 sum
    in "expect"."""
    h = hashlib.sha256()
    # This will raise an exception if the file doesn't exist. Catching
    # and handling it is left as an exercise for the reader.
    with open(filename, 'rb') as fh:
        # Read and hash the file in 4K chunks. Reading the whole
        # file at once might consume a lot of memory if it is
        # large.
        while True:
            data = fh.read(4096)
            if len(data) == 0:
                break
            else:
                h.update(data)
    return expect == h.hexdigest()


if __name__ == '__main__':
    with open('dataset_1/2 (1).jpg','rb') as fh:
        for line in fh:
            print(line)
            m = r.match(line)

            #m = line.hex()
            if m:
                m.group(1)
                checksum = m.group(1)
                filename = m.group(2)
                if check(filename, checksum):
                    print(f'{filename}: OK')
                else:
                    print(f'{filename}: BAD CHECKSUM')


