#!/usr/bin/env python
import web
import tempfile
import os
from random import random
import VideoWrapper
from Client import Client
from web.contrib.template import render_jinja

# We only want the main index
urls = (
  '/', 'Index',
  '/video/(.*)', 'VideoHandler'
)

# Create an app and render context
app = web.application(urls, globals())
render = render_jinja("src/assets", encoding = "utf-8")
directory = tempfile.mkdtemp()

# The main web class
class Index:
  # On GET, we just display the jinja page
  def GET(self):
    return render.index(SplitType = VideoWrapper.SplitType)

  # On POST, we create a client
  def POST(self):
    # Open a temporary file
    file = open("%s/in_%f.dat" % (directory, random()), 'wb')
    inputs = web.input(video = {}, type = {}, start = {}, end = {})
    file.write(inputs['video'].value)

    # Flush the file
    file.flush()
    os.fsync(file.fileno())
    file.close()

    start = None
    end = None

    if len(inputs["start"]) > 0:
      start = int(inputs["start"])

    if len(inputs["end"]) > 0:
      end = int(inputs["end"])

    segments = Client(file.name, int(inputs['type']), start, end).run()
    segmentNames = []

    # Write each segment out (encode: THEO, container: OGG)
    for segment in segments:
      rnd = str(random())
      segmentNames.append("video/%s" % rnd)
      segment.write("%s/out_%s.ogg" % (directory, rnd))

    return render.video(segments = segmentNames)

# Handles requests for videos
class VideoHandler:
  def GET(self, name):
    file = open("%s/out_%s.ogg" % (directory, name), "rb")
    return file.read()

# If we run this file, start the web server
if __name__ == "__main__":
    app.run()
