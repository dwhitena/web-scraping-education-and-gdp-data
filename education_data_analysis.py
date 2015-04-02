import pandas as pd
import sqlite3 as lite
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm

# ---------------------------
# LOAD DATA
# ---------------------------

# connect to database
con = lite.connect('education.db')
cur = con.cursor()

# read the weather data into a dataframe
df = pd.read_sql_query("SELECT t1.country, t1.year, men, women, gdp \
	FROM undata t1 \
	INNER JOIN gdpdata t2 ON t1.country=t2.country \
	AND t1.year=t2.year", con)

df.dropna(inplace=True)

# ---------------------------
# VISUALIZE DATA
# ---------------------------

# histogram of GDPs
plt.figure()
df['gdp'].hist()
plt.draw()
plt.savefig('gdp_histogram.png')

# SLE = School Life Expectancy
# scatter plots of SLE vs. gdp:

plt.figure()
plt.scatter(df['gdp'], df['men'], alpha=0.3)
plt.xlabel('GDP')
plt.ylabel('School Life Expectancy (Male)')
plt.draw()
plt.savefig('maleSLE_vs_gdp.png')

plt.figure()
plt.scatter(df['gdp'], df['women'], alpha=0.3)
plt.xlabel('GDP')
plt.ylabel('School Life Expectancy (Female)')
plt.draw()
plt.savefig('femaleSLE_vs_gdp.png')

plt.figure()
plt.scatter(df['gdp'].map(lambda num: np.log(num)), df['men'], alpha=0.3)
plt.xlabel('log(GDP)')
plt.ylabel('School Life Expectancy (Male)')
plt.draw()
plt.savefig('maleSLE_vs_loggdp.png')


# ---------------------------
# MODEL DATA - LINEAR REGRESSION
# ---------------------------

df['loggdp'] = df['gdp'].map(lambda num: np.log(num))

# shape data
# The dependent variable
y = np.matrix(df['men']).transpose()
# The independent variables shaped as columns
x = np.matrix(df['loggdp']).transpose()

# add column of ones (constant)
X = sm.add_constant(x)

# Linear model
model1 = sm.OLS(y,X).fit()
print 'GDP Coefficient: ', model1.params[1]
print 'Intercept: ', model1.params[0]
print 'P-Values: ', model1.pvalues  # ??? why do these come out zero ???
print 'R-Squared: ', model1.rsquared

# To visualize this see the following plot:
gdpsample = np.arange(min(df.gdp),max(df.gdp), 1000000000)
logsample = np.log(gdpsample)
plt.figure()
plt.scatter(df['loggdp'], df['men'], alpha=0.3)
plt.xlabel('log(GDP)')
plt.ylabel('School Life Expectancy (Male)')
plt.plot(logsample, model1.params[0] + model1.params[1]*logsample, 'r')
plt.draw()
plt.savefig('model_fit.png')


plt.show()