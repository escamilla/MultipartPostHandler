MultipartPostHandler
====================

About
-----
MultipartPostHandler is a handler for Python's urllib2 and urllib.request
modules that enables multipart form posting.

This program is a modified version of Will Holcomb's MultipartPostHandler
module, available at https://pypi.python.org/pypi/MultipartPostHandler/.

The original module has been modified primarily to add support for Python 3.x.

License
-------
This program is licensed under the GNU Lesser General Public License v3.
See https://www.gnu.org/licenses/lgpl.html for the full license text.

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

