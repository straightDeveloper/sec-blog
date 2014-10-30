import os
import webapp2
import jinja2
import cgi
import re



jinja_environment = jinja2.Environment(autoescape=True,loader=jinja2.FileSystemLoader( os.path.join(os.path.dirname(__file__), 'templates') ) )


class week2_mini_task_1_1(webapp2.RequestHandler):
	
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'

		template = jinja_environment.get_template("week2/1.html");

		self.response.write(template.render({}))


class week2_mini_task_1_2(webapp2.RequestHandler):

	def get(self):
		self.response.headers['Content-Type'] = "text/plain"
		q = self.request.get("q");
		self.response.write(q);



class week2_HW1(webapp2.RequestHandler):
	template = jinja_environment.get_template("week2/HW1.html");
		
	def verifyLetter(self,var):
		if ( var >= "a" and var <="z" ):
			return "a";
		if ( var >= "A" and var <= "Z" ):
			return "A";		
	
	def convertLetter(self,ch):
		offset = self.verifyLetter(ch);
		if offset:
			offset = ord(offset);
			ch = ( ord(ch) - offset + 13 ) % 26 ;
			ch = chr(ch + offset);
		return ch;

	def rot13(self,stringer):
		newString = "";
		for ch in stringer:
			newString = newString+self.convertLetter(ch); 
		return newString;
	def get(self):
		self.response.write(self.template.render({}));
	
	def post(self):
		text = self.request.get("text");
		text = self.rot13(text);
		#text = cgi.escape(text);
		self.response.write(self.template.render({"texts":text}));



class week2_HW2_2(webapp2.RequestHandler):
	"""docstring for week2_HW2_2"""
	def get(self):
		resp = "<h2>Welcome, %s!</h2>"%self.request.get("name");
		self.response.write(resp);


class week2_HW2_1(webapp2.RequestHandler):
	template = jinja_environment.get_template("week2/signup.html");
	USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$");
	Email_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$");
	Pass_RE = re.compile(r"^.{3,20}$");

	def notMatchRegularExp(RE,stringer):
		not RE.match(stringer);

	def finderrors(self,username,pass1,pass2,email):
		errors = {"badPassword": not self.Pass_RE.match(pass1),"badUser": not self.USER_RE.match(username),"badEmail": not self.Email_RE.match(email),"passwordMismatch": pass1 != pass2 };
		errors["passwordMismatch"] = errors["passwordMismatch"] and not errors["badPassword"];
		#errors find all the errors and values to be added
		if email == "":
			errors["badEmail"] = False;
		isThereError = False;
		
		for k , error in errors.iteritems():		
			isThereError = isThereError or error;

		self.addUnErroredParam(errors,username,"badUser","username");				

		self.addUnErroredParam(errors,email,"badEmail","email");#add email value if its correct				


		
		return {"total":isThereError,"errors":errors}

	def addUnErroredParam(self,errors,value,cond,param):
		if not errors[cond]:
			errors[param] = value;

	def get(self):
		self.response.write(self.template.render({}));

	def post(self):
		username = self.request.get("username");	
		pass1 = self.request.get("password");	
		pass2 = self.request.get("verify");	
		email = self.request.get("email");
		result = self.finderrors(username,pass1,pass2,email);
		if result["total"]:
			self.response.write(self.template.render(result["errors"]));
		else:
			self.redirect("/week2/welcome?name=%s"%username);
