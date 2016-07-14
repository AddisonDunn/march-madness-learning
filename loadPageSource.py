import urllib2;
import datetime;
from bs4 import BeautifulSoup;

# http://stackoverflow.com/questions/3949744/python-http-download-page-source
def loadPageSource(link):
	user_agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3'
	headers = { 'User-Agent' : user_agent }
	req = urllib2.Request(link, None, headers)
	response = urllib2.urlopen(req)
	page = response.read()
	response.close()
	return page


#-----------------------------------------------------------------------------

def loadTourneyResults(numberOfYears):
	rootTourneyLink1 = "http://www.sports-reference.com/cbb/postseason/"
	rootTourneyLink2 = "-ncaa.html"

	now = datetime.datetime.now()

	# If the current month is April or before the data from this year has probably not been uploaded yet
	if 4 < now.month:
		startYear = now.year
	else:
		startYear = now.year - 1

	sourceTemp = loadPageSource(rootTourneyLink1 + str(startYear) + rootTourneyLink2)
	soup = BeautifulSoup(sourceTemp, 'html.parser')


	for a in soup.find_all('a'):
		if a.parent.parent.name == "td":
			if a.parent.name == 'p':
				print a.getText().encode("utf-8")

	# for x in range(0, numberOfYears):
	# 	print startYear - x

#----------------------------------------------------------------