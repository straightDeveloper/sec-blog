import webapp2
from week1 import week1_task_1
from blog import blog

application = webapp2.WSGIApplication([
	('/week1/task1/', week1_task_1),('/blog/',blog),
], debug=True)