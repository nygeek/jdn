# JDN

Julian Day Number calculations

## background

***calcJDN( year, month, day )*** computes the Julian Day Number (JDN).  This
is a measure of time that starts on 1 January 4713 BCE and increments
uniformly.  It is used extensively by astronomers because of its
uniformity.  This system deviates from the classical JDN, which
changes at noon rather than at midnight.  This begs the question
of noon *where*, of course.

***calcYMD( jdn )*** inverts the calculation in julian and returns the tuple
( year, month, day ) corresponding to the proffered jdn.  Note that this
implementation of the calculator assumes that the switch from the old
Julian calendar to the Gregorian calendar took place on 2 September 1752,
which is correct by-and-large for the English-speaking world.

In much of the rest of the world the change happened on 15 October 1582,
during the papacy of Gregory the XIII, for whom the Gregorian Calendar
is named.

The Julian Day Number is based on the work of Joseph Scaliger,
a scholar who proposed it at the time of the Gregorian calendar reform.
He named the system for his father Julius Caesar Scaliger, also a noted
scholar.
