ARGS ?=
TOP = $(shell pwd)
export PYTHONPATH := $(TOP)/enzyme:$(TOP)/src:$(TOP)/tests:$(PYTHONPATH)

shell:
	rm -f .pystart
	echo "from cv2 import *; from VideoWrapper import *" > .pystart
	PYTHONSTARTUP="./.pystart" python 
	rm -f .pystart

cluster:
	python src/FaceClustering.py res/skyfall.mp4

client:
	python "$(TOP)/src/Client.py" ${ARGS}
desktop:
	python "$(TOP)/src/DesktopClient.py" ${ARGS}

test:
	python -m unittest discover -s 'tests/' -p '*Test.py'
