import os
import webapp2
import jinja2
from model import Page,Post
from handler import Handler

mainPageName = "MainPage"
blog_url = r"/blog/(\d+|%s)"%mainPageName;


class blog(Handler):

	
	mainTemplates = ["Blog/BlogPosts.html","Blog/BlogLinks.html"];
	template = mainTemplates[1];
	ID = None;
	isLinkPage = True;

	def getParent(self):
		parent = None;
		if self.ID:
			parent = Page.get_by_id(self.ID);

		return parent;
	



	def getParentKey(self):
		parent = self.getParent();
		if parent:
			return parent.key;



	def getLinkContent(self):
		return Page.query( Page.parent == self.getParentKey() ).order(-Page.timeOfCreation)

	def getPostContent(self):
		return Post.query( Post.parent == self.getParentKey() ).order(-Post.time);
	

	def set_ID_and_Type(self,ids):
		try:
			self.ID = int(ids);
			parent = self.getParent();
			if parent:#checking if this id exist
				self.isLinkPage = not parent.isPostPage; 
				return
		except:
			if ids == mainPageName:
				self.ID = None;
				return;
		
		self.redirect( blog_url.replace( "(\d+|%s)" % mainPageName , mainPageName ) );


	def writePage(self):
		content = self.getLinkContent();
		self.render(self.template,content=content)
	
	

	

	def get(self,ids):
		self.set_ID_and_Type(ids);

		self.writePage();

	def post(self,ids):
		self.set_ID_and_Type(ids);
		post = self.get_posted_link_data();
		post.put();
		self.redirect(self.request.url);
	

	



	def get_posted_post_data(self):
		subject = self.get_filtered_form("subject");
		content = self.get_filtered_form("content");
		return Post(title=subject,text=content,parent=self.getParentKey());	


	def get_posted_link_data(self):
		name = self.get_form("name");
		isPostPage = not self.get_form("isLinkPage");
		return Page(name=name,parent=self.getParentKey(),isPostPage=isPostPage);


