#!/bin/python

# $Id$

# from Numeric       import shape
from datetime      import date
from getopt        import getopt
from os.path       import basename
from sys           import argv
from time          import time

from jdn           import jdn

dayHistogram = {}
for d in range( 1, 32 ):
  dayHistogram[ d ] = 0

monthHistogram = {}
for m in range( 1, 13 ):
  monthHistogram[ m ] = 0;

for j in range( 0, 9999647 ):
# for j in range( 2400000, 2401000 ):
  z = jdn( j )
  y, m, d = z.getYMD()
  z.setYear( y )
  k = z.getJDN()
  monthHistogram[ m ] = monthHistogram[ m ] + 1
  dayHistogram[ d ] = dayHistogram[ d ] + 1
  if ( j != k ):
    mm = ( '00' + str( m ) )[-2:]
    dd = ( '00' + str( d ) )[-2:]
    print "Error: j: " + str( j ) + " k: " + str( k ) + " => " + str( j - k ) + " (" + str( y ) + "-" + mm + "-" + dd + ")"

print "Day:"
for d in dayHistogram.keys():
  print str( d ) + ": " + str( dayHistogram[ d ] )

print "\nMonth:"
for m in monthHistogram.keys():
  print str( m ) + ": " + str( monthHistogram[ m ] )
