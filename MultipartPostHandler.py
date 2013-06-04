#!/usr/bin/python

####
# 06/2013 modified by Joshua Escamilla <jescamilla@hushmail.com>
# * added support for Python 3.x
#
##
# available at
# https://github.com/jryane/MultipartPostHandler

####
# 02/2006 Will Holcomb <wholcomb@gmail.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
##
# available at
# https://pypi.python.org/pypi/MultipartPostHandler/

__all__ = ["MultipartPostHandler"]

from email.generator import _make_boundary
from mimetypes import guess_type
from os.path import basename

import sys
PY3K = sys.version > "3"

if PY3K:
    from io import IOBase as FILE_TYPE
    from urllib.parse import urlencode
    from urllib.request import BaseHandler
else:
    FILE_TYPE = file
    from urllib import urlencode
    from urllib2 import BaseHandler

try:
    bytes
except NameError:
    bytes = str

def b(str_or_bytes):
    if not isinstance(str_or_bytes, bytes):
        return str_or_bytes.encode("ascii")
    else:
        return str_or_bytes

NEWLINE = "\r\n"

def _get_content_type(filename):
    return guess_type(filename)[0] or "application/octet-stream"

class MultipartPostHandler(BaseHandler):
    handler_order = BaseHandler.handler_order - 10

    def _encode_form_data(self, fields, files):
        boundary = _make_boundary()
        parts = []

        for name, value in fields:
            parts.append(b("--%s" % boundary))
            parts.append(b("Content-Disposition: form-data; name=\"%s\""
                                                                   % name))
            parts.append(b("Content-Type: text/plain"))
            parts.append(b(""))
            parts.append(b(value))

        for name, fp in files:
            filename = basename(fp.name)
            mimetype = _get_content_type(filename)
            fp.seek(0)

            parts.append(b("--%s" % boundary))
            parts.append(b("Content-Disposition: file; name=\"%s\"; " \
                           "filename=\"%s\"" % (name, filename)))
            parts.append(b("Content-Type: %s" % mimetype))
            parts.append(b(""))
            parts.append(fp.read())

        parts.append(b("--%s--" % boundary))
        data = b(NEWLINE).join(parts)

        return boundary, data

    def http_request(self, req):
        data = req.data

        if data and isinstance(data, dict):
            fields = []
            files = []

            for key, value in data.items():
                if isinstance(value, FILE_TYPE):
                    files.append((key, value))
                else:
                    fields.append((key, value))

            if files:
                boundary, data = self._encode_form_data(fields, files)
                req.add_header("Content-Type", "multipart/form-data; " \
                               "boundary=\"%s\"" % boundary)
                req.add_header("Content-Length", len(data))
            else:
                data = urlencode(fields, doseq=True)

            req.data = data

        return req

    https_request = http_request
