MultipartPostHandler
====================

About
-----
MultipartPostHandler is a handler for urllib2 and urllib.request that enables multipart form posting. This module is a modified version of the original MultipartPostHandler by Will Holcomb, which is available at https://pypi.python.org/pypi/MultipartPostHandler/. The original module has been modified primarily to add support for Python 3.x.

Example
-------
```python
# Uploading a file to a web page

import urllib.request
from MultipartPostHandler import MultipartPostHandler

opener = urllib.request.build_opener(MultipartPostHandler())

fp = open("foobar.baz", "rb")

params = {
    "username": "john_smith",
    "password": "12345",
    "file": fp
}

response = opener.open("http://examplewebsite.com/upload/", params)

# Don't forget to close your files
fp.close()
```
