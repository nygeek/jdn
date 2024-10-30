""" hist-range.py

Accept two integers from and to.  Treat each integer between from and
to as a JDN and compute the YMD for it.  Emit the result as a JSON
object.

"""

from datetime import date
import argparse
import json
import sys
from jdn import JulianDate

def display(_tag, _array):
    """ display this array """
    print(f"{_tag}")
    for _i in range(0, len(_array)):
        print(f"{_i}: {_array[_i]}")


def main():
    """main routine."""
    # program_name = sys.argv[0]
    # print(f"program_name: {program_name}")

    parser = argparse.ArgumentParser( \
        description= \
        'load a JSON object with {jdn: [y,m,d]} pairs and analyze them.')
    parser.add_argument('infile', type=str, nargs='?')
    args = parser.parse_args()

    infile = args.infile
    infileFP = open(infile)
    sample = json.loads(infileFP.read())

    day_histogram = [0] * 32
    month_histogram = [0] * 13

    engine = JulianDate(0)
    for jdn in sample:
        (y, m, d) = sample[jdn]
        day_histogram[d] += 1
        month_histogram[m] += 1
        engine.set_ymd(y, m, d)
        check_jdn = engine.get_jdn()
        if int(jdn) != check_jdn:
            print(f"Mismatch: jdn: {jdn} ymd: {(y,m,d)}")
            print(f"==> check_jdn: {check_jdn}")

    display("Day:", day_histogram)
    print("\n")
    display("Month:", month_histogram)

if __name__ == '__main__':
    main()
