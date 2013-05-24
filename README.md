MultipartPostHandlerPy3K
========================

About
-----
MultipartPostHandlerPy3K is a handler for Python 3.x's urllib.request module that enables multipart/form-data POSTing.

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
