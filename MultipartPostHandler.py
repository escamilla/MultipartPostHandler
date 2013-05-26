#!/usr/bin/python

####
# 05/2013 modified by Joshua Escamilla <jescamilla@hushmail.com>
# * added support for Python 3.x
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

from email.generator import _make_boundary
from mimetypes import guess_type
from os.path import basename

import sys
PY3K = sys.version > "3"

if PY3K:
	from io import IOBase as BUILTIN_FILE_TYPE
	from urllib.parse import urlencode
	from urllib.request import BaseHandler
else:
	BUILTIN_FILE_TYPE = file
	from urllib import urlencode
	from urllib2 import BaseHandler

__all__ = ["MultipartPostHandler"]

try:
	bytes
except NameError:
	bytes = str

def b(str_or_bytes):
	if not isinstance(str_or_bytes, bytes):
		return str_or_bytes.encode("ascii")
	else:
		return str_or_bytes

NEWLINE = b("\r\n")

def _get_content_type(filename):
	return guess_type(filename)[0] or "application/octet-stream"

class MultipartPostHandler(BaseHandler):
	handler_order = BaseHandler.handler_order - 10

	def _encode_form_data(self, fields, files):
		boundary = _make_boundary()
		data = bytes()

		for name, value in fields:
			data += b("--") + b(boundary) + NEWLINE
			data += b("Content-Disposition: form-data; name=\"%s\"" % name) + NEWLINE
			data += b("Content-Type: text/plain") + NEWLINE
			data += NEWLINE
			data += b(value) + NEWLINE

		for name, fp in files:
			filename = basename(fp.name)
			mimetype = _get_content_type(filename)
			fp.seek(0)

			data += b("--") + b(boundary) + NEWLINE
			data += b("Content-Disposition: file; name=\"%s\"; filename=\"%s\"" %
				(name, filename)) + NEWLINE
			data += b("Content-Type: %s" % mimetype) + NEWLINE
			data += NEWLINE
			data += fp.read() + NEWLINE

		data += b("--") + b(boundary) + b("--") + NEWLINE

		return boundary, data

	def http_request(self, req):
		data = req.data

		if data and isinstance(data, dict):
			fields = []
			files = []
			for key, value in data.items():
				if isinstance(value, BUILTIN_FILE_TYPE):
					files.append((key, value))
				else:
					fields.append((key, value))

			if not files:
				data = urlencode(fields, doseq=True).encode()
			else:
				boundary, data = self._encode_form_data(fields, files)
				req.add_header("Content-Type",
					"multipart/form-data; boundary=\"%s\"" % boundary)
				req.add_header("Content-Length", len(data))

			req.data = data

		return req

	https_request = http_request
