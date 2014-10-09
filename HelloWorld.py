import os
import webapp2
import jinja2

jinja_environment = jinja2.Environment(autoescape=True,loader=jinja2.FileSystemLoader( os.path.join(os.path.dirname(__file__), 'templates') ) )


class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'

		template = jinja_environment.get_template("BlogMain.html");

		self.response.write(template.render({}))

