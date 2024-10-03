"""
    Julian Day Number class

    $Id$

    Copyright (C) 2024 Marc Donner

    To Do: finish migrating to Python3

"""

# Regular year [0] Leap year [1]
TOT_LEN = [
    [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 365],
    [0, 31, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335, 366]]

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
    [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]]

class JulianDayNumber:
    """Julian Day Number class."""

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
            self.calc_leap()
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
        self.calc_leap()
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


    def calc_jdn(self):
        """ calculate jdn from ymd"""
        # Day 0 of JDN numbering is 1 January 4713 BCE
        y0 = self.y + 4712
        yd = 365 * y0 + int(y0 / 4)
        self.calc_leap()
        if self.leap:
            yd = yd - 1
        md = TOT_LEN[self.leap][self.m - 1]
        self.jdn = yd + md + self.d
        # in the British Empire and successors, 2 September 1752
        if self.jdn > 2361221:
            y0 = self.y - 300
        # Adjust for January and February in Leap Year
        if self.m <= 2:
            y0 = y0 - 1
        self.jdn = self.jdn - int(((y0 / 100) * 3) / 4) - 1
        self.jdn_flag = True
        return self.jdn


    def calc_leap(self):
        """ Is this a leap year? """
        self.leap = (self.y % 4) == 0
        if self.y > 1752:
            if (self.y % 100) == 0 and (self.y % 400) != 0:
                # Not four century, but century
                self.leap = False
        return self.leap


    def calc_ymd(self):
        """ calculate ymd from jdn """
        # 1684595 is the JDN for 3 March -100.
        # 146097 is the number of days in 400
        # years in the new style calendar
        # 2361221 is the JDN for 2 September 1752,
        # the last day of the Julian (old style)
        # calendar in Britain and its colonies

        workjdn = self.jdn
        if self.jdn > 2361221:
            century = int(((self.jdn - 1684595) * 4) / 146097)
            workjdn = self.jdn + int(((century * 3) / 4) - 2)

        yearz = int(workjdn / 1461) * 4
        self.d = workjdn % 1461

        #    0 -  365 is year 0, a leap year,   366 days long
        #  366 -  730 is year 1, a normal year, 365 days long
        #  732 - 1096 is year 2, a normal year, 365 days long
        # 1097 - 1461 is year 3, a normal year, 365 days long

        if self.d <= 365:
            yearsincycle = 0
        elif 366 <= self.d and self.d <= 730:
            self.d -= 366
            yearsincycle = 1
        elif 731 <= self.d and self.d <= 1095:
            self.d -= 731
            yearsincycle = 2
        else:
            self.d -= 1096
            yearsincycle = 3

        yearz = yearz + yearsincycle
        self.y = yearz - 4712

        # this sets the self.leap value
        self.calc_leap()

        print(f"DEBUG: self.y: {self.y}, self.d: {self.d}")
        print(f"DEBUG: yearsincycle: {yearsincycle}")
        if self.y >= 1752 and yearsincycle == 0 and \
           self.y % 100 == 0 and self.y % 400 != 0:
            if self.d > TOT_LEN[self.leap][2]:
                self.d -= 1

        for self.m in range(0, 13):
            if self.d < TOT_LEN[self.leap][self.m]:
                break
        self.d = self.d - TOT_LEN[self.leap][self.m - 1] + 1

        self.ymd_flag = True
        return (self.y, self.m, self.d)


def main():
    """Main body."""
    engine = JulianDayNumber(2024, 10, 1)
    print(f"JDN(2024, 10, 1): {engine.get_jdn()}")
    engine.set_ymd(-4712, 1, 1)
    print(f"JDN(-4712, 1, 1): {engine.get_jdn()}")
    engine.set_jdn(0)
    (year, month, day) = engine.get_ymd()
    print(f"YMD(0): y: {year}, m: {month}, d: {day}")
    engine.set_jdn(2460585)
    (year, month, day) = engine.get_ymd()
    print(f"YMD(2460585): y: {year}, m: {month}, d: {day}")
    engine.set_jdn(2361221)
    (year, month, day) = engine.get_ymd()
    print(f"YMD(2351221): y: {year}, m: {month}, d: {day}")



if __name__ == '__main__':
    main()
