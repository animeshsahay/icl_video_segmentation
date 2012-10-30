ARGS ?=
TOP = $(shell pwd)
export PYTHONPATH := $(TOP)/webpy:$(TOP)/jinja2:$(TOP)/src:$(TOP)/tests:$(PYTHONPATH)

shell:
	rm -f .pystart
	echo "from cv2 import *; from VideoWrapper import *" > .pystart
	PYTHONSTARTUP="./.pystart" python 
	rm -f .pystart

cluster:
	python src/FaceClustering.py res/skyfall.mp4
web:
	python "$(TOP)/src/WebServer.py" ${ARGS}

client:
	python "$(TOP)/src/Client.py" ${ARGS}
desktop:
	python "$(TOP)/src/DesktopClient.py" ${ARGS}

test:
	python -m unittest discover -s 'tests/' -p '*Test.py'
