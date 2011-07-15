from google.appengine.ext import webapp
from google.appengine.api import xmpp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import xmpp_handlers
from google.appengine.ext.webapp.template import render
from BeautifulSoup import BeautifulSoup
import urllib
import re
from os import path

HELP_MSG = """Welcome to automatd LEO bot for RP
====================
Following features are supported -
1. /grades (includes UT grades)
2. /rj (includes submission status)
3. /timetable
4. /ce
5. /gpa
6. /me
7. /gradesall (beta)

*Please notice that I do not store your credentials. The source code will be open-sourced soon*.

If you enjoy using it, buy me a RedBull if you run into me in koufu :P
====================
Developed by _*Kaung Htet Zaw*_ . 
====================
Mail to emoosx@gmail.com for Bug reports & feature suggestions.

USAGE EXAMPLE
-------------
/grades 91234:password
/timetable 91234:password
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

	def timetable_command(self, message=None):
		colon_index = message.arg.index(":")
		sid = str(message.arg[0:colon_index])
		password = str(message.arg[colon_index+1:])
		message.reply(getTimetable(sid, password))

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
def getTimetable(sid, password):
	site = "http://emoosx.me/leoapp/timetable.php?"
	site += urllib.urlencode({"sid" : str(sid), "password":str(password)})
	html = str(urllib.urlopen(site).read())
	if re.search("<TITLE> Fail to access LEO </TITLE>", html):
		return "Wrong username/password combination"
	else:
		html = html.replace('<br>','\r\n')
		strip = ['small', 'i', 'b', 'td']
		for char in strip:
			html = html.replace('<'+char+'>','').replace('</'+char+'>','')
		soup = BeautifulSoup(html).contents[0].contents[1].findAll('tr')
		msg = "TimeTable\n====================\n"
		for i in range(2, len(soup)):
			each = soup[i].renderContents()
			result = re.sub('<.{0,22}>', "",each)
			msg += result + "\n====================\n" 
		return msg


def getRJ(sid, password):
	site =  "http://emoosx.me/leoapp/rj.php?"
	site += urllib.urlencode({"sid": str(sid), "password":str(password)})
	html = urllib.urlopen(site).read()
	
	if re.search("<TITLE> Fail to access LEO </TITLE>", html):
		return "Wrong username/password combination"
	else:
		problem_list = re.findall("SELECTED> (.+)</OPTION>",html)
		question = re.search("<font class=iContent>Question:(.*)</font><BR><br>", str(html), re.S)
		if (len(problem_list) > 0 and question):
			response = re.search("<font class=iContent>Response: (.*) </font>", str(html), re.S)
			response = response.groups()[0]
			msg = "RJ Question - Problem > %s\n====================\n" % problem_list[0]
			msg += question.groups()[0].strip()
			msg += "\n====================\nStatus :: "
			if response != "No Submission":
				msg += "*Submitted*"
			else:
				msg += "*Not Submitted Yet*"
				return msg
		return "No Reflection Journal Assigned Yet!"

def getGrades(sid, password):
	site = "http://emoosx.me/leoapp/recentGrades.php?"
	site += urllib.urlencode({"sid": str(sid), "password":str(password)})
	html = str(urllib.urlopen(site).read())
	
	if re.search("<TITLE> Fail to access LEO </TITLE>", html):
		return "Wrong username/password combination"
	else:
		modules = re.findall("'_blank'>([A-Z][0-9][0-9][0-9])-", html)
		problems = re.findall("Problem (\d{1,2})", html)
		grades = re.findall("\}' target='_blank'>([ABCDFX])<", html)
		utModules = re.findall("'_blank'>(.{4})-\d-.{4}-\w</a>.{300,303}UT", html)
		utNo = re.findall("UT ([1-3])", html)
		utGrades = re.findall("}&order=1' target='_blank'>(.{1,2})<", html)
		msg = 'Recent Daily Grades\n====================\n'
		for i in range(len(modules)):
			msg += "%s > Problem-(%s)%3s\n" % (modules[i], problems[i], grades[i])
		msg += "\n====================\nUT Grades\n====================\n"
		if(len(utModules) > 0):		
			for j in range(len(utModules)):
				msg += "%s > UT-(%s)%3s\n" % (utModules[j], utNo[j], utGrades[j])
		else:
			msg += "No UT Grades Published Yet"
		return msg.strip('\n')
	
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
	site = "http://emoosx.me/leoapp/recentGrades.php?"
	site += urllib.urlencode({"sid": sid, "password": password})
	html = urllib.urlopen(site).read()
	
	if re.search("<TITLE> Fail to access LEO </TITLE>", html):
		return "Wrong username/password combination"
	else:
		modules = re.findall("'_blank'>([A-Z][0-9][0-9][0-9])-", html)
		courseid = re.findall("projectweb\/student_summary.asp\?courseid=(.{38})", html, re.S)
		msg = ""
		for i,module in enumerate(modules):
			msg += "\n\nModule Summary for %s" % module
			msg += "\n====================\n"
			msg += getAllGradesInAModule(sid, password, courseid[i])
		return msg
		
def getAllGradesInAModule(sid, password, courseid):
	site = "http://emoosx.me/leoapp/moduleSummary.php?"
	site += urllib.urlencode({"sid" :sid, "password" : password, "courseid" :courseid})
	html = urllib.urlopen(site).read()
	problem_grades = re.findall("<b>([ABCDFX])</b>", html)
	ut_grades = re.findall("<font class=iContent>(.{1,2})</font>", html)
	msg = ""
	for problem in range(len(problem_grades)):
		msg += "\nProblem %d => %s" %(problem+1, problem_grades[problem])
	msg += "\n--------------------"
	for ut in range(len(ut_grades)):
		msg += "\n UT %d => %s" %(ut+1, ut_grades[ut])
	return msg

def main():
    application = webapp.WSGIApplication([
	      ('/', MainHandler),
	      ('/_ah/xmpp/message/chat/', XmppHandler),
	      ], debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
