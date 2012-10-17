TOP=$(shell pwd)
export PYTHONPATH:=$(TOP)/src:$(TOP)/tests:$(PYTHONPATH)

test:
	python 'tests/VideoWrapperTest.py'
