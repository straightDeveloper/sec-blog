from google.appengine.ext import ndb

class Page(ndb.Model):
	name = ndb.StringProperty(required=True)
	isPostPage = ndb.BooleanProperty(required=True)
	parent = ndb.KeyProperty(kind='Page'); 
	timeOfCreation = ndb.DateTimeProperty(auto_now_add=True);

	def render(self,class_name=''):
		return '<a href="/blog/%(url)s" class="%(class)s" >%(name)s</a>'%{'url':self.key.id(),'name':self.name, 'class': class_name}


class Post(ndb.Model):
	title = ndb.StringProperty(required=True);
	text = ndb.TextProperty(required=True);
	parent = ndb.KeyProperty(kind='Page');
	time = ndb.DateTimeProperty(auto_now_add=True);