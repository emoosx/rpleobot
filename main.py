from google.appengine.ext import webapp
from google.appengine.api import xmpp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import xmpp_handlers
from BeautifulSoup import BeautifulSoup
import urllib
import re

HELP_MSG = "Welcome to automated LEO bot for RP \n====================\n Following features are supported - \n 1. /grades \n 2. /rj \n 3. /timetable \n 4. /ce \n 5. /gpa \n 6. /me \n More features to be implemented soon. Developed by *Kaung Htet Zaw* (emoosx@gmail.com)\n====================\nUSAGE EXAMPLE\n====================\n/grades 12345:password\n/timetable 12345:password"

class MainHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write("Life is short, use python!")


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


#helper methods to do respective actions
def getTimetable(sid, password):
	site = "http://emoosx.me/leoapp/timetable.php?"
	site += urllib.urlencode({"sid" : str(sid), "password":str(password)})
	html = str(urllib.urlopen(site).read())
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
	problem_list = re.findall("SELECTED> (.+)</OPTION>",html)
	question = re.search("<font class=iContent>Question:(.*)</font><BR><br>", str(html), re.S)
	if (len(problem_list) > 0 and question):
		#response = re.search("<font class=iContent>Response: (.*) </font>", str(html), re.S)
		#response = response.groups()[0]
		msg = "RJ Question - Problem > %s\n====================\n" % problem_list[0]
		msg += question.groups()[0].strip()
		#msg += "\n====================\nStatus :: "
		#if response != "No Submission":
		#	msg += "*Submitted*"
		#else:
		#	msg += "*Not Submitted Yet*"
		return msg
	return "No Reflection Journal Assigned Yet!"

def getGrades(sid, password):
	site = "http://emoosx.me/leoapp/recentGrades.php?"
	site += urllib.urlencode({"sid": str(sid), "password":str(password)})
	html = urllib.urlopen(site).read()
	modules = re.findall("'_blank'>([A-Z][0-9][0-9][0-9])-", str(html))
	problems = re.findall("Problem ([1-9]{1,2})", str(html))
	grades = re.findall("\}' target='_blank'>([ABCDFX])<", str(html))
	msg = 'Recent Grades\n====================\n'
	for i in range(len(modules)):
		msg += "%s > Problem-(%s)%3s\n" % (modules[i], problems[i], grades[i])
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

def main():
    application = webapp.WSGIApplication([
	      ('/', MainHandler),
	      ('/_ah/xmpp/message/chat/', XmppHandler),
	      ], debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
