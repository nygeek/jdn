# Calendar object

# $Id: calendar.py,v 1.1 2008/12/07 14:33:31 marc Exp $

#
# Use the jdn.py object to do calculations of julian day number
# for a given month.
#

#
# Note that the JDN % 7 tells the day of week (dow)
#   0 -> Monday, 1 > Tuesday, ..., 6 -> Sunday
#

#
# A single month calendar can cover six weeks.  Existence proof:
#
#  S  M  T  W  T  F  S
#                    1
#  2  3  4  5  6  7  8
#  9 10 11 12 13 14 15
# 16 17 18 19 20 21 22
# 23 24 25 26 27 28 29
# 30 31
#

from jdn           import jdn

class calendar:

  DateText = [
      "   ",
      " 1 ",
      " 2 ",
      " 3 ",
      " 4 ",
      " 5 ",
      " 6 ",
      " 7 ",
      " 8 ",
      " 9 ",
      "10 ",
      "11 ",
      "12 ",
      "13 ",
      "14 ",
      "15 ",
      "16 ",
      "17 ",
      "18 ",
      "19 ",
      "20 ",
      "21 ",
      "22 ",
      "23 ",
      "24 ",
      "25 ",
      "26 ",
      "27 ",
      "28 ",
      "29 ",
      "30 ",
      "31 "
      ]


  def __init__(self, y, m ):
    self.cal = []
    for w in xrange( 6 ):  # Worst case - a month can touch six separate weeks.
      week = []
      for d in xrange( 7 ):
        week.append( 0 )
      self.cal.append( week )
    self.firstDay = jdn( y, m, 1 )
    for dom in xrange( self.firstDay.getMonthLength() ):
      w = ( dom + self.firstDay.getDOW() ) / 7
      d = ( dom + self.firstDay.getDOW() ) % 7
      self.cal[ w ][ d ] = dom + 1
    return

  def render( self ):
    self.text = []
    head = self.firstDay.getMonthName()
    head += " " + '%d' % self.firstDay.getYear()
    self.text.append( head.center( 21, " " ) )
    self.text.append( "Su Mo Tu We Th Fr Sa " )
    for w in xrange( 6 ):
      weekText = ""
      for d in xrange( 7 ):
        weekText += calendar.DateText[ self.cal[ w ][ d ] ]
      if weekText != "                     ":
        self.text.append( weekText )
    return self.text
