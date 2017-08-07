from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt
import random
import numpy as np

winningPowerBalls = []
winningWhiteBalls = []
randomWhiteList = []
randomPowerList = []
drawDates = []
averages = []
# Dates indicate starting dates for the game changes (refer to discoveries.txt)

# April 22, 1992,   Pick 5 of 45, Pick 1 of 45
# empty because insufficient data was recorded
URL1 = ''

# November 5, 1997, Pick 5 of 49, Pick 1 of 42
URL2 = 'http://www.powerball.com/powerball/pb_nbr_history.asp?startDate=10%2F5%2F2002&endDate=11%2F5%2F1997'

# October 9, 2002,  Pick 5 of 53, Pick 1 of 42
URL3 = 'http://www.powerball.com/powerball/pb_nbr_history.asp?startDate=8%2F31%2F2005&endDate=10%2F9%2F2002'

# August 28, 2005,  Pick 5 of 55, Pick 1 of 42
URL4 = 'http://www.powerball.com/powerball/pb_nbr_history.asp?startDate=1%2F3%2F2009&endDate=8%2F31%2F2005'

# January 7, 2009,  Pick 5 of 59, Pick 1 of 39
URL5 = 'http://www.powerball.com/powerball/pb_nbr_history.asp?startDate=1%2F14%2F2012&endDate=1%2F3%2F2009'

# January 15, 2012, Pick 5 of 59, Pick 1 of 35
URL6 = 'http://www.powerball.com/powerball/pb_nbr_history.asp?startDate=10%2F3%2F2015&endDate=1%2F18%2F2012'

# October 7, 2015,  Pick 5 of 69, Pick 1 of 26
URL7 = 'http://www.powerball.com/powerball/pb_nbr_history.asp?startDate=12%2F17%2F2016&endDate=10%2F3%2F2015'


# Scrape the URL
def scrape(url):

    r = requests.get(url)
    data = r.text

    soup = BeautifulSoup(data, "html.parser")

    # get all of the winning WHITE BALLS
    for whiteBalls in soup.find_all('td', {'background': '/images/ball_white_40.gif'}):
        winningWhiteBalls.append(int(whiteBalls.contents[0]))

    # get all of the winning POWER BALLS
    for redBalls in soup.find_all('td', {'background': '/images/ball_red_40.gif'}):
       winningPowerBalls.append(int(redBalls.contents[0]))

    # get all of the draw dates
    for dates in soup.find_all('b'):
        drawDates.append(dates.contents[0])

    # Special case where the first two items in drawDates are not dates, so get rid of them.
    for i in range(2):
        drawDates.pop(0)


# Plot the historgrams
def plotHist():
    whiteBins = np.arange(71)
    powerBins = np.arange(28)
    fig, axes = plt.subplots(nrows=2, ncols=2)
    ax0, ax1, ax2, ax3 = axes.flat

    # Plot for the white balls (1 - 69)
    ax0.hist(winningWhiteBalls, whiteBins, range=None, normed=False, weights=None, cumulative=False,
             bottom=None, histtype='bar', align='left', orientation='vertical', rwidth=None, log=False,
             color='blue', label=None, stacked=True)
    ax0.legend(prop={'size': 10})
    ax0.set_title('Winning White Balls')


    # Plot for the power balls (1 - 26)
    ax1.hist(winningPowerBalls, powerBins, range=None, normed=False, weights=None, cumulative=False,
             bottom=None, histtype='bar', align='left', orientation='vertical', rwidth=None, log=False,
             color='red', label=None, stacked=True)
    ax1.set_title('Winning Power Balls')

    # Plot for randomly generated frequencies 1- 69
    ax2.hist(randomWhiteList, whiteBins, range=None, normed=False, weights=None, cumulative=False,
             bottom=None, histtype='bar', align='left', orientation='vertical', rwidth=None, log=False,
             color='red', label=None, stacked=True)
    ax2.set_title('Random Frequency 1 - 69')

    # Plot for randomly generated frequencies 1 - 26
    ax3.hist(randomPowerList, powerBins, range=None, normed=False, weights=None, cumulative=False,
             bottom=None, histtype='bar', align='left', orientation='vertical', rwidth=None, log=False,
             color='red', label=None, stacked=True)
    ax3.set_title('Random Frequency 1 - 26')

    plt.tight_layout()
    plt.show()


# creates randomly generated lists for white balls and power balls
def createRandomList():

    # White balls
    for i in range(500):
        randomWhiteList.append(random.randrange(1, 70, 1))

    # Power balls
    for i in range(100):
        randomPowerList.append(random.randrange(1, 27, 1))


scrape(URL7)
createRandomList();
plotHist()
