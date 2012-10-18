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
  '/', 'Index'
)

# Create an app and render context
app = web.application(urls, globals())
render = render_jinja("src/assets", encoding = "utf-8")
directory = tempfile.mkdtemp()

# The main web class
class Index:
  # On GET, we just display the jinja page
  def GET(self):
    print VideoWrapper.SplitType.__dict__
    return render.index(SplitType = VideoWrapper.SplitType)

  # On POST, we create a client
  def POST(self):
    # Open a temporary file
    file = open("%s/in_%f.dat" % (directory, random()), 'wb')
    inputs = web.input(video={}, type={})
    file.write(inputs['video'].value)

    # Flush the file
    file.flush()
    os.fsync(file.fileno())
    file.close()

    return Client(file.name, int(inputs['type'])).run()

# If we run this file, start the web server
if __name__ == "__main__":
    app.run()
