#!/usr/bin/env python
import web
import tempfile
import VideoWrapper
from web.contrib.template import render_jinja

# We only want the main index
urls = (
  '/', 'Index'
)

# Create an app and render context
app = web.application(urls, globals())
render = render_jinja("src/assets", encoding = "utf-8")

# The main web class
class Index:
  # On GET, we just display the jinja page
  def GET(self):
    print VideoWrapper.SplitType.__dict__
    return render.index(SplitType = VideoWrapper.SplitType)

  # On POST, we create a client
  def POST(self):
    file = tempfile.NamedTemporaryFile()
    file.write(web.input(video={})['video'].value)
    file.flush()
    return Client(file.name, None)

# If we run this file, start the web server
if __name__ == "__main__":
    app.run()
