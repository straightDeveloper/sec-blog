from google.appengine.ext import db
import webapp2
from handler import Handler

img_saver_url = "/test/img_saver";
img_handler_url = r"/test/img_handler/(\d+)";
img_adder_url = "/test/img_adder";

class Site_Image(db.Model):
	img = db.BlobProperty();

	def get_id(self):
		return self.key().id();


class img_handler(Handler):
	def get(self,img_id):
		img_id = int(img_id);
		img=Site_Image.get_by_id(img_id);
		if img:
			self.response.headers['Content-Type'] = 'image'
			self.response.out.write(img.img);

		else:
			self.error(404);

class img_adder(Handler):
	def post(self):
		img_file = str(self.request.get("pic"));
		
		img = Site_Image();
		img.img = db.Blob(img_file);
		img.put();
		self.redirect("/test/img_handler/%s"%img.get_id())
		#self.write("%s"%img.get_id());

class img_saver(Handler):
	def get(self):
		self.render("img_handler.html",postTo=img_adder_url);

class img_direct_adder(Handler):
	def post(self):
		pic = self.request.get('pic');
		self.response.headers['Content-Type'] = 'image/png'
		self.response.out.write(pic);


import os
import urllib

from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

class blobHandler(Handler):

	def get(self):
		upload_url = blobstore.create_upload_url('/blob/upload')

		self.render("blobstore/uploadform.html",postTo=upload_url)


class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
	def post(self):
		upload_files = self.get_uploads('pic')  # 'file' is file upload field in the form
		blob_info = upload_files[0]
		#self.write(blob_info)
		self.redirect('/blob/serve/%s' % blob_info.key())

class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
	def get(self, resource):
		resource = str(urllib.unquote(resource))
		blob_info = blobstore.BlobInfo.get(resource)
		self.send_blob(blob_info)


