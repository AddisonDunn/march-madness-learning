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

	Mia mia = new Mia();

	# ITERATE THROUGH YEARS:
	currentYear = 2014
	tourneyResultList = [instance for instance in session.query(TourneyResult).filter(TourneyResult.season == currentYear)]
	teamList = [result.name for result in tourneyResultList]


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