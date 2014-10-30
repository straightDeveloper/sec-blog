from google.appengine.ext import ndb

class Posts(ndb.Model):
	title = ndb.StringProperty(required=True);
	text = ndb.TextProperty(required=True);
	timeOfCreation = ndb.DateTimeProperty(auto_now_add=True);

