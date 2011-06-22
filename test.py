from BeautifulSoup import BeautifulSoup
import re, urllib

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
	site += urllib.urlencode({"sid":str(sid), "password":str(password)})
	html = str(urllib.urlopen(site).read())
	msg = "Personal Particulars\n====================\n"
	name = "Name => %s\n" % str(re.findall('id="ctl00_ContentPlaceHolderMain_lblName" class="gen12">(.*)</span>', html)[0])
	diploma = "Diploma => %s\n" % str(re.findall('id="ctl00_ContentPlaceHolderMain_lblDiploma" class="gen12">(.*)</span>', html)[0])
	fin = "Fin No => %s\n" % str(re.findall('id="ctl00_ContentPlaceHolderMain_lblUIN" class="gen12">(.*)</span>', html)[0])
	email = "Email => %s@myrp.edu.sg\n" % str(sid)
	ph = "Phone Number => %s\n" % str(re.findall('id="ctl00_ContentPlaceHolderMain_lblContactNo" class="gen12">(.*)</span>', html)[0])
	return msg + name + diploma + fin+email+ph
	
def getFIN(sid, password):
	site = "http://emoosx.me/leoapp/academic.php?"
	site += urllib.urlencode({"sid":str(sid), "password":str(password)})
	name = str(re.findall('id="ctl00_ContentPlaceHolderMain_lblName" class="gen12">(.*)</span>', html)[0])
	fin = str(re.findall('id="ctl00_ContentPlaceHolderMain_lblUIN" class="gen12">(.*)</span>', html)[0])
 	return (name,fin)

def getLibDetails(sid, password):
	site = "http://libopac.rp.edu.sg/cgi-bin/cw_cgi?25335+patronLogin+3089"
	return "nil"

def getAllGrades(sid, password):
	recent_grades_url = "http://emoosx.me/leoapp/recentGrades.php?"
	recent_grades_url += urllib.urlencode({"sid":str(sid), "password":str(password)})
	recent_grades_html = str(urllib.urlopen(recent_grades_url).read())
	modules = re.findall("'_blank'>([A-Z][0-9][0-9][0-9])-", str(recent_grades_html))
	modules_url = re.
	print modules
	print problems
	print grades
	
	

sid = "91178"
password = "parphoungM@"
print getAllGrades(sid, password)
#print getRJ("91329", "Ji@yo#year3")
#print getRJ("91155","Dv311mc4y0")


