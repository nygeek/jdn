"""
    Julian Day Number class

    $Id$

    Copyright (C) 2024 Marc Donner

    To Do: finish migrating to Python3

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

# Regular year [0] Leap year [1]
MONTH_LENGTH = [
    [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
    [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    ]

class JulianDate:
    """Julian Date class."""

    def __init__(self, y_or_jdn, m=None, d=None):
        """ initialize """
        self.y = 0
        self.m = 0
        self.d = 0
        self.jdn = 0
        self.leap = 0
        if m is None and d is None:
            self.jdn = y_or_jdn
            self.jdn_flag = True
            self.ymd_flag = False
            self.calc_ymd()
        elif d is None:
            raise TypeError("Call with one or three arguments.")
        else:
            self.y = y_or_jdn
            self.m = m
            self.d = d
            self.calc_jdn()
            self.leap = self.calc_leap(self.y)
            self.jdn_flag = False
            self.ymd_flag = True


    def set_year(self, y):
        """ set year """
        if not self.ymd_flag:
            self.calc_ymd()
        self.y = y
        self.jdn_flag = False
        self.ymd_flag = True


    def set_month(self, m):
        """ set month """
        if not self.ymd_flag:
            self.calc_ymd()
        self.m = m
        self.jdn_flag = False
        self.ymd_flag = True


    def set_day(self, d):
        """ set day """
        if not self.ymd_flag:
            self.calc_ymd()
        self.d = d
        self.jdn_flag = False
        self.ymd_flag = True


    def get_year(self):
        """ get year """
        if not self.ymd_flag:
            self.calc_ymd()
        return self.y
        # Note that we can never have an instantiated JDN
        # without at least one of jdn_flag or ymd_flag set.


    def get_month(self):
        """ get month """
        if not self.ymd_flag:
            self.calc_ymd()
        return self.m


    def get_month_name(self):
        """ get month name """
        if not self.ymd_flag:
            self.calc_ymd()
        return MONTH_NAME[self.m - 1]


    def get_month_length(self):
        """ get month length """
        if not self.jdn_flag:
            self.calc_jdn()
        if not self.ymd_flag:
            self.calc_ymd()
        return MONTH_LENGTH[self.leap][self.m - 1]


    def get_day(self):
        """ get day """
        if not self.ymd_flag:
            self.calc_ymd()
        return self.d


    def get_leap(self):
        """ get leap year? """
        if self.jdn_flag:
            self.calc_ymd()
        return self.leap


    def set_ymd(self, y, m, d):
        """ set jdn """
        self.y = y
        self.m = m
        self.d = d
        self.calc_jdn()
        self.leap = self.calc_leap(self.y)
        self.jdn_flag = False
        self.ymd_flag = True
        return self.jdn


    def set_jdn(self, jdn):
        """ set jdn """
        self.jdn = jdn
        self.jdn_flag = True
        self.ymd_flag = False
        self.calc_ymd()
        return self.jdn


    def get_jdn(self):
        """ get jdn """
        if not self.jdn_flag:
            self.calc_jdn()
        return self.jdn


    def get_dow(self):
        """ get day of week (dow) """
        if not self.jdn_flag:
            self.calc_jdn()
        return (self.jdn + 1) % 7
        # this way 0 -> Sunday, 1 -> Monday, 2 > Tuesday,
        # ..., 6 -> Sunday


    def get_ymd(self):
        """ get ymd """
        if not self.ymd_flag:
            self.calc_ymd()
        return (self.y, self.m, self.d)


    def calc_jdn_new(self):
        """ calculate jdn from ymd"""
        # Cribbed from https://www.hermetic.ch/cal_stud/jdn.htm
        # Attributed to Henry F. Fliegel and Thomas C. Van Flandern.
        y = self.y
        m = self.m
        d = self.d
        self.jdn = \
          (1461 * (y + 4800 + int((m - 14) // 12))) // 4 + \
          (367 * (m - 2 - 12 * int((m - 14) // 12))) // 12 - \
          (3 * ((y + 4900 + (m - 14) // 12) // 100)) // 4 + \
          d - 32075
        return self.jdn


    def calc_jdn(self):
        """ calculate jdn from ymd"""
        #
        # Phase 1 - basic Julian Calendar calculation
        #
        # Day 0 of JDN numbering is 1 January 4713 BCE
        y0 = self.y + 4712
        # JDN contribution just from years: 365.25 * y0
        # y0 must be an integer
        yd = 365 * y0 + y0 // 4
        # Is this leap calculation needed?
        self.leap = self.calc_leap(self.y)
        if self.leap:
            yd -= 1
        # Now look up days from completed months before this one
        md = TOT_LEN[self.leap][self.m - 1]
        # jdn = days from years (yd) plus days from months (md) 
        #       plus days from the current month
        self.jdn = yd + md + self.d
        #
        # Phase 2 - Gregorian Calendar corrections
        #
        #     2299150 is jdn(1582,10,4), the last day of the old-style
        #     calendar in the Catholic countries
        #     2361221 is jdn(1752,9,2), the last day of the old-style
        #     calendar in the British Empire
        #
        # Julian calendar assumes year is 365.25 days long.
        # Year is actually 365.2422 days long, so after the Gregorian
        # reform (1582-10-05, or 1752-09-02) we will need to subtract
        # the accumulated error to correct.  The Gregorian correction
        # eliminates three leap days in every 400 years.
        # Note that the Julian reform in 46 BCE corrected the accumulated
        # error to then.
        # Sadly, the pontifexes misunderstood the leap year rules and
        # inserted leap years every three years for twelve cycles.
        # These were corrected by eliminating leap years for twelve
        # years ending in 4 CE, so we can treat the calendar as being
        # aligned from then onward.  It still added 0.0078 days per year
        # too many, which were corrected by the Gregorian reform in 1582.
        #

        if self.jdn > 2361221:
            if self.y % 100 == 0 and self.y % 400 != 0:
                self.leap = False
                if self.m <= 2:
                    self.jdn -= 1
            self.jdn -= 1
            y1 = self.y - 300
            if self.m <= 2:
                y1 -= 1
            self.jdn -= ((y1 // 100) * 3) // 4

        self.jdn_flag = True
        return self.jdn


    def calc_leap(self, y):
        """ Is y a leap year? """
        leap = (y % 4) == 0
        if y > 1752:
            if (y % 100) == 0 and (y % 400) != 0:
                # Not four century, but century
                leap = False
        return leap


    def calc_ymd_new(self):
        """ calculate ymd from jdn """
        # Cribbed from https://www.hermetic.ch/cal_stud/jdn.htm
        # Attributed to Henry F. Fliegel and Thomas C. Van Flandern.
        l = self.jdn + 68569
        n = (4 * l) // 146097
        l = l - (146097 * n + 3) // 4
        i = (4000 * (l + 1)) // 1461001
        l = l - (1461 * i) // 4 + 31
        j = (80 * l) // 2447
        self.d = l - (2447 * j) // 80
        l = j // 11
        self.m = j + 2 - (12 * l)
        self.y = 100 * (n - 49) + i + l
        self.leap = self.calc_leap(self.y)
        return (self.y, self.m, self.d)


    def calc_ymd(self):
        """ calculate ymd from jdn """
        # 1684595 is the JDN for 3 March -100.
        # 146097 is the number of days in 400
        # years in the new style calendar
        # 2361221 is the JDN for 2 September 1752,
        # the last day of the Julian (old style)
        # calendar in Britain and its colonies

        # this undoes the Gregorian correction, so workjdn
        # would be the date if we still had the Julian calendar
        workjdn = self.jdn
        if self.jdn > 2361221:
            century = ((self.jdn - 1684595) * 4) // 146097
            workjdn += ((century * 3) // 4) - 2

        yearz = workjdn // 1461 * 4
        self.d = workjdn % 1461

        #    0 -  365 is year 0, a leap year,   366 days long
        #  366 -  730 is year 1, a normal year, 365 days long
        #  732 - 1096 is year 2, a normal year, 365 days long
        # 1097 - 1461 is year 3, a normal year, 365 days long

        if self.d <= 365:
            year_in_cycle = 0
        elif 366 <= self.d and self.d <= 730:
            self.d -= 366
            year_in_cycle = 1
        elif 731 <= self.d and self.d <= 1095:
            self.d -= 731
            year_in_cycle = 2
        else:
            self.d -= 1096
            year_in_cycle = 3

        yearz += year_in_cycle
        self.y = yearz - 4712

        # this sets the self.leap value

        # print(f"DEBUG: self.y: {self.y}, self.d: {self.d}")
        # print(f"DEBUG: year_in_cycle: {year_in_cycle}")
        self.leap = False
        if year_in_cycle == 0:
            if self.y < 1752:
                self.leap = True
            elif self.y % 100 == 0:
                if self.y % 400 != 0:
                    # double exception
                    if self.d > TOT_LEN[self.leap][2]:
                        self.d -= 1
                else:
                    # triple exception
                    self.leap = True
            else:
                # single exception
                self.leap = True

        for self.m in range(0, 13):
            if self.d < TOT_LEN[self.leap][self.m]:
                break
        self.d = self.d - TOT_LEN[self.leap][self.m - 1] + 1

        self.ymd_flag = True
        return (self.y, self.m, self.d)


def main():
    """Main body."""
    engine = JulianDate(236122)
    testjdns = [2361221, 2361222, 2419512, 2342108]
    for jdn in testjdns:
        engine.set_jdn(jdn)
        (y, m, d) = engine.get_ymd()
        print(f"{jdn} => y: {y}, y: {m}, y: {d}")
        engine.set_ymd(y, m, d)
        jdn2 = engine.get_jdn()
        print(f"y: {y}, y: {m}, y: {d} => {jdn2}")
        print("=====\n") 

if __name__ == '__main__':
    main()
