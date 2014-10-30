import os
import webapp2
import jinja2
from model import Page,Post
from handler import Handler

blog_url = r"/blog/(\d+)";



class blog(Handler):

	
	mainTemplates = ["Blog/BlogPosts.html","Blog/BlogLinks.html"];
	template = "Blog/BlogPosts.html";
	
	def getLinkContent(self,ID):
		pass

	def getContent(self,ID):
		return Post.query().order(-Post.time);
	
	def writePage(self,ids):
		ID = int(ids);
		content = self.getContent(ID);
		self.render(self.template,content=content)
	
	

	

	def get(self,ids):
		self.writePage(ids);

	def post(self):
		post = self.get_posted_data();
		post.put();
		self.redirect(self.request.url);
	

	



	def get_posted_data(self):
		subject = self.get_filtered_form("subject");
		content = self.get_filtered_form("content");
		return Post(title=subject,text=content,parent=None);	

