# JDN

Julian Day Number calculations

## background

***calc_jdn( year, month, day )*** computes the Julian Day Number (JDN).  This
is a measure of time that starts on 1 January 4713 BCE and increments
uniformly.  It is used extensively by astronomers because of its
uniformity.  This system deviates from the classical JDN, which
changes at noon rather than at midnight.  This begs the question
of noon *where*, of course.

***calc_ymd( jdn )*** inverts the calculation in julian and returns the tuple
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

## Testing

How do we know that the calc_jdn() and calc_ymd() functions are working
correctly.

The program test3.py iterates through all of the JDNs from 0 to 9999646.

It verifies that calc_jdn(calc_ymd(jdn) == jdn (i.e. that the ymd and
jdn functions are inverses)

In addition, it computes a Day histogram (counts up the number of day
values (1 <= day <= 31) across the entire period.  And it calculates
a Month histogram (counts up the number of month values (1 <= month <= 12)
across the entire period.

These histograms we compare with a first-principles theoretical histogram
that is calculated in nygeek-187, a spreadsheet that replicates a manual
calculation that I conducted in the mid-1980s at CMU.

Beyond test3.py, there are some power tools:

### ymd-range.py

This program accepts two integers a from and a to.  The program starts
a loop at from and runs to to.  It treats each integer as a JDN and
calculates the matching (y, m, d).

There are two output flags:

-j - emits the output as a single JSON object representing a dictionary
mapping the text representations of the integer JDNs to the [y, m, d]
list.

-r - does the same thing as -j, but emits it in "readable" form.  The
result has inadmissible whitespace (newlines) so it can not be directly
imported with json.loads() without preprocessing.

The two output flags are not exclusive, so you can set both of them if
you like.  If you set neither, there will be no output at all.  This is
bad UI design.

### hist-range.py

This program accepts a file name.  The file should contain a JSON object
emitted by ymd-range.py.

It does two things:

1 - it computes the JDN from each (y, m, d) it finds in the data structure
and verifies that it matches the integer rendering of the corresponding
dictionary key.

2 - it computes a day-histogram and the month-histogram the same way that
test3.py does and then emits it as text.

When jdn.py is working correctly with no bugs, the following will replicate
the results of the test3.py test:

> python3 ymd-range.py -j 0 9999647 > bigrange.json
> python3 hist-range bigrange.json > bigtest.out

When done, bigtest.out and test.reference should be identical.

## To Do

When I wrote the original code I blithely designed it around the
assumption that the work was only of interest in the British Empire
and its successors in the English-speaking world.  This is not the
case, so the calc_jdn() and calc_ymd() functions should be parameterized
by region.  At the very least, we should correctly handle the 1582
October 4 cutover to the new style calendar for the main Gregorian
reform as well as the 1752 September 2 cutover for the English-speaking
world.
