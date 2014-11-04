import os
import webapp2
import jinja2
from model import Page,Post
from handler import Handler
import hashlib
mainPageName = "MainPage"
blog_url = r"/blog/(\d+|%s)"%mainPageName;

username = "mostafa";
password = '53d124408addf1eb1de84f3ff866ead8';


class blog(Handler):

	
	mainTemplates = ["Blog/BlogPosts.html","Blog/BlogLinks.html"];
	template = mainTemplates[1];
	ID = None;
	isLinkPage = True;
	is_user = True;

	
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
	
	def check_user(self):
		isUser = self.get_secure_cookie("user");
		if isUser == "t":
			self.is_user = True;
			
		else:
			self.is_user = False;

		#self.is_user = True;		
		return self.is_user;

	def set_ID_and_Type(self,ids):
		if not self.check_user():
			pass
			#self.add_secure_cookie("user","t");
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

		
		self.render(self.template,content=content,myId=self.ID,is_user=self.is_user);
	
	

	

	def get(self,ids):
		self.set_ID_and_Type(ids);
		self.writePage();


	def check_delete_target(self,target):
		if target == "deleteLink":
				self.deleteLink( self.get_form("targetValue") ) ;
		elif target == "clearLink":
			self.clearLink( self.ID );
		elif target == "deletePost":
			self.deletePost( self.get_form("targetValue") );

		else:
			self.redirectPage(mainPageName);
			return False;

		return True;	


	def post(self,ids):
		self.set_ID_and_Type(ids);
		target = self.get_form("target");
		
		if target == "signin":
			name = self.get_form("sign_name");
			mypassword = self.get_form("password");
			if name != None and mypassword != None:
				if name == username and hashlib.md5(mypassword).hexdigest() == password:
					self.add_secure_cookie("user","t");
				else:
					self.write("%s %s"%(name,mypassword));
					return

		elif target:
			if target == "deleteLink":
				self.deleteLink( self.get_form("targetValue") ) ;
			elif target == "clearLink":
				self.clearLink( self.ID );
			elif target == "deletePost":
				self.deletePost( self.get_form("targetValue") );

			else:
				self.redirectPage(mainPageName);
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
	
	def deletePost(self,ids):
		self.mainDelete(ids,postDelete)

	def clearLink(self,ids):
		self.mainDelete(ids,linkNodeDelete)
	

	def mainDelete(self,ids,deleteMethod):
		try:
			ID = int(ids);
		except:
			ID = None; 
			

		deleteMethod(ID=ID);

		self.redirectPage(self.ID);



def linkNodeDelete(ID):

	link = None;
	if ID:
		link = Page.get_by_id(ID);
	myKey = None;
	if link:
		myKey = link.key;
	
	 
	for m in Page.query(Page.parent == myKey):
		linkDelete(m.key.id());
		
	for m in Post.query(Post.parent == myKey):
		m.key.delete();


	return link;

def linkDelete(ID):
	link = linkNodeDelete(ID);
	if link:
		link.key.delete();	
		#	myKey.delete();
			
			#sonkeys = [m.key for m in page.query(Post.parent=myKey)];
			#ndb.delete_multi(sonkeys);

def postDelete(ID):
	if ID:
		myPost = Post.get_by_id(ID);
		if myPost:
			myPost.key.delete();



