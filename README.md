MultipartPostHandlerPy3K
========================

About
-----
MultipartPostHandler is a handler for urllib.request that enables multipart/form-data POSTing. The handler is only available for Python 3.x.

Example
-------
```python
# Uploading a file to a web page

import urllib.request
import MultipartPostHandler

opener = urllib.request.build_opener(MultipartPostHandler.MultipartPostHandler())

params = {
  "username": "john_smith",
  "password": "12345",
  "file": open("foobar.baz", "rb")
}

response = opener.open("http://examplewebsite.com/upload/", params)
```
