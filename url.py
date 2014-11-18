import webapp2
from week1 import week1_task_1
#from week3.week3 import Week3_Blog , week3_blog_url ,week3_Blog_permalink, week3_permalink_url,week3_Blog_NewPosts,week3_Blog_NewPosts_url
#from week2 import week2_mini_task_1_1,week2_mini_task_1_2,week2_HW1,week2_HW2_1,week2_HW2_2
#from week2_a import template_tst_1,template_tst_2,template_tst_3,FizzBuzz
from BLog.blog import blog,blog_url
from week4.week4 import week4_basic_test,week4_basic_test_url,week4_HW1_1,week4_HW1_1_url,week4_HW1_2,week4_HW1_2_url,week4_HW2_url,week4_HW2,week4_HW3,week4_HW3_url
#from test import img_saver,img_saver_url,img_adder,img_adder_url,img_handler,img_handler_url,img_direct_adder
#from test import ServeHandler,blobHandler,UploadHandler
from blobstore.blobstore import blobHandler_url,blobUpload_url,blobServer_url,blobHandler,blobUpload,blobServer
def urlify(url):
	return url+"/?$"


#week2_mini_task_1_1_url = '/week2/google/';
#week2_mini_task_1_2_url = week2_mini_task_1_1_url+'testform/';



#week2_app = [('/week2/hw1/',week2_HW1),('/week2/google/',week2_mini_task_1_1 ),('/week2/google/testform/', week2_mini_task_1_2),('/week2/signup/',week2_HW2_1),('/week2/welcome',week2_HW2_2),];
#week2_a_app = [('/week2-a/1',template_tst_1),('/week2-a/2',template_tst_2),('/week2-a/3',template_tst_3),('/week2-a/fizzbuz/',FizzBuzz)];

#week3_app = [( urlify(week3_blog_url) ,Week3_Blog ),( urlify(week3_permalink_url) ,week3_Blog_permalink ),(urlify(week3_Blog_NewPosts_url),week3_Blog_NewPosts),]

week4_app = [(urlify(week4_basic_test_url),week4_basic_test),( urlify(week4_HW1_1_url), week4_HW1_1 ),( urlify(week4_HW1_2_url), week4_HW1_2 ),( urlify(week4_HW3_url) ,week4_HW3),( urlify(week4_HW2_url),week4_HW2 ), ]

blog_app = [(urlify(blog_url),blog),]

#blob_app = [('/blob', blobHandler),(urlify('/blob/upload'), UploadHandler),(urlify('/blob/serve/([^/]+)?'), ServeHandler),]
blob_app = [(blobHandler_url,blobHandler),(blobUpload_url,blobUpload),(blobServer_url,blobServer),]

application = webapp2.WSGIApplication([
	('/week1/task1/', week1_task_1),]+week4_app, debug=True)