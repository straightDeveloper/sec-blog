import os
import urllib
import webapp2
from handler import Handler
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

blobHandler_url = '/blob';
blobUpload_url = '/blob/upload' 
blobServer_url = '/blob/serve/([^/]+)?'
blob_server_director = '/blob/serve/%s'

class blobHandler(Handler):

	def get(self):
		upload_url = blobstore.create_upload_url(blobUpload_url)

		self.render("blobstore/uploadform.html",postTo=upload_url)


class blobUpload(blobstore_handlers.BlobstoreUploadHandler):
	def post(self):
		upload_files = self.get_uploads('pic')  # 'file' is file upload field in the form
		blob_info = upload_files[0]
		#self.write(blob_info)
		self.redirect(blob_server_director % blob_info.key())

class blobServer(blobstore_handlers.BlobstoreDownloadHandler):
	def get(self, resource):
		resource = str(urllib.unquote(resource))
		blob_info = blobstore.BlobInfo.get(resource)
		self.send_blob(blob_info)


