from google.appengine.ext import webapp
from google.appengine.api import xmpp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import xmpp_handlers
from google.appengine.ext.webapp.template import render
from google.appengine.api import urlfetch
from BeautifulSoup import BeautifulSoup

from django.utils import simplejson as json

import urllib
import re
from os import path

HELP_MSG = """Welcome to automatd LEO bot for RP
====================
Following features are supported -
1. /grades (daily grades + UT grades)
2. /rj (includes submission status)
3. /class ( Class Timetable )
4. /ut ( UT Timetable )
5. /ce
6. /gpa
7. /me
8. /gradesall (beta)

*Please notice that I do not store your credentials*. Please check out the source code at https://github.com/emoosx/rpleobot.

Spread the love if you enjoy using it.
====================
Developed by _*Kaung Htet Zaw*_ . 
====================
Mail to emoosx@gmail.com for Bug reports & feature suggestions.

USAGE EXAMPLE
-------------
/grades 91234:password
/class 91234:password
/ut 91234:password
"""

class MainHandler(webapp.RequestHandler):
    def get(self):
		tmpl = path.join(path.dirname(__file__), "index.html")
		content = {}
		self.response.out.write(render(tmpl, content))


class XmppHandler(xmpp_handlers.CommandHandler):

	def text_message(self, message=None):
		message.reply(HELP_MSG)

	def unhandled_command(self, message=None):
		message.reply('Unknown Feature! Type "/help" for usage manual')

	def grades_command(self, message=None):
		colon_index = message.arg.index(":")
		sid = str(message.arg[0:colon_index])
		password = str(message.arg[colon_index+1:])
		message.reply(getGrades(sid, password))

	def class_command(self, message=None):
		colon_index = message.arg.index(":")
		sid = str(message.arg[0:colon_index])
		password = str(message.arg[colon_index+1:])
		message.reply(getClassSchedule(sid, password))
		
	def ut_command(self, message=None):
		colon_index = message.arg.index(":")
		sid = str(message.arg[0:colon_index])
		password = str(message.arg[colon_index+1:])
		message.reply(getUTSchedule(sid,password))

	def rj_command(self, message=None):
		colon_index = message.arg.index(":")
		sid = str(message.arg[0:colon_index])
		password = str(message.arg[colon_index+1:])
		message.reply(getRJ(sid, password))
		
	def ce_command(self, message=None):
		colon_index = message.arg.index(":")
		sid = str(message.arg[0:colon_index])
		password = str(message.arg[colon_index+1:])
		message.reply(getCE(sid, password))
	
	def gpa_command(self, message=None):
		colon_index = message.arg.index(":")
		sid = str(message.arg[0:colon_index])
		password = str(message.arg[colon_index+1:])
		message.reply(getGPA(sid, password))

	def help_command(self, message=None):
		message.reply(HELP_MSG)
		
	def me_command(self, message=None):
		colon_index = message.arg.index(":")
		sid = str(message.arg[0:colon_index])
		password = str(message.arg[colon_index+1:])
		message.reply(getDetails(sid, password))
	
	def gradesall_command(self, message=None):
		colon_index = message.arg.index(":")
		sid = str(message.arg[0:colon_index])
		password = str(message.arg[colon_index+1:])
		message.reply(getAllGrades(sid, password))
	
#helper methods to do respective actions
def getClassSchedule(sid, password):
	TIMETABLE_API_URL = 'http://emoosx.me/regulus/api/classroom/classSchedule'
	data = urllib.urlencode({"sid" : sid, "password" : password})
	
	try:
		timetable_result = urlfetch.fetch(TIMETABLE_API_URL, payload=data, method=urlfetch.POST, deadline=60, headers={'Content-Type' : 'application/x-www-form-urlencoded'})
		timetable_json = json.loads(timetable_result.content)
	except urlfetch.DownloadError:
		timetable_json = {"error" : "Server is taking too much time. Please try again!"}
	
	msg = ""
	if not "error" in timetable_json:
		msg += "\nClass Timetable"
		msg += "\n===================="
		for timetable in timetable_json:
			msg += "\nModule : %s %s" % (timetable["module_code"],timetable["module_name"])
			msg += "\nProblem No : %s" % timetable["problem_no"]
			msg += "\nVenue : %s" % timetable["venue"]
			msg += "\nDate : %s" % timetable["date"]
			msg += "\nDay : %s" % timetable["day"]
			msg += "\nTime : %s" % timetable["time"]
			msg += "\n\n"
	return msg

def getUTSchedule(sid, password):
	UT_API_URL = 'http://emoosx.me/regulus/api/classroom/utSchedule'
	data = urllib.urlencode({'sid' : sid, "password" : password})
	
	try:
		ut_result = urlfetch.fetch(UT_API_URL, payload=data, method=urlfetch.POST, deadline=60, headers={'Content-Type' : 'application/x-www-form-urlencoded'})
		ut_json = json.loads(ut_result.content)
	except urlfetch.DownloadError:
		ut_json = {"error" : "Server is taking too much time. Please try again!"}
	
	msg = ""
	if not "error" in ut_json:
		msg += "\nUT Timetable"
		msg += "\n===================="
		for ut in ut_json:
			msg += "\nUT Name : %s" % ut["ut_name"]
			msg += "\nModule Name : %s" % ut['module_name']
			msg += "\nVenue : %s" % ut['venue']
			msg += "\nTime : %s" % ut['time']
			msg += "\nDate : %s" % ut['date']
			msg += "\n\n"
	return msg
	
