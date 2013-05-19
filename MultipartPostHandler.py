from email.generator import _make_boundary
from io import FileIO as BUILTIN_FILE_TYPE
from mimetypes import guess_type
from os.path import basename
from urllib.parse import urlencode
from urllib.request import BaseHandler

__all__ = ['MultipartPostHandler']

NEWLINE = b'\r\n'

def _get_content_type(filename):
	return guess_type(filename)[0] or 'application/octet-stream'

class MultipartPostHandler(BaseHandler):
	handler_order = BaseHandler.handler_order - 10

	def _encode_form_data(self, fields, files):
		boundary = _make_boundary()
		boundary_b = boundary.encode()

		data = bytearray()

		for name, value in fields:
			data.extend(b'--' + boundary_b + NEWLINE)
			data.extend('Content-Disposition: form-data; name="{}"' \
				.format(name).encode() + NEWLINE)
			data.extend(b'Content-Type: text/plain' + NEWLINE)
			data.extend(NEWLINE)
			data.extend(value.encode() + NEWLINE)

		for name, fp in files:
			filename = basename(fp.name)
			mimetype = _get_content_type(filename)
			fp.seek(0)

			data.extend(b'--' + boundary_b + NEWLINE)
			data.extend('Content-Disposition: file; name="{}"; filename="{}"' \
				.format(name, filename).encode() + NEWLINE)
			data.extend('Content-Type: {}'.format(mimetype).encode() + NEWLINE)
			data.extend(NEWLINE)
			data.extend(fp.read() + NEWLINE)

		data.extend(b'--' + boundary_b + b'--' + NEWLINE)

		return boundary, data

	def http_request(self, req):
		data = req.data

		if data and isinstance(data, dict):
			fields = []
			files = []
			for k, v in data.items():
				if isinstance(v, BUILTIN_FILE_TYPE):
					files.append((k, v))
				else:
					fields.append((k, v))

			if not files:
				data = urlencode(fields, doseq=True).encode()
			else:
				boundary, data = self._encode_form_data(fields, files)
				req.add_header('Content-Type',
					'multipart/form-data; boundary="{}"'.format(boundary))
				req.add_header('Content-Length', len(data))

			req.data = data

		return req

	https_request = http_request
