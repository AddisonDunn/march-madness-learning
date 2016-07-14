import MySQLdb;
import csv;
import urllib2;
import datetime;
from bs4 import BeautifulSoup;
from loadData import loadData;
from loadPageSource import loadTourneyResults, loadPageSource;
from sqlalchemy import *;
from sqlalchemy.ext.automap import automap_base;
from sqlalchemy.orm import Session;
from sqlalchemy.ext.declarative import declarative_base;

Base = automap_base()


#----------------------------------------------------------------------------

# Assumes database already exists. If it does not, error is thrown
# def startDatabase(host, username, pword, name):

	# newDb = MySQLdb.connect(host="localhost",    # your host, usually localhost
	#                      user=username,         # your username
	#                      passwd=pword,  # your password
	#                      db=name)        # name of the data base

#----------------------------------------------------------------------------

# def createTeamsTable(engine):

# 	t = Team('teams', MetaData(bind=None),
# 	  Column('id', Integer(), table=<teams>, primary_key=True, nullable=False),
# 	  Column('name', String(), table=<teams>),  
# 	  Column('second_name', String(), table=<teams>), 
# 	  schema=None)

# 	t.create(checkfirst=True)

#----------------------------------------------------------------------------

class Team(Base):
     __tablename__ = 'teams'

     id = Column(Integer(), primary_key=True, unique=True)
     name = Column(String(50), unique=True)
     fullname = Column(String(50), unique=False)

     def __repr__(self):
        return "<Team(name='%s', fullname='%s')>" % (
                            self.name, self.fullname)

#----------------------------------------------------------------------------

def loadTeams(session):
	rootTourneyLink1 = "http://www.sports-reference.com/cbb/seasons/"
	rootTourneyLink2 = "-school-stats.html"

	now = datetime.datetime.now()

	# If the current month is April or before the data from this year has probably not been uploaded yet
	if 4 < now.month:
		startYear = now.year
	else:
		startYear = now.year - 1

	sourceTemp = loadPageSource(rootTourneyLink1 + str(startYear) + rootTourneyLink2)
	soup = BeautifulSoup(sourceTemp, 'html.parser')

	for a in soup.find_all('a'):
		if a.parent.parent.name == "tr":
			if a.parent.name == 'td':
				my_team = Team(name=a.getText().encode("utf-8"), fullname="")
				session.add(my_team)
	session.commit()

#----------------------------------------------------------------------------

#MAIN

username = "root"
pword = "password"
name = "madnessdata"

# Initialize the database :: Connection & Metadata retrieval
engine = create_engine('mysql+mysqldb://' + username + ':' + pword + '@localhost/' + name)
Base.prepare(engine, reflect=True)

# SqlAlchemy :: Starts a session
mainSession = Session(engine)

Base.metadata.create_all(engine)

# mainSession = startDatabase(Base, "localhost", "root", "password", "madnessdata")

# createTeamsTable(mainEngine)

# Load the results of the NCAA tournament from the past x years
#loadTourneyResults(20)
loadTeams(mainSession)

print "FINISHED  WTIH 0 ERRORS"