def getRJ(sid, password):
	RJ_API_URL = 'http://emoosx.me/regulus/api/dailyProblem/rjquestion'
	data = {"sid" : sid, "password" : password}
	
	try:
		rj_result = urlfetch.fetch(RJ_API_URL,payload=urllib.urlencode(data),method=urlfetch.POST,deadline=60,headers={'Content-Type': 'application/x-www-form-urlencoded'})
		rj_json = json.loads(rj_result.content)
	except urlfetch.DownloadError:
		rj_json = {"error" : "Server is taking too much time. Please try again!"}
		
	msg = ""
	if not "error" in rj_json:
		msg += "\n" + rj_json["problem_name"]
		msg += "\n===================="
		msg += "\n *Question* : %s" %rj_json["rj_question"]
		msg += "\n===================="
		msg += "\n *Status* : %s" %rj_json["status"]
	else:
		msg = rj_json["error"]
	return msg	

	
def getGrades(sid, password):
	GRADES_API_URL = "http://emoosx.me/regulus/api/grades/recentGrades"
	UT_API_URL = "http://emoosx.me/regulus/api/grades/recentUTGrades"	
	data = urllib.urlencode({"sid" : sid, "password" : password})
	
	try:
		grades_result = urlfetch.fetch(GRADES_API_URL, method=urlfetch.POST, deadline=60, payload=data, headers={'Content-Type': 'application/x-www-form-urlencoded'})
		grades_json = json.loads(grades_result.content)
	except urlfetch.DownloadError:
		grades_json = {"error" : "Server is taking too much time. Please try again!"}
	
	try:
		ut_result = urlfetch.fetch(UT_API_URL, method=urlfetch.POST, deadline=60, payload=data, headers={'Content-Type': 'application/x-www-form-urlencoded'})
		ut_json = json.loads(ut_result.content)
	except urlfetch.DownloadError:
		ut_json = {"error" : "Server is taking too much time. Please try again!"}
	
	msg = ""
	if not "error" in grades_json:
		msg = "\n*Recent Daily Grades* \n===================="
		for p in grades_json:
			msg += "\n%s > P(%s) %s " % (p["module_name"], p["problem"], p["grade"])
	
		msg += "\n\n====================\n*UT Grades* \n===================="
		for ut in ut_json:
			msg += "\n%s > UT-(%s) %s" % (ut["module_name"], ut["ut_no"], ut["ut_grade"])
	else:
		msg = grades_json["error"]
	return msg
	
def getCE(sid, password):
	site = "http://emoosx.me/leoapp/academic.php?"
	site += urllib.urlencode({"sid": str(sid), "password":str(password)})
	html = str(urllib.urlopen(site).read())
	ce_diploma = re.findall('id="ctl00_ContentPlaceHolderMain_lblCEDiploma" class="gen12"><b>(.*)</b>', html)[0]
	ce_nondiploma = re.findall('id="ctl00_ContentPlaceHolderMain_lblCENDiploma" class="gen12"><b>(.*)</b>', html)[0]
	msg = "CE Points\n====================\n"
	msg += "Diploma Points => %s\n" % str(ce_diploma)
	msg += "Non-Diploma Points => %s\n" % str(ce_nondiploma)
	msg += "---------------------\n"
	msg += "Total => %d" % (int(ce_diploma) + int(ce_nondiploma))
	return msg
	
def getGPA(sid, password):
	site = "http://emoosx.me/leoapp/academic.php?"
	site += urllib.urlencode({"sid": str(sid), "password":str(password)})
	html = str(urllib.urlopen(site).read())
	gpa = re.findall('id="ctl00_ContentPlaceHolderMain_lblGPA" class="gen12"><b>(.*)</b>', html)[0]
	msg = "GPA\n====================\n"
	return msg + "Cummulative GPA => " + str(gpa)

def getDetails(sid, password):
	site = "http://emoosx.me/leoapp/academic.php?"
	site += urllib.urlencode({"sid": str(sid), "password":str(password)})
	html = str(urllib.urlopen(site).read())
	msg = "Personal Particulars\n====================\n"
	name = "Name => %s\n" % str(re.findall('id="ctl00_ContentPlaceHolderMain_lblName" class="gen12">(.*)</span>', html)[0])
	diploma = "Diploma => %s\n" % str(re.findall('id="ctl00_ContentPlaceHolderMain_lblDiploma" class="gen12">(.*)</span>', html)[0])
	fin = "Fin No => %s\n" % str(re.findall('id="ctl00_ContentPlaceHolderMain_lblUIN" class="gen12">(.*)</span>', html)[0])
	email = "Email => %s@myrp.edu.sg\n" % str(sid)
	ph = "Phone Number => %s\n" % str(re.findall('id="ctl00_ContentPlaceHolderMain_lblContactNo" class="gen12">(.*)</span>', html)[0])
	return msg + name + diploma + fin+email+ph
	

def getAllGrades(sid, password):
	MODULE_SUMMARY_API_URL = "http://emoosx.me/regulus/api/grades/allModuleSummary?"
	data = {"sid" : sid, "password" : password}
	
	MODULE_SUMMARY_API_URL += urllib.urlencode(data)
	try:
		summary_result = urlfetch.fetch(MODULE_SUMMARY_API_URL, method=urlfetch.GET,deadline=100)
		summary_json = json.loads(summary_result.content)
	except urlfetch.DownloadError:
		summary_json = {"error" : "Server is taking too much time. Please try again!"}
		
	msg = ""
	if not "error" in summary_json:
		for module in summary_json:
			msg += "\n" + module["module_code"] + " > " + module["module_name"]
			msg += "\n====================\n"
			for p in summary_json["daily_grades"]:
				msg += "\n" + p
	else:
		msg = summary_json["error"]
	return msg
		
		



def main():
    application = webapp.WSGIApplication([
	      ('/', MainHandler),
	      ('/_ah/xmpp/message/chat/', XmppHandler),
	      ], debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
