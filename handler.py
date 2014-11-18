import webapp2
import jinja2
import os
import re
import hmac

jinja_environment = jinja2.Environment(autoescape=True,loader=jinja2.FileSystemLoader( os.path.join(os.path.dirname(__file__), 'templates') ) )

debug_password= "1gag&242k*hc@@@141&gl&88r235^^_@@#22#&^"

class BasicHandler(webapp2.RequestHandler):
	SECRET = debug_password;	

	def add_secure_cookie(self,header,value):
		self.add_cookie( header , self.secure_cookie(value) );
	
	def hash_str(self,s):
		return hmac.new(self.SECRET,s).hexdigest();

	def secure_cookie(self,s):
		return "%s|%s" % (s, self.hash_str(s));


	def get_secure_cookie(self,header):
		naive_cookie = self.get_cookie(header);
		if naive_cookie:
			cookie_split = naive_cookie.split("|");
		else:
			return None;

		if len(cookie_split) != 2:
			return None;

		value = cookie_split[0];

		if naive_cookie == self.secure_cookie(value):
			return value;

		return None;

	def get_cookie(self,header):
		return str( self.request.cookies.get(header) );
		
	def delete_cookie(self,header):
		self.add_cookie(header,'');


	def add_cookie(self,header,value):
		cookie = "%s=%s"%(str(header),str(value));
		cookie = str(cookie);
		self.set_cookie(cookie);

	def set_cookie(self,cookie):
		self.response.headers.add_header("Set-Cookie",cookie);
		



class Handler(BasicHandler):
	#password = debug_password;
	def empty_inputs(self,*p):
		for inputs in p:
			if inputs == None:
				return True;
		return False;
	
	def empty_input_str(self,*p):
		for inputs in p:
			if inputs == "":
				return True;
		return False;

	def total_empty_input(self,*p):
		return self.empty_input_str(*p) or self.empty_inputs(*p);  

	def get_form(self,name):
		return self.request.get(name);
	

	def get_filtered_form(self,name):
		name = self.request.get(name);
		name = self.removeSpaces(name);
		return name;
	
	def removeSpaces(self,string):
		string = re.sub(r'^ *',"",string);
		return string;


	def write(self,*a,**kw):
		self.response.write(*a,**kw);

	def render_str(self,template,**params):
		t = jinja_environment.get_template(template);
		return t.render(params);

	def render(self,template,**kw):
		self.write( self.render_str(template,**kw) );



