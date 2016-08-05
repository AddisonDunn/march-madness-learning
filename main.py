import MySQLdb;
from sqlalchemy import *;
from sqlalchemy.ext.automap import automap_base;
from sqlalchemy.orm import Session, relationship;
from sqlalchemy.ext.declarative import declarative_base;
from loadData import Team, SeasonResult, TourneyResult;
from mia import Mia;

Base = automap_base()

#----------------------------------------------------------------------------

def mainAlgo(session):

	mia = Mia()

	# ITERATE THROUGH YEARS:
	currentYear = 2014
	# tourneyResultList = [instance for instance in session.query(TourneyResult).filter(TourneyResult.season == currentYear)]
	# tourneyNameLIst = [instance.name for instance in tourneyResultList]
	tourneyResultDict = {instance.name : instance.wins for instance in session.query(TourneyResult).filter(TourneyResult.season == currentYear)}
	seasonResultList = [instance for instance in session.query(SeasonResult).filter(SeasonResult.season == currentYear)]
	

	for entry in seasonResultList:
		if entry.name in tourneyResultDict.keys():
			print entry.name
			print entry
			mia.train(tourneyResultDict[entry.name], entry)
			break

	


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


mainAlgo(mainSession)