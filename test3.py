# $Id$

from jdn import JulianDate

day_histogram = [0] * 32
month_histogram = [0] * 13
engine = JulianDate(0)

def display(_tag, _array):
    """ display this array """
    print(f"{_tag}")
    for _i in range(0, len(_array)):
        print(f"{_i}: {_array[_i]}")

# display("Day:", day_histogram)

for j in range(0, 9999647):
# for j in range(2361000, 2460598):
# for j in range(2400000, 2401000):
    engine.set_jdn(j)
    (y, m, d) = engine.get_ymd()
    # This does nothing other than force recalculation of
    # JDN when next get_jdn() is called
    engine.set_ymd(y, m, d)
    k = engine.get_jdn()
    month_histogram[m] += 1
    # print(f"+++ d: {d}")
    day_histogram[d] += 1
    if j != k or d == 32:
        print(f"j: {j}")
        print(f"    => y: {y}, m: {m}, d: {d}")
        print(f"        => k: {k}")
        print(f"ERROR: {j-k}")

display("Day:", day_histogram)
print("\n")
display("Month:", month_histogram)
