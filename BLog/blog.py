import os
import webapp2
import jinja2
from model import Page,Post
from handler import Handler





class blog(Handler):

	template = "Blog/BlogPosts.html";
	def writePage(self):
		content = Post.query().order(-Posts.time);
		self.render("Blog/BlogPosts.html",content=content)
	
	def get(self):
		
	def post(self):
		subject = self.get_filtered_form("subject");
		content = self.get_filtered_form("content");
		post = Post(title=subject,text=content,parent=None);
		post.put();
		self.redirect(self.request.url);
	
