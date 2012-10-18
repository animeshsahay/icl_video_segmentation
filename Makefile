TOP=$(shell pwd)
export PYTHONPATH:=$(TOP)/src:$(TOP)/tests:$(PYTHONPATH)

.PHONY: src

src:
	cd src && python VideoWrapper.py
test: src
	python 'tests/VideoWrapperTest.py'
