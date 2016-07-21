from __future__ import division;
import MySQLdb;
import csv;
import urllib2;
import datetime;
import re;
from bs4 import BeautifulSoup;
from sqlalchemy import *;
from sqlalchemy.ext.automap import automap_base;
from sqlalchemy.orm import Session;
from sqlalchemy.ext.declarative import declarative_base;

from loadPageSource import loadPageSource;

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

#     t = Team('teams', MetaData(bind=None),
#       Column('id', Integer(), table=<teams>, primary_key=True, nullable=False),
#       Column('name', String(), table=<teams>),  
#       Column('second_name', String(), table=<teams>), 
#       schema=None)

#     t.create(checkfirst=True)

#----------------------------------------------------------------------------

class Team(Base):
     __tablename__ = 'teams'

     id = Column(Integer(), primary_key=True, unique=True)
     name = Column(String(50), unique=True)
     second_name = Column(String(50), unique=False)

     def __repr__(self):
        return "<Team(name='%s', second_name='%s')>" % (
                            self.name, self.second_name)

#----------------------------------------------------------------------------

class TourneyResults(Base):
    __tablename__ = 'tourney_results'

    season_id = Column(String(1), primary_key=True, unique=False)
    name = Column(String(50), unique=False)
    wins = Column(Integer(), unique=False)
    pointDif = Column(Integer(), unique=False)

    def __repr__(self):
        return "<TourneyResults(season_id='%s' name='%s', wins='%d', pointDif='%d')>" % (
                            self.season_id, self.name, self.wins, self.pointDif)

#-------------------------------------------------------------------------

# Tried to throw in loadPageSource.py, but that was difficult to accomplish without having circular dependencies
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
                my_team = Team(name=a.getText().encode("utf-8"), second_name="")
                session.add(my_team)

    session.commit()
#----------------------------------------------------------------

# There are name discrepencies in the data (ex. North Carolina = UNC). I decided to do this manually to save time.
def loadSecondNames(session, numberOfYears):

    # ONLY USED IF FINDING NEW NAME DISCREPENCIES #
    rootTourneyLink1 = "http://www.sports-reference.com/cbb/postseason/"
    rootTourneyLink2 = "-ncaa.html" 
    now = datetime.datetime.now()
    if 4 < now.month:
        startYear = now.year
    else:
        startYear = now.year - 1
    # -------------------------------------- #

    teamDict = {key: '' for key, in session.query(Team.name)}

    # ############ HARDCODED NAMES ############ #
    teamDict['North Carolina'] = 'UNC'
    teamDict['Saint Joseph\'s'] = 'St. Joseph\'s'
    teamDict['Southern California'] = 'USC'
    teamDict['Louisiana State'] = 'LSU'
    teamDict['Southern Methodist'] = 'SMU'
    teamDict['Mississippi'] = 'Ole Miss'
    teamDict['Connecticut'] = 'UConn'
    teamDict['Massachusetts'] = 'UMass'
    teamDict['Brigham Young'] = 'BYU'
    teamDict['Pittsburgh'] = 'Pitt'
    teamDict['Virginia Commonwealth'] = 'VCU'
    teamDict['UC-Santa Barbara'] = 'UCSB'
    teamDict['East Tennessee State'] = 'ETSU'
    teamDict['Central Connecticut State'] = 'Central Connecticut'
    teamDict['Pennsylvania'] = 'Penn'
    teamDict['Nevada-Las Vegas'] = 'UNLV'
    teamDict['Central Florida'] = 'UCF'
    teamDict['Detroit Mercy'] = 'Detroit'
    teamDict['Illinois-Chicago'] = 'UIC'
    teamDict['Long Island University'] = 'LIU-Brooklyn'
    teamDict['Texas-San Antonio'] = 'UTSA'
    teamDict['Saint Peter\'s'] = 'St. Peter\'s'
    teamDict['Southern Mississippi'] = 'Southern Miss'
    teamDict['Texas-El Paso'] = 'UTEP'
    teamDict['Maryland-Baltimore County'] = 'UMBC'

    # ######################################## #

    # Used to analyze which team names are missing.
    # NOT GETTING ALL THE TEAMS
    for x in range(0, numberOfYears):
        movingYear = startYear - x
        sourceTemp = loadPageSource(rootTourneyLink1 + str(movingYear) + rootTourneyLink2)
        soup = BeautifulSoup(sourceTemp, 'html.parser')
        for a in soup.find_all('a'):
            if a.parent.parent.name == "td" or a.parent.parent.name == "p":
                if a.parent.name == "p" or a.parent.name == "br":
                    if not (re.search(r'\d', a.getText())) \
                        and not(a.getText().encode("utf-8") in teamDict.keys()) \
                        and not (a.getText().encode("utf-8") in teamDict.values()):

                        # print a.getText().encode("utf-8")
                        continue


    for instance in session.query(Team):
        instance.second_name = teamDict[instance.name]


    session.commit()

