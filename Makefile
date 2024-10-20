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
PYLINT := ${PYTHON} -m pylint

DIRS := "."
HOME := "/Users/marc"
DIRPATH := "${HOME}/projects/j/julian/"

SOURCE = \
	jdn.py \
	test3.py

FILES = \
	${SOURCE} \
	.gitignore \
	Makefile \
	README.md \
	pylintrc \
	test.reference

TESTS = \
	test.out

listings: ${SOURCE}
	echo ${SOURCE}
	enscript -b '${DIRPATH}' -p- -G ${SOURCE} | ps2pdf - listings.pdf

.PHONY: test
test:
	rm -f ${TESTS}
	echo 'Testing python library ...'
	${MAKE} test.out
	echo 'done.'

test.out: test3.py jdn.py
	${PYTHON} ./test3.py > test.out
	- diff test.out test.reference

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

