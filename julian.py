#!/usr/bin/python

""" julian.py

Compute the Julian Day Number for a date.  Accept
a date (Y, M, D) on the command line and return the
Julian Day Number.

2024-10-02 - convert to Python3

"""

from datetime import date
import argparse
import sys
from jdn import JulianDate

def main():
    """main routine."""

    # get the current year, month, and day
    today = date.today()
    today_year = today.year
    today_month = today.month
    today_day = today.day

    program_name = sys.argv[0]
    # print "program_name: " + program_name

    parser = argparse.ArgumentParser(description='Accept a date.')

    parser.add_argument('year', type=int, nargs='?',\
            default=today_year, help='Year number')
    parser.add_argument('month', type=int, nargs='?',\
            default=today_month, help='Month number')
    parser.add_argument('day', type=int, nargs='?',\
            default=today_day, help='Day number')

    args = parser.parse_args()

    # print "Year"
    # print args.year
    # print "Month"
    # print args.month
    # print "Day"
    # print args.day

    engine = JulianDate(0)
    engine.set_ymd(args.year, args.month, args.day)
    dow_name = engine.get_dow_name()

    (y, m, d) = engine.get_ymd()
    month_name = engine.get_month_name()
    print(f"Date is: {dow_name}, {str(d)} {month_name} {y}")
    print(f"JDN is: {engine.get_jdn()}")

if __name__ == '__main__':
    main()
