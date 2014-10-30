import os
import webapp2
import jinja2
from model import Page,Post
from handler import Handler

blog_url = r"/blog/(\d+)";
mainPageName = "MainPage"


class blog(Handler):

	
	mainTemplates = ["Blog/BlogPosts.html","Blog/BlogLinks.html"];
	template = mainTemplates[1];
	ID = None;

	def getParent(self):
		parent = None;
		if self.ID:
			parent = Page.get_by_id(self.ID);
			
		return parent;

	def getLinkContent(self):
		return Page.query(Page.parent == self.getParent()).order(-Page.timeOfCreation)

	def getPostContent(self):
		return Post.query().order(-Post.time);
	

	def getID(self,ids):
		try:
			self.ID = int(ids);
		except:
			if ids == mainPageName:
				self.ID = None;


	def writePage(self):
		content = self.getLinkContent();
		self.render(self.template,content=content)
	
	

	

	def get(self,ids):
		self.getID(ids);
		self.writePage();

	def post(self,ids):
		self.getID(ids);
		post = self.get_posted_link_data();
		post.put();
		self.redirect(self.request.url);
	

	



	def get_posted_post_data(self):
		subject = self.get_filtered_form("subject");
		content = self.get_filtered_form("content");
		return Post(title=subject,text=content,parent=None);	


	def get_posted_link_data(self):
		name = self.get_form("name");
		return Page(name=name,parent=self.getParent(),isPostPage=False);


