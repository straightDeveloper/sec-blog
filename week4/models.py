from google.appengine.ext import ndb
from bcrypt.bcrypt import hashpw,gensalt
import re

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$");
Email_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$");
Pass_RE = re.compile(r"^.{3,20}$");


class User(ndb.Model):
	name = ndb.StringProperty(required=True);
	email = ndb.StringProperty(required=False); 
	password = ndb.StringProperty(required=True);
	def add_properties(self,name=name,password=password,email=email):
		self.name = name;
		if email != "" or email != None:
			self.email = email;
		self.password = self.encrpytPassword(password);
	def encrpytPassword(self,password):
		return hashpw(password, gensalt());

	def check_password(self,cpass):
		return hashpw(cpass, self.password) == self.password;
		#return (self.mpass == cpass);
