#
# Julian
#
# Makefile for Julian day number calculator
#
# $Id$
#

.PHONY: help
help:
	echo "OS: " ${OS}
	echo "DATE: " ${DATE}
	cat Makefile

clean: *.pyc *.out *.ps *.pdf
	- rm $<

# Make us OS-independent ... at least for MacOS and Linux
OS := $(shell uname -s)
ifeq (Linux, ${OS})
    DATE := $(shell date --iso-8601)
else
    DATE := $(shell date "+%Y-%m-%d")
endif

# Python version
PYTHON := python3
# PYTHON := python2
PYLINT := ${PYTHON} -m pylint

DIRS := "."
HOME := "/Users/marc"
DIRPATH := "${HOME}/projects/j/julian/"

SOURCE = \
		 jdn.py

FILES = \
	${SOURCE} \
	.gitignore \
	Makefile \
	README.md \
	pylintrc \
	testpython \
	testpython.reference

TESTS = \
	testpython.out

listings: ${SOURCE}
	echo ${SOURCE}
	enscript -b '${DIRPATH}' -p- -G ${SOURCE} | ps2pdf - listings.pdf

.PHONY: tests
tests:
	rm -f ${TESTS}
	echo 'Testing python library ...'
	${MAKE} testpython.out
	echo 'done.'

testpython.out: ./testpython jdn.py
	${PYTHON} ./testpython > testpython.out
	diff testpython.out testpython.reference

pylint:
	- ${PYLINT} ${SOURCE}

lint: pylint

# GIT operations

diff: .gitattributes
	git diff

status: ${FORCE}
	git status

# this brings the remote copy into sync with the local one
commit: .gitattributes
	git commit ${FILES}
	git push -u origin main

# This brings the local copy into sync with the remote (main)
pull: .gitattributes
	git pull origin main

log: .gitattributes
	git log --pretty=oneline

