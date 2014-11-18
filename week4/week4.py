import time
import os
import webapp2
import jinja2
import cgi
import re
from handler import Handler
from week2 import week2_HW2_1 
from models import User

week4_basic_test_url = "/week4/visits"
week4_HW1_1_url = "/week4/signup";

week4_HW2_url = "/week4/login"

week4_HW3_url = "/week4/logout"

week4_HW1_2_url = "/week4/welcome"
user_name_header = "name";


class week4_HW1_2(Handler):#signup
	def get(self):
		name = self.get_secure_cookie(user_name_header);
		if name == None or name == "":
			self.redirect(week4_HW1_1_url);

		self.write("<h2>Welcome, %s!</h2>"%name)


class week4_HW1_1(week2_HW2_1):#success form

	def signin(self,name):
		self.add_secure_cookie(user_name_header,str(name));
		self.redirect(week4_HW1_2_url);
		
	def signout(self):
		self.delete_cookie(user_name_header);

	def atSuccess(self,username,password,email):
		user = User();
		user.add_properties(name=username,password=password,email=email);
		user.put();
		self.signin(username);



class week4_HW3(week4_HW1_1):#signout

	def post(self):
		self.error(405);
	def get(self):
		self.signout();
		self.redirect(week4_HW1_1_url);


class week4_HW2(week4_HW1_1):

	def writePage(self,error = False):
		self.render("week4/signin.html",error=error)
	def get(self):
		self.writePage();
		
	def post(self):
		self.signout();
		name = str( self.get_form("username") );
		password = str( self.get_form("password") );

		my_user=User.query(User.name == name).get();
	
		if my_user and my_user.check_password(password):
			self.signin(name);
			#self.write(my_user.password);
		else:
			self.writePage(error=True);




class week4_basic_test(Handler):

	def get(self):
		self.response.headers['Content-Type'] = 'text/plain';
		visits = self.get_visits();
		self.add_cookie("visits",visits);
		if visits < 255:
			self.write("you have been there %s times" % visits)
		else:
			self.write("you are an astute guy");

	def get_visits(self):
		visits = self.request.cookies.get('visits',"0");
		if visits.isdigit():
			visits = int(visits) + 1;

		else:
			visits = 0;

		return visits;

