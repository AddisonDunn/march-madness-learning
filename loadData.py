import MySQLdb;
import csv;
#----------------------------------------------------------------------------


# http://stackoverflow.com/questions/17044259/python-how-to-check-if-table-exists
def checkTableExists(db, tablename):
    dbcur = db.cursor()
    dbcur.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = '{0}'
        """.format(tablename.replace('\'', '\'\'')))
    if dbcur.fetchone()[0] == 1:
        dbcur.close()
        return True

    dbcur.close()
    return False


def loadData(db, tableName, csvName, OVERWRITE = False):
	# you must create a Cursor object. It will let
	#  you execute all the queries you need
	cursor = db.cursor()

	# if the table already exists then we cannot load the data
	if checkTableExists(db, tableName):
		if OVERWRITE:
			cursor.execute("DROP TABLE {}".format(tableName))
		else:
			print "Table \'{}\' already exists, moving on...".format(tableName)
			return


	csv_data = csv.reader(file(csvName))

	# pop the first two lines -- the first line has the field name and the second has an example of the date so we can figure out the type
	first_line = next (csv_data, None) # ', None' - don't raise exception if line does not exist
	second_line = next(csv_data, None)

	if first_line[0].lower() == 'id':
		hasIdField = True;
	else:
		hasIdField = False;

	# create table assuming it will have an id field
	cursor.execute('CREATE TABLE {} (id INT NOT NULL PRIMARY KEY)'.format(tableName))

	if not hasIdField:
		try: 
			int(second_line[0])
			cursor.execute("ALTER TABLE {} ADD %s INT(15)".format(tableName) % (first_line[0]))
		except ValueError:
			cursor.execute("ALTER TABLE {} ADD %s CHAR(75)".format(tableName) % (first_line[0]))

	for x in range(1, len(first_line)):
		try: 
			int(second_line[x])
			cursor.execute("ALTER TABLE {} ADD %s INT(15)".format(tableName) % (first_line[x]))
		except ValueError:
			cursor.execute("ALTER TABLE {} ADD %s CHAR(75)".format(tableName) % (first_line[x]))

	x = 1;
	if not hasIdField:
		cursor.execute("INSERT INTO {} VALUES %r;".format(tableName) % ((x,) +tuple(second_line),) )
		# automatically starts with third row because of the next() method
		for row in csv_data:
			x += 1
			cursor.execute("INSERT INTO {} VALUES %r;".format(tableName) % ((x,) + tuple(row),) )
			
	else:
		cursor.execute("INSERT INTO {} VALUES %r;".format(tableName) % (tuple(second_line),) )
		# automatically starts with third row because of the next() method
		for row in csv_data:	
			cursor.execute("INSERT INTO {} VALUES %r;".format(tableName) % (tuple(row),) )

	#close the connection to the database.
	db.commit()
	cursor.close()
	print "Data Loaded! (table \'{}\')".format(tableName)

#----------------------------------------------------------------------------
