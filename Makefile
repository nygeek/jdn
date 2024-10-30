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
	echo "PYTHON:" ${PYTHON}
	echo "BASH:" ${BASH}
	echo "HOME:" ${HOME}
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
# PYTHON := python3
PYTHON := $(shell which python3)
PYLINT := ${PYTHON} -m pylint
BASH := $(shell which bash)

DIRS := "."
HOME := $(shell echo ${HOME})
PWD := $(shell pwd)

SOURCE = \
	jdn.py \
	julian.py \
	nailuj.py \
	test3.py \
	ymd-range.py

FILES = \
	${SOURCE} \
	.gitignore \
	Makefile \
	julian.sh \
	nailuj.sh \
	README.md \
	pylintrc \
	test.reference

.PHONY: julian.sh
julian.sh:
	echo '#!'${BASH} > julian.sh
	echo ${PYTHON} ${PWD}/julian.py '$$*' >> julian.sh

.PHONY: nailuj.sh
nailuj.sh:
	echo '#!'${BASH} > nailuj.sh
	echo ${PYTHON} ${PWD}/nailuj.py '$$*' >> nailuj.sh

.PHONY: install
install: julian.sh nailuj.sh
	- rm -f ${HOME}/bin/j3 ${HOME}/bin/n3
	(cd ${HOME}/bin; ln -s ${PWD}/julian.sh j3)
	(cd ${HOME}/bin; ln -s ${PWD}/nailuj.sh n3)

TESTS = \
	test.out

listings: ${SOURCE}
	echo ${SOURCE}
	enscript -b ${PWD} -p- -G ${SOURCE} | ps2pdf - listings.pdf

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

