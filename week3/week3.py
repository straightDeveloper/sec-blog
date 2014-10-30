import time
import os
import webapp2
import jinja2
import cgi
import re
from handler import Handler
#from datetime import strftime
from models import Posts


week3_blog_url = "/week3/blog";
week3_permalink_url = '/week3/blog/(\d+)'
week3_Blog_NewPosts_url = '/week3/blog/newpost'

class Week3_Blog(Handler):
	template = "week3/mainPage.html";
	
	def getTheRequiredPosts(self):
		return Posts.query().order(-Posts.timeOfCreation);
		
	def writeForm(self,error=False,text="",title=""):
		posts = self.getTheRequiredPosts();
		yourUrl = self.request.url; 
		self.render(self.template,error=error,text=text,title=title,main_url = week3_blog_url,posts=posts);

	
	def get(self):
		self.writeForm();

	










class week3_Blog_NewPosts(Handler):
	template = "week3/blog_post.html";

	def get(self):
		self.writeForm();

	def writeForm(self,error=False,text="",title=""):
		self.render(self.template,error=error,text=text,title=title);
	

	def validatePost(self,title,text):
		return title != "" and text != "";


	def post(self):
		title = self.request.get("subject");
		text = self.request.get("content");
		title = self.removeSpaces(title);
		text = self.removeSpaces(text);
		if not self.validatePost(title,text):
			self.writeForm(error=True,title=title,text=text);
		else:
			post = Posts(title=title,text=text);
			post.put();
			released_url = week3_permalink_url.replace('(\d+)',str( post.key.id() ) )
			time.sleep(1);
			self.redirect(released_url);










class week3_Blog_permalink(Week3_Blog):
	post = None;
	template = "week3/permalink.html";
	def getTheRequiredPosts(self):
		return self.post;
	def get(self,ids):
		ID = int(ids);
		self.post = Posts.get_by_id(ID);
		if self.post:
			self.writeForm();
		else:
			self.redirect(week3_blog_url);

	def post(self):
		pass

