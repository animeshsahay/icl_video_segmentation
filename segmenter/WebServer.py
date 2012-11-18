#!/usr/bin/env python
import web
import tempfile
import os
import cv2
from random import random
from Segmenter import Segmenter, SplitType
from Client import Client, directory
from web.contrib.template import render_jinja

# We only want the main index
urls = (
  '/', 'Index',
  '/video/(.*)', 'VideoHandler'
)

# Create an app and render context
app = web.application(urls, globals())
render = render_jinja("segmenter/assets", encoding = "utf-8")

# The main web class
class Index:
  # On GET, we just display the jinja page
  def GET(self):
    return render.index(SplitType = SplitType)

  # On POST, we create a client
  def POST(self):
    # Open a temporary file
    file = open("%s/in_%f.dat" % (directory, random()), 'wb')
    inputs = web.input(video = {}, type = {}, start = {}, end = {}, faces = {})
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

    client = Client(file.name, int(inputs['type']), start = start, end = end)
    segmentNames = client.run(Segmenter(), inputs['faces'] == "on", "THEO", "ogg", False)

    return render.video(segments = segmentNames)

# Handles requests for videos
class VideoHandler:
  def GET(self, name):
    # Initialise wanted variables
    filename = "%s/out_%s" % (directory, name)
    len = os.path.getsize(filename + ".ogg")
    range = web.ctx.env.get("HTTP_RANGE")
    file = open(filename + ".ogg", "rb")

    # Setup the common headers
    web.header("Content-Type", "video/ogg")
    web.header("Accept-Ranges", "bytes");
    web.header("X-Content-Duration", float(open(filename + ".size").read()));

    # If the whole file is wanted, return the whole file
    if not range:
      web.header("Content-Length", len)
      return file.read()

    # Otherwise return partial content
    web.ctx.status = "206 Partial Content"

    # Get the size of the chunck
    _, r = range.split("=")
    f, t = r.split("-")
    f = int(f)

    # "To" doesn't have to be specified. If it isn't, set it.
    if t != "" and int(t) < len:
      t = int(t)
    else:
      t = len - 1

    # We want a positive sized chunk
    assert f < t

    # Setup the correct headers for partial content
    web.header("Content-Length", t - f + 1)
    web.header("Content-Range", "bytes %d-%d/%d" % (f, t, len))

    # Return the chunk
    file.seek(f);
    return file.read()[0:t - f + 1]

# If we run this file, start the web server
if __name__ == "__main__":
    app.run()

def integrateFace(frameNo, frame, faces):
  """Integrates faces into the frame if applicable"""
  for (f, rects) in faces:
    if f == frameNo:
      for (x, y, width, height) in rects:
        cv2.rectangle(frame, (x, y), (x + width, y + height), (255, 0, 0), 2)
  return frame
