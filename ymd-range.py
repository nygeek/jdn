#!/usr/bin/python

""" ymd-range.py

Accept two integers from and to.  Treat each integer between from and
to as a JDN and compute the YMD for it.  Emit the result as a JSON
object.

"""

from datetime import date
import argparse
import json
import sys
from jdn import JulianDate

def main():
    """main routine."""
    # program_name = sys.argv[0]
    # print(f"program_name: {program_name}")

    parser = argparse.ArgumentParser( \
        description= \
        'Accept from and to JDNs.  Report out the YMD for each.')
    parser.add_argument('-r', action='store_true')
    parser.add_argument('-j', action='store_true')
    parser.add_argument('fff', type=int, default=0, nargs='?')
    parser.add_argument('ttt', type=int, default=1461, nargs='?')
    args = parser.parse_args()

    from_index = args.fff
    to_index = args.ttt
    engine = JulianDate(0)

    # print(f"\n# from_index: {from_index}, to_index: {to_index}\n")

    result = {}
    if args.r:
        print("{")
    for jdn in range(from_index, to_index):
        engine.set_jdn(jdn)
        (y, m, d) = engine.get_ymd()
        _result = {}
        _result[str(jdn)] = [y, m, d]
        result[str(jdn)] = [y, m, d]
        _z = json.dumps(_result, separators=(',',':'), indent=None)
        if args.r:
            print(f"{_z},")
    if args.r:
        print("}")

    if args.j:
        print(json.dumps(result, indent=None))

if __name__ == '__main__':
    main()
