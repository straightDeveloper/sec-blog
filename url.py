import webapp2
from HelloWorld import MainPage

application = webapp2.WSGIApplication([
	('/', MainPage),
], debug=True)