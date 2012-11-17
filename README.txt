======================
icl_video_segmentation
======================

Imperial College London 3rd Year Group Project - video segmentation and indexing.

Installation
============

To make an installable package:
    make dist
Install with:
    pip install dist/Segmenter-0.0.1.tar.gz

Running in place after git clone
================================

Run this once:
    git submodule init
    git submodule update
Then:
    make desktop

Testing
=======

Use:
    make test
