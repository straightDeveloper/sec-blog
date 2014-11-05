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

	def writePage(self,signin_error=False,signin_mistake=False,no_post=False):
		
		if self.isLinkPage:
		
			content = self.getLinkContent();
		
		else:
			content = self.getPostContent();

		
		self.render(self.template,content=content,myId=self.ID,is_user=self.is_user,signin_error=signin_error,signin_mistake=signin_mistake,post_error=no_post);
	
	

	

	def get(self,ids):
		self.set_ID_and_Type(ids);
		self.writePage();
		#self.delete_cookie("user");

	def check_sign_post(self,target):
		if target == "signin":
			name = self.get_form("sign_name");
			mypassword = self.get_form("password");
			
			if not self.empty_inputs(name,mypassword):#name != None and mypassword != None:
				
				if not self.empty_input_str(name,mypassword):#blank input in the form
					if name == username and hashlib.md5(mypassword).hexdigest() == password:#checking for correct password
						self.add_secure_cookie("user","t"); # making it a user 
					else:
						self.writePage(signin_mistake=True);
						return "incorrect_submission";
	
				else:
					self.writePage(signin_error=True);
					return "incorrect_submission";


		elif target == "signout":
			self.delete_cookie("user");

		else:
			return False;
			
		return True;# i t
		

	def check_delete_target(self,target):#check for delete forms during post page 
		if target:
			if target == "deleteLink":
				self.deleteLink( self.get_form("targetValue") ) ;
			elif target == "clearLink":
				self.clearLink( self.ID );
			elif target == "deletePost":
				self.deletePost( self.get_form("targetValue") );

			else:
				return False;#self.redirectPage(mainPageName);
			
			return True;

		return False;	

	def check_post_content(self):
		if self.isLinkPage:
			post = self.get_posted_link_data();#make a post model to be added.
		else:
			post = self.get_posted_post_data();#make a page model to be added.
		if post and post != "incorrect_submission" :
			post.put();
			return True;

		return post;#return post error false or error

	def post(self,ids):
		self.set_ID_and_Type(ids);
		target = self.get_form("target");
		
		signing_situation =  self.check_sign_post(target);#going to see if signin or signout happened and fetch it and proccess it.

		if signing_situation == "incorrect_submission": #if wrong submision dont redirect any where you are done.
			return;
		elif signing_situation:#if signed in then redirect as usual
			pass
		elif self.check_delete_target(target):#check for delete posts
			pass
		else:
			adding_a_post_situation = self.check_post_content();# trying to find correct post
			if adding_a_post_situation == "incorrect_submission":# if the post is incorrect
				self.writePage(no_post = True);
				return;
			elif adding_a_post_situation == False:
				self.redirectPage(mainPageName);# if no real post redirect to the mainpage
				
		self.redirect(self.request.url);# after posting get the page again to see the result
	

	
	def get_the_post_bad_situation(self,*p):

		if self.empty_inputs(*p):
			return False;
		if self.empty_input_str(*p):
			return "incorrect_submission";
		return True;



	def get_posted_post_data(self):
		subject = self.get_filtered_form("subject");
		content = self.get_filtered_form("content");
		post_situation = self.get_the_post_bad_situation(subject,content);
		if post_situation != True:
			return post_situation;
		return Post(title=subject,text=content,parent=self.getParentKey());	


	def get_posted_link_data(self):
		name = self.get_filtered_form("name");
		isPostPage = not self.get_form("isLinkPage");
		post_situation = self.get_the_post_bad_situation(name,isPostPage);
		if post_situation != True:
			return post_situation;
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



