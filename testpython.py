# $Id$

# from Numeric       import shape
from datetime      import date
from getopt        import getopt
from os.path       import basename
from sys           import argv
from time          import time

from jdn import JulianDayNumber

day_histogram = {}
for d in range(1, 32):
    day_histogram[d] = 0

month_histogram = {}
for m in range(1, 13):
    month_histogram[m] = 0;

engine = JulianDayNumber(0)
for j in range( 0, 9999647 ):
    engine.set_jdn(j)
    y, m, d = engine.get_ymd()
    engine.set_year(y)
    k = engine.get_jdn()
    month_histogram[m] += 1
    day_histogram[d] += 1
    if (j != k):
        mm = ('00' + str(m))[-2:]
        dd = ('00' + str(d))[-2:]
        print(f"Error: j: {j} + k: {k} => {j-k} ({y}-{mm}-{dd})")

print("Day:")
for d in dayHistogram.keys():
    print(f"{d}: {dayHistogram[d]}")

print("\nMonth:")
for m in monthHistogram.keys():
    print(f"{d}: {monthHistogram[m]}")
