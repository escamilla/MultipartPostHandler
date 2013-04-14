from email.generator import _make_boundary
from io import IOBase as FILE_TYPE
from mimetypes import guess_type
from os.path import basename
from urllib.parse import urlencode
from urllib.request import BaseHandler

__all__ = ['MultipartPostHandler']

CRLF = '\r\n'
CRLF_b = b'\r\n'

def _get_content_type(filename):
	return guess_type(filename)[0] or 'application/octet-stream'

class MultipartPostHandler(BaseHandler):
	handler_order = BaseHandler.handler_order - 10

	def __init__(self, close_file_objs=False):
		self.close_file_objs = close_file_objs

	def _encode_form_data(self, params, files):
		boundary = _make_boundary()
		boundary_b = boundary.encode()

		data = bytearray()

		for name, value in params:
			data.extend(b'--' + boundary_b + CRLF_b)
			data.extend('Content-Disposition: form-data; name="{}"'.format(name).encode() + CRLF_b)
			data.extend(b'Content-Type: text/plain' + CRLF_b)
			data.extend(CRLF_b)
			data.extend(value.encode() + CRLF_b)

		for name, fp in files:
			filename = basename(fp.name)
			mimetype = _get_content_type(filename)
			fp.seek(0)

			data.extend(b'--' + boundary_b + CRLF_b)
			data.extend('Content-Disposition: file; name="{}"; filename="{}"'.format(
				name, filename).encode() + CRLF_b)
			data.extend('Content-Type: {}'.format(mimetype).encode() + CRLF_b)
			data.extend(CRLF_b)
			data.extend(fp.read() + CRLF_b)

			if self.close_file_objs:
				fp.close()

		data.extend(b'--' + boundary_b + b'--' + CRLF_b)

		return boundary, data

	def http_request(self, req):
		data = req.data

		if data and isinstance(data, dict):
			params = []
			files = []
			for k, v in data.items():
				if isinstance(v, FILE_TYPE):
					files.append((k, v))
				else:
					params.append((k, v))

			if not files:
				data = urlencode(params, doseq=True).encode()
			else:
				boundary, data = self._encode_form_data(params, files)
				req.add_header('Content-Type',
					'multipart/form-data; boundary="{}"'.format(boundary))
				req.add_header('Content-Length', str(len(data)))

			req.data = data
		return req

	https_request = http_request
