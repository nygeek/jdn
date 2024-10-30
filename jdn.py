"""
    Julian Day Number class

    $Id$

    Copyright (C) 2024 Marc Donner

"""

# Regular year [0] Leap year [1]
TOT_LEN = [
    [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 365],
    [0, 31, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335, 366]
    ]

MONTH_NAME = [
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

DOW_NAME = [
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday"
    ]

# Regular year [0] Leap year [1]
MONTH_LENGTH = [
    [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
    [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    ]

#
# The Gregorian reform was adopted by Papal action in 1582,
# with 4 October 1582 followed by 14 October 1582, omitting nine
# days.
#
GREGORIAN_NEW_STYLE_JDN = 2299160
GREGORIAN_NEW_STYLE_YEAR = 1582
GREGORIAN_NEW_STYLE_MONTH = 10
GREGORIAN_NEW_STYLE_DAY = 4

#
# The British Empire adopted the new style calendar in 1752,
# with 2 September 1752 followed by 14 September 1752, omitting eleven
# days.
#
BRITISH_NEW_STYLE_JDN = 2361221
BRITISH_NEW_STYLE_YEAR = 1752
BRITISH_NEW_STYLE_MONTH = 9
BRITISH_NEW_STYLE_DAY = 2

# We will use two different two-letter ISO 3166 country codes
# to differentiate between the two calendars.  'gb' for the British
# Empire calendar and 'it' for the original Gregorian calendar.

class JulianDate:
    """Julian Date class."""

    # pylint: disable=too-many-instance-attributes
    # Eight is reasonable in this case.

    def __init__(self, y_or_jdn, m=None, d=None, region='gb'):
        """ initialize """
        self.region = region
        self._y = 0
        self._m = 0
        self._d = 0
        self._jdn = 0
        self.leap = 0
        self.jdn_flag = True
        self.ymd_flag = True
        if m is None and d is None:
            self._jdn = y_or_jdn
            self.calc_ymd()
        elif d is None:
            raise TypeError("Call with one or three arguments.")
        else:
            self._y = y_or_jdn
            self._m = m
            self._d = d
            self.calc_jdn()
            self.leap = self.calc_leap(self._y)


    def get_jdn(self):
        """ get jdn """
        if not self.jdn_flag:
            self.calc_jdn()
        return self._jdn


    def set_jdn(self, value):
        """ set jdn """
        self._jdn = value
        self.jdn_flag = True
        self.ymd_flag = False


    def get_y(self):
        """The year property."""
        if not self.ymd_flag:
            self.calc_ymd()
        return self._y


    def set_y(self, value):
        """The year property."""
        self._y = value
        self.jdn_flag = False
        self.ymd_flag = True


    def get_m(self):
        """The month property."""
        if not self.ymd_flag:
            self.calc_ymd()
        return self._m


    def set_m(self, value):
        """ Set month. """
        self._m = value
        self.jdn_flag = False
        self.ymd_flag = True


    def get_d(self):
        """The day property."""
        if not self.ymd_flag:
            self.calc_ymd()
        return self._d


    def set_d(self, value):
        """ Set day. """
        self._d = value
        self.jdn_flag = False
        self.ymd_flag = True


    def get_month_name(self):
        """ get month name """
        if not self.ymd_flag:
            self.calc_ymd()
        return MONTH_NAME[self._m - 1]


    def get_month_length(self):
        """ get month length """
        if not self.jdn_flag:
            self.calc_jdn()
        if not self.ymd_flag:
            self.calc_ymd()
        return MONTH_LENGTH[self.leap][self._m - 1]


    def get_leap(self):
        """ get leap year? """
        if self.jdn_flag:
            self.calc_ymd()
        return self.leap


    def set_ymd(self, y, m, d):
        """ set ymd """
        self._y = y
        self._m = m
        self._d = d
        self.leap = self.calc_leap(self._y)
        self.jdn_flag = False


    def get_dow(self):
        """ get day of week (dow) """
        if not self.jdn_flag:
            self.calc_jdn()
        return (self._jdn + 1) % 7
        # 0 -> Sunday, 1 -> Monday, ..., 6 -> Sunday


    def get_dow_name(self):
        """ get day of week (dow) """
        if not self.jdn_flag:
            self.calc_jdn()
        return DOW_NAME[(self._jdn + 1) % 7]
        # 0 -> Sunday, 1 -> Monday, ..., 6 -> Sunday


    def get_ymd(self):
        """ get ymd """
        if not self.ymd_flag:
            self.calc_ymd()
        return (self._y, self._m, self._d)


    def calc_jdn(self):
        """ calculate jdn from ymd"""
        #
        # Phase 1 - basic Julian Calendar calculation
        # Day 0 of JDN numbering is 1 January 4713 BCE (-4712)
        #
        y0 = self._y + 4712
        # JDN contribution from completed years: 365.25 * y0
        # y0 must be an integer
        yd = 365 * y0 + y0 // 4
        self.leap = self.calc_leap(self._y)
        if self.leap:
            yd -= 1
        # Now look up days from completed months before this one
        md = TOT_LEN[self.leap][self._m - 1]
        # jdn = days from years (yd) plus days from months (md)
        #       plus days from the current month
        self._jdn = yd + md + self._d
        #
        # Phase 2 - Gregorian Calendar corrections
        #
        #     2299150 is jdn(1582,10,4), the last day of the old-style
        #     calendar in the Catholic countries
        #     2361221 is jdn(1752,9,2), the last day of the old-style
        #     calendar in the British Empire
        #
        # Julian calendar assumes year is 365.25 days long.
        # Year is closer to 365.2422 days long, so after the Gregorian
        # reform (1582-10-05, or 1752-09-02) we need to subtract
        # the accumulated error to correct.  The Gregorian correction
        # eliminates three leap days in every 400 years.
        #
        # Note that the Julian reform in 46 BCE corrected the accumulated
        # error to that point, about 90 days.
        #
	    # Sadly, the Pontifexes, who interpreted the calendar,
	    # misunderstood the leap year rules and inserted leap years
	    # every three years for twelve cycles.  These were corrected
	    # by eliminating leap years for twelve cycles ending in 4 CE,
	    # so we can treat the calendar as being aligned from then
	    # onward.  It still added 0.0078 days per year too many, which
	    # were (mostly) corrected by the Gregorian reform in 1582.  That
        # reform took out 0.0075 days per year, across a 400 year cycle.
        # Of course, that left an error of about 0.0003 day per year.
        #

        if self._jdn > BRITISH_NEW_STYLE_JDN:
            if self._y % 100 == 0 and self._y % 400 != 0:
                self.leap = False
                if self._m <= 2:
                    self._jdn -= 1
            self._jdn -= 1
            y1 = self._y - 300
            if self._m <= 2:
                y1 -= 1
            self._jdn -= ((y1 // 100) * 3) // 4


    def calc_leap(self, y):
        """ Is y a leap year? """
        leap = (y % 4) == 0
        if y > BRITISH_NEW_STYLE_YEAR:
            if (y % 100) == 0 and (y % 400) != 0:
                # Not four century, but century
                leap = False
        return leap


    def calc_ymd(self):
        """ calculate ymd from jdn """

        # 1684595 is the JDN for 3 March -100.
        # 146097 is the number of days in 400 years, new style.
        # 1461 is the number of days in a four-year leap cycle
        # years in the new style calendar.

        # First step, undo the Gregorian leap adjustment so that
        # we can calculate y,m,d more simply.
        #
        # The Julian reform, adopted in 43 BCE, got the calendar
        # and the seasons back into alignment, so the Gregorian
        # adjustment only needs to estimate the corrections back to
        # 100 BCE.
        #

        workjdn = self._jdn
        # print(f"self._jdn: {self._jdn} => workjdn: {workjdn}")

        if self._jdn > BRITISH_NEW_STYLE_JDN:
        # if self._jdn > 2361221:
            century = ((self._jdn - 1684595) * 4) // 146097
            workjdn += ((century * 3) // 4) - 2
            # print(f"century: {century}, workjdn: {workjdn}")

        # How many complete leap cycles have we completed?
        yearz = workjdn // 1461 * 4
        self._d = workjdn % 1461
        # self._d now has the days in the current four-year
        # leap cycle.
        # print(f"after workjdn % 1461: self._d: {self._d}")

        #    0 -  365 is year 0, a leap year,   366 days long
        #  366 -  730 is year 1, a normal year, 365 days long
        #  732 - 1096 is year 2, a normal year, 365 days long
        # 1097 - 1461 is year 3, a normal year, 365 days long

        if self._d <= 365:
            year_in_cycle = 0
        elif 366 <= self._d and self._d <= 730:
            self._d -= 366
            year_in_cycle = 1
        elif 731 <= self._d and self._d <= 1095:
            self._d -= 731
            year_in_cycle = 2
        else:
            self._d -= 1096
            year_in_cycle = 3

        # Now self._d has the day-of-year for *this* year

        yearz += year_in_cycle
        self._y = yearz - 4712

        # print(f"DEBUG: self._y: {self._y}, self._d: {self._d}")
        # print(f"DEBUG: year_in_cycle: {year_in_cycle}")

        # this sets the self.leap value
        self.leap = False
        if year_in_cycle == 0:
            if self._y < BRITISH_NEW_STYLE_YEAR:
                # Old Style = always a leap year
                self.leap = True
            elif self._y % 100 == 0:
                if self._y % 400 != 0:
                    # double exception - NOT a leap year
                    # tweak it AS IF it were a leap year
                    if self._d > TOT_LEN[self.leap][2]:
                        self._d -= 1
                else:
                    # triple exception - a leap year
                    self.leap = True
            else:
                # single exception - regular leap year
                self.leap = True

        # self.d right now is day-of-year (index origin 0) ...
        # we need to figure out the month so that we end up
        # with self.d as day-of-month for the correct month.

        self._m = sum(d <= self._d for d in TOT_LEN[self.leap])
        # print(f"before: self._d: {self._d}")
        self._d -= TOT_LEN[self.leap][self._m - 1]
        self._d += 1
        # print(f"self.leap {self.leap}, self._m: {self._m}")
        # print(f"TOT_LEN[...]: {TOT_LEN[self.leap][self._m - 1]}")
        # print(f"after: self._d: {self._d}")

        self.ymd_flag = True
        return (self._y, self._m, self._d)


def main():
    """Main body."""
    engine = JulianDate(236122)
    testjdns = [2361221, 2361222, 2419512, 2342108]
    for jdn in testjdns:
        engine.set_jdn(jdn)
        (y, m, d) = engine.get_ymd()
        print(f"{jdn} => y: {y}, y: {m}, d: {d}")
        engine.set_ymd(y, m, d)
        jdn2 = engine.get_jdn()
        print(f"y: {y}, y: {m}, y: {d} => {jdn2}")
        print("=====\n")


if __name__ == '__main__':
    main()
