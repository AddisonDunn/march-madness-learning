import MySQLdb;
import csv;
from loadData import loadData;
#----------------------------------------------------------------------------


#----------------------------------------------------------------------------

#MAIN

dbName = "madnessData"

db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="password",  # your password
                     db=dbName)        # name of the data base

loadData(db, 'teams', 'data/teams.csv', False)
loadData(db, 'regularSeasonResults', 'data/regular_season_results.csv', False)


print "FINISHED  WTIH 0 ERRORS"