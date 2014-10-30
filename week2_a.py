import os
import webapp2
import jinja2

jinja_environment = jinja2.Environment(autoescape=True,loader=jinja2.FileSystemLoader( os.path.join(os.path.dirname(__file__), 'templates') ) )


class Handler(webapp2.RequestHandler):

	def write(self,*a,**kw):
		self.response.write(*a,**kw);

	def render_str(self,template,**params):
		t = jinja_environment.get_template(template);
		return t.render(params);

	def render(self,template,**kw):
		self.write( self.render_str(template,**kw) );

formHtml = """<form>
		<h2>Add a food</h2>
	<input type="text" name="food">
%s
	<button>Add</button>
	</form> """
hiddenHtml = """ <input type="hidden" name='food' value="%s"> """

itemHtml = "<li>%s</li>"

shoppingList = """<br>
<br>
<h2>shoppingList</h2>
<ul>
%s
</ul>

 """

class template_tst_1(Handler):#very simple thing
	def get(self):
		self.write("Hello world!");


class template_tst_2(Handler):#string substitution without testing
	def get(self):
		output= formHtml;
		outputHidden = ""
		outputItems = ""
		items=self.request.get_all("food");
		if items:
			for item in items:
				outputHidden += hiddenHtml%item;

			for item in items:
				outputItems += itemHtml%item;

		output_shopping = shoppingList%outputItems;
		output += output_shopping;
		output = output%outputHidden;
		
		self.write(output);



class template_tst_3(Handler):#with testing
	def get(self):
		self.render("week2-a/3.html",name="steve")


class FizzBuzz(Handler):
	def get(self):
		n = self.request.get("n",0);
		n = n and int(n);
		self.render("week2-a/FizzBuzz.html",n = n);





