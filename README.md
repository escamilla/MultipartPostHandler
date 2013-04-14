MultipartPostHandlerPy3K
========================
A handler for urllib.request that enables multipart form uploading.
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
