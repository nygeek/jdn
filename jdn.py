#!/usr/bin/python

# Julian Day Number object

# $Id: jdn.py,v 1.5 2022/03/09 22:11:27 marc Exp marc $

#
# calcJDN( year, month, day ) computes the Julian Day Number (JDN).  This
# is a measure of time that starts on 1 January 4713 BCE and increments
# uniformly.  It is used extensively by astronomers because of its
# uniformity.  This system deviates from the classical JDN, which
# changes at noon rather than at midnight.  This begs the question
# of noon *where*, of course.
#
# calcYMD( jdn ) inverts the calculation in julian and returns the tuple
# ( year, month, day ) corresponding to the proffered jdn.  Note that this
# implementation of the calculator assumes that the switch from the old
# Julian calendar to the Gregorian calendar took place on 2 September 1752,
# which is correct by-and-large for the English-speaking world.
#
# In much of the rest of the world the change happened on 15 October 1582,
# during the papacy of Gregory the XIII, for whom the Gregorian Calendar
# is named.
#
# The Julian Day Number is based on the work of Joseph Scaliger,
# a scholar who proposed it at the time of the Gregorian calendar reform.
# He named the system for his father Julius Caesar Scaliger, also a noted
# scholar.
#

#
# 2008-12-01 add the getDOW() method to return the Day-of-Week number

class jdn:

  # Regular year [0] Leap year [1]
  TotLen = [
    [ 0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 365 ],
    [ 0, 31, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335, 366 ] ]

  MonthName = [
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
  MonthLength = [
    [ 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 ],
    [ 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 ] ]

  def __init__(self, y_or_jdn, m=None, d=None ):
    if ( m is None and d is None ):
      self.setJDN( y_or_jdn )
    elif ( d is None ):
      raise TypeError, "Call with one or three arguments."
    else:
      self.setYMD( y_or_jdn, m, d )

  def setJDN( self, jdn ):
    self.jdn = jdn
    self.jdnFlag = True
    self.ymdFlag = False

  def setYMD( self, y, m, d ):
    self.y = y
    self.m = m
    self.d = d
    self.jdnFlag = False
    self.ymdFlag = True

  # How can we get here?  If we did a setJDN as our initialization, then
  # we had better do a calcYMD before we set the year, month, or day
  def setYear( self, y ):
    if not self.ymdFlag:
      self.calcYMD()
    self.y = y
    self.jdnFlag = False
    self.ymdFlag = True

  def setMonth( self, m ):
    if not self.ymdFlag:
      self.calcYMD()
    self.m = m
    self.jdnFlag = False
    self.ymdFlag = True

  def setDay( self, d ):
    if not self.ymdFlag:
      self.calcYMD()
    self.d = d
    self.jdnFlag = False
    self.ymdFlag = True

  def getYear( self ):
    if not self.ymdFlag:
      self.calcYMD()
    return self.y
    # Note that we can never have an instantiated JDN
    # without at least one of jdnFlag or ymdFlag set.

  def getMonth( self ):
    if not self.ymdFlag:
      self.calcYMD()
    return self.m

  def getMonthName( self ):
    if not self.ymdFlag:
      self.calcYMD()
    return jdn.MonthName[ self.m - 1 ]

  def getMonthLength( self ):
    if not self.jdnFlag:
      self.calcJDN()
    if not self.ymdFlag:
      self.calcYMD()
    return jdn.MonthLength[ self.leap ][ self.m - 1 ]

  def getDay( self ):
    if not self.ymdFlag:
      self.calcYMD()
    return self.d

  def getLeap( self ):
    if not self.ymdFlag:
      self.calcYMD()
    else:
      self.calcJDN()
      # This is potentially overkill.  To avoid this we would have
      # to distinguish between setting YMD from the setYMD()
      # method and calculating it using the calcYMD() method.
      self.calcYMD()
    return self.leap

  def getJDN( self ):
    if not self.jdnFlag:
      self.calcJDN()
    return self.jdn

  def getDOW( self ):
    if not self.jdnFlag:
      self.calcJDN()
    return ( self.jdn + 1 ) % 7
    # this way 0 -> Sunday, 1 -> Monday, 2 > Tuesday, ..., 6 -> Sunday

  def getYMD( self ):
    if not self.ymdFlag:
      self.calcYMD()
    return ( self.y, self.m, self.d )

  def calcJDN( self ):
    # Day 0 of JDN numbering is 1 January 4713 BCE
    y0 = self.y + 4712
    yd = 365 * y0 + ( y0 / 4 )
    self.leap = ( y0 % 4 ) == 0
    if self.leap:
      yd = yd - 1
    md = jdn.TotLen[ self.leap ][ self.m - 1 ]
    self.jdn = yd + md + self.d
    # in the British Empire and successors, 2 September 1752
    if ( self.jdn > 2361221 ):
      y0 = self.y - 300
      if ( self.m <= 2 ):
        y0 = y0 - 1
      self.jdn = self.jdn - ( ( ( y0 / 100 ) * 3 ) / 4 ) - 1
    self.jdnFlag = True

  def calcYMD( self ):

    # 1684595 is the JDN for 3 March -100.  146097 is the number of days
    #   in 400 years in the new style calendar
    # 2361221 is the JDN for 2 September 1752, the last day of the Julian
    #   (old style) calendar in Britain and its colonies

    workjdn = self.jdn
    if self.jdn > 2361221:
      century = ( ( self.jdn - 1684595 ) * 4 ) / 146097
      workjdn = self.jdn + ( ( century * 3 ) / 4 ) - 2

    yearz = ( workjdn / 1461 ) * 4
    self.d = workjdn % 1461

    #    0 -  365 is year 0, a leap year,   366 days long
    #  366 -  730 is year 1, a normal year, 365 days long
    #  732 - 1096 is year 2, a normal year, 365 days long
    # 1097 - 1461 is year 3, a normal year, 365 days long

    if ( self.d <= 365 ):
      yearsincycle = 0
    elif ( ( 366 <= self.d ) and ( self.d <= 730 ) ):
      self.d = self.d - 366
      yearsincycle = 1
    elif ( ( 731 <= self.d ) and ( self.d <= 1095 ) ):
      self.d = self.d - 731
      yearsincycle = 2
    else:
      self.d = self.d - 1096
      yearsincycle = 3

    yearz = yearz + yearsincycle
    self.y = yearz - 4712

    self.leap = False
    if ( yearsincycle == 0 ):
      if (self.y < 1752 ):
        self.leap = True                 # before 1752 every %4==0 is leap
      elif ( ( self.y % 100 ) == 0 ):
        if ( ( self.y % 400 ) != 0 ):    # century year after 1752
          if ( self.d > jdn.TotLen[ self.leap ][ 2 ] ):
            self.d = self.d - 1          # century year exception
        else:
          self.leap = True               # four-century year
      else:
        self.leap = True                 # after 1752, not a century

    for self.m in range( 0, 13 ):
      if ( self.d < jdn.TotLen[ self.leap ][ self.m ] ): break
    self.d = self.d - jdn.TotLen[ self.leap ][ self.m - 1 ] + 1

    self.ymdFlag = True


def main():
    """Main body."""


if __name__ == '__main__':
    main()
