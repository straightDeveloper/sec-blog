from google.appengine.ext import ndb

class Page(ndb.Model):
	name = ndb.StringProperty(required=True)
	isPostPage = ndb.BooleanProperty(required=True)
	parent = ndb.KeyProperty(kind='Page'); 
	timeOfCreation = ndb.DateTimeProperty(auto_now_add=True);



class Post(ndb.Model):
	title = ndb.StringProperty(required=True);
	text = ndb.TextProperty(required=True);
	parent = ndb.KeyProperty(kind='Page');
	time = ndb.DateTimeProperty(auto_now_add=True);