import webapp2
import jinja2
import os
import re

jinja_environment = jinja2.Environment(autoescape=True,loader=jinja2.FileSystemLoader( os.path.join(os.path.dirname(__file__), 'templates') ) )



class Handler(webapp2.RequestHandler):

	def get_form(self,name):
		return self.request.get(name);
	def get_filtered_form(self,name):
		name = self.request.get(name);
		name = self.removeSpaces(name);
		return name;
	def removeSpaces(self,string):
		string = re.sub(r'^[ \n]*',"",string);
		string = re.sub(r'[ \n]*$',"",string);
		return string;


	def write(self,*a,**kw):
		self.response.write(*a,**kw);

	def render_str(self,template,**params):
		t = jinja_environment.get_template(template);
		return t.render(params);

	def render(self,template,**kw):
		self.write( self.render_str(template,**kw) );
