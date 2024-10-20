#!/usr/bin/python

""" nailuj.py

Compute the Gregorian date for a JDN.  Accept a JDN in the command
line argument and return Y, M, and D

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

    engine = JulianDate(0)
    engine.set_ymd(today_year, today_month, today_day)
    today_jdn = engine.get_jdn()

    program_name = sys.argv[0]
    # print "program_name: " + program_name

    parser = argparse.ArgumentParser(description='Accept a JDN.')

    parser.add_argument('jdn', type=int, nargs='?',\
            default=today_jdn, help='Julian Day Number')

    args = parser.parse_args()
    engine.set_jdn(args.jdn)

    (y, m, d) = engine.get_ymd()
    daynames = [
        "Sunday",
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday"
    ]
    dayname = daynames[engine.get_dow()]
    monthnames = [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December"
            ]
    monthname = monthnames[m]

    print(f"JDN is: {engine.get_jdn()}")
    print(f"Date is: {dayname}, {str(d)} {monthname} {y}")

if __name__ == '__main__':
    main()