#----------------------------------------------------------------
def isInt(String):
    return re.search(r'\d', String)

# Loads win and score differential data from two given indices
def loadGame(d, teams, scores, index1, index2):
    # Load point differential.
    d[teams[index1]][1] += scores[index1] - scores[index2]
    d[teams[index2]][1] += scores[index2] - scores[index1]

    # If upper team score < lower team score...
    if scores[index2] < scores[index1]:
        d[teams[index1]][0] += 1
    else:
        d[teams[index2]][0] += 1 

def loadTourneyResults(session, numberOfYears):
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

    teamNameList = [instance.name for instance in session.query(Team)]
    secondNameList = [instance.second_name for instance in session.query(Team)]

    

    siteData = []
    for a in soup.find_all('a'):
        if a.parent.parent.name == "td" or a.parent.parent.name == "p":
            if a.parent.name == "p" or a.parent.name == "br":
                siteData.append(a.getText().encode("utf-8"))
                # print a.getText().encode("utf-8")


    # Gets list of teams if they have a corresponding score
     # or x > 250
    teamList = [siteData[x] for x in range(0, len(siteData)) if not isInt(siteData[x]) and (isInt(siteData[x+1])) ]

    scoreList = [int(x) for x in siteData if isInt(x)]

    # teamDict keeps track of wins and point differential -- [# wins, point differential]
    teamDict = {key: [0, 0] for key in teamList}

    for x in range(0, len(scoreList)):
        print teamList[x] + " " + str(x) + ", " + str(scoreList[x])
    print('-------------------------------------------------------')

    # The two teams that play each other in a given game are not next to each other in the html format.
    # The teams that play each other are matched up based on haw many total games they play and 
    # the loaction of their name in teamsList.
    baseIndex = 0
    for x in range(0, 8):
        baseIndex = x * 15

        # Loads all the games that the first or sixth seed would play if they won every game
        for y in range(0, 4):
            # upperIndex is the index of a team that appears earlier in teamList, lowerIndex is the other.
            upperIndex = baseIndex + y
            lowerIndex = int(baseIndex + float(y**3)/3 + 5/3 * y + 4)

            loadGame(teamDict, teamList, scoreList, upperIndex, lowerIndex)

            # The top game in this regional bracket has already been loaded. This break prevents it from being loaded again.
            if y == 2 and x % 2 == 1:
                break

        loadGame(teamDict, teamList, scoreList, baseIndex + 5, baseIndex + 7)
        loadGame(teamDict, teamList, scoreList, baseIndex + 8, baseIndex + 11)
        loadGame(teamDict, teamList, scoreList, baseIndex + 9, baseIndex + 13)  
        loadGame(teamDict, teamList, scoreList, baseIndex + 12, baseIndex + 14)      

    loadGame(teamDict, teamList, scoreList, 120, 122)
    loadGame(teamDict, teamList, scoreList, 123, 125)
    loadGame(teamDict, teamList, scoreList, 121, 124)

    for q in teamDict.keys():
        if teamDict[q][0] > 0:
            print q + " " + str(teamDict[q][0]) + ", " + str(teamDict[q][1])

        # Creates list of team names from list of number of games played using list comprehension. Not used anymore, but kept around for reference.
        # alternateTeamsList = [teamList[baseIndex + sum(numGamesPlayedList[0:i]): baseIndex + sum(numGamesPlayedList[0:i]) + numGamesPlayedList[i]] for i in range(0, len(numGamesPlayedList))]

    # siteData = [(team, points) for team in siteData if ]

                

    # for x in range(0, numberOfYears):
    #     print startYear - x

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

# Load team names into a table
# loadTeams(mainSession)

# loadSecondNames(mainSession, 25)

# Load the results of the NCAA tournament from the past x years
loadTourneyResults(mainSession, 25)

print "FINISHED  WTIH 0 ERRORS"