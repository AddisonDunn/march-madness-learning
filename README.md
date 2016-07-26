# march-madness-learning

CURRENT STATUS: all data uploads. ML algorithm is in development.

Using Python (2.7) and SQL to predict the results of the NCAA basketball tourney. loadData.py load the sports data into a mySQL database and main.py is where the algorithm is performed on the information in the database. So run loadData and then main.

I used Sublime Text 2 to develop this project. If you use it, you should purchase the license (https://www.sublimetext.com/buy?v=3). SQLAlchemy is used to make mySQL easier to use from python; download and donate (http://www.sqlalchemy.org/). BeautfulSoup is beautiful. It was used to extract data from web pages (https://www.crummy.com/software/BeautifulSoup/bs4/doc/). 

The data is from http://www.sports-reference.com/cbb/, the college basketball-related portion of a cool sports statistics site. I highly reccomend it for all projects using sports statistics. 

Formerly, offline csv files were used as the source of data. This proved to be impractical. However, the code will remain in this project (primarily loadData.py) as I believe it could be very useful to others.

I used Python 2.7 on this project. It is likely you will have problems using any files on this repository running Python 3.

Feel free to contact me, and enjoy!

season_results:
![alt tag](https://github.com/AddisonDunn/march-madness-learning/blob/master/screenshots/seasonResults.png)
