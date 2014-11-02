import webapp2
from week1 import week1_task_1
#from week3.week3 import Week3_Blog , week3_blog_url ,week3_Blog_permalink, week3_permalink_url,week3_Blog_NewPosts,week3_Blog_NewPosts_url
#from week2 import week2_mini_task_1_1,week2_mini_task_1_2,week2_HW1,week2_HW2_1,week2_HW2_2
#from week2_a import template_tst_1,template_tst_2,template_tst_3,FizzBuzz
from BLog.blog import blog,blog_url
from week4.week4 import week4_basic_test,week4_basic_test_url


def urlify(url):
	return url+"/?$"


#week2_mini_task_1_1_url = '/week2/google/';
#week2_mini_task_1_2_url = week2_mini_task_1_1_url+'testform/';



#week2_app = [('/week2/hw1/',week2_HW1),('/week2/google/',week2_mini_task_1_1 ),('/week2/google/testform/', week2_mini_task_1_2),('/week2/signup/',week2_HW2_1),('/week2/welcome',week2_HW2_2),];
#week2_a_app = [('/week2-a/1',template_tst_1),('/week2-a/2',template_tst_2),('/week2-a/3',template_tst_3),('/week2-a/fizzbuz/',FizzBuzz)];

#week3_app = [( urlify(week3_blog_url) ,Week3_Blog ),( urlify(week3_permalink_url) ,week3_Blog_permalink ),(urlify(week3_Blog_NewPosts_url),week3_Blog_NewPosts),]

week4_app = [(urlify(week4_basic_test_url),week4_basic_test),]

blog_app = [(urlify(blog_url),blog),]


application = webapp2.WSGIApplication([
	('/week1/task1/', week1_task_1),]+blog_app, debug=True)