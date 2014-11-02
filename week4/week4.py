import time
import os
import webapp2
import jinja2
import cgi
import re
from handler import Handler


week4_basic_test_url = "/week4/visits"

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
		