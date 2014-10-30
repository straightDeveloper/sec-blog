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

	
	def set_page_property(self):
		template_index = 0;
		
		if self.isLinkPage:
			template_index = 1;
		
		self.template = self.mainTemplates[template_index];

	
	def redirectPage(self,ids):
		self.redirect( blog_url.replace( "(\d+|%s)" % mainPageName , str(ids) ) );
 






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
				self.set_page_property();
		 
				return
		except:
			if ids == mainPageName:
				self.ID = None;
				return;


		
		self.redirectPage(mainPageName);

	def writePage(self):
		
		if self.isLinkPage:
		
			content = self.getLinkContent();
		
		else:
		
			content = self.getPostContent();

		
		self.render(self.template,content=content)
	
	

	

	def get(self,ids):
		self.set_ID_and_Type(ids);
		self.writePage();

	def post(self,ids):
		self.set_ID_and_Type(ids);
		target = self.get_form("target");

		if target:
			if target == "deleteLink":
				self.deleteLink( self.get_form("targetValue") ) ;
		else:
			if self.isLinkPage:
				post = self.get_posted_link_data();
			else:
				post = self.get_posted_post_data();

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


	def deleteLink(self,ids):
		self.mainDelete(ids,linkDelete)

	def mainDelete(self,ids,deleteMethod):
		try:
			ID = int(ids);
		except:
			return;


		deleteMethod(ID=ID);

		#link = Page.get_by_id(ID);
		#if link:
		#	myKey = link.key;
		#	sonKeys = [m.key for m in Page.query(Page.parent=myKey)]
		#	ndb.delete_multi(sonkeys);
		#	sonkeys = [m.key for m in page.query(Post.parent=myKey)];
		#	ndb.delete_multi(sonkeys);
		self.redirectPage(self.ID);



def linkNodeDelete():

	link = Page.get_by_id(ID);
	if link:
		myKey = link.key;
		for m in Page.query(Page.parent == myKey):
			linkDelete(m.key.id());
		
		for m in Post.query(Post.parent == myKey):
			m.key.delete();

	return link;

def linkDelete(ID):
		link = Page.get_by_id(ID);
		if link:
			myKey = link.key;
			for m in Page.query(Page.parent == myKey):
				linkDelete(m.key.id());
			
			for m in Post.query(Post.parent == myKey):
				m.key.delete();
			
			myKey.delete();
			
			#sonkeys = [m.key for m in page.query(Post.parent=myKey)];
			#ndb.delete_multi(sonkeys);

