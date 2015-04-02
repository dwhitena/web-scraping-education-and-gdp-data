import pandas as pd
import sqlite3 as lite
import matplotlib.pyplot as plt
import csv

# ---------------------------
# READ IN THE GDP DATA
# ---------------------------

# read in GDP data
df = pd.read_csv('ny.gdp.mktp.cd_Indicator_en_csv_v2.csv', skiprows=2)

# select out the columns of interest (matching UN data)
prng = pd.period_range('1999', '2010', freq='A-DEC')
prng = list(str(periodval) for periodval in prng)
columns_subset = ['Country Name'] + prng
df = df[columns_subset]


# ---------------------------
# STORE THE DATA
# ---------------------------

# store data in SQLite
# connect to database
con = lite.connect('education.db')
cur = con.cursor()

# create and fill table
with con:
	# clear table if it exists
	cur.execute("DROP TABLE IF EXISTS gdpdata")
	# create maxtemps table
	cur.execute("CREATE TABLE gdpdata (country TEXT, year INT, gdp NUMERIC);")
	#loop over countries and years
	for dfidx in df.index: 
		fillvalues = []
		for year in prng:
			fillvalues = fillvalues + [(df.ix[dfidx]['Country Name'], year, df.ix[dfidx][year])]
			# fill dates
		cur.executemany('INSERT INTO gdpdata (country, year, gdp) VALUES (?, ?, ?)', fillvalues)