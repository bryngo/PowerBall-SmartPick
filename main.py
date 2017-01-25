from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import random
import numpy as np
from twilio.rest import TwilioRestClient

account_sid = "ACec8e89fbcc98bc086180e75ba263bce4"
auth_token = "239d886ffe5d7f6f7d4da6e0d886f966"
client = TwilioRestClient(account_sid, auth_token)

winningPowerBalls = []
winningWhiteBalls = []
drawDates = []
random_list = []
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


# makes a random list of numbers
def makeRanList():
    for i in range(535):
        random_list.append(random.randrange(1, 70, 1))


# helper function to compare random list of numbers to actual pulled numbers
def getDelt(white, rand):

    delt = []

    for i in range(len(white)):
        delta = white[i] - rand[i]
        delt.append(delta)

    sum = np.cumsum(delt)

    avergae = sum / len(white)

    averages.append(avergae)



def getStats():

    n_white, bins_white, patches_white = plt.hist(winningWhiteBalls, bins=range(71), range=None, normed=False, weights=None, cumulative=False, bottom=None, histtype='bar', align='mid', orientation='vertical', rwidth=None, log=False, color='blue', label=None, stacked=True, hold=None)
    #plt.hist(winningPowerBalls, bins=range(28), range=None, normed=False, weights=None, cumulative=False, bottom=None, histtype='bar', align='mid', orientation='vertical', rwidth=.75, log=False, color='red', label=None, stacked=True, hold=None)
    n_rand, bins_rand, patches_rand = plt.hist(random_list, bins=range(71), range=None, normed=False, weights=None, cumulative=False, bottom=None, histtype='bar', align='mid', orientation='vertical', rwidth=.3, log=False, color='red', label=None, stacked=True, hold=None)

    getDelt(n_white, n_rand)


def plotHist():
    whiteBins = np.arange(71)
    powerBins = np.arange(28)
    fig, axes = plt.subplots(nrows=1, ncols=2)
    ax0, ax1 = axes.flat

    ax0.hist(winningWhiteBalls, whiteBins, range=None, normed=False, weights=None, cumulative=False,
             bottom=None, histtype='bar', align='left', orientation='vertical', rwidth=None, log=False,
             color='blue', label=None, stacked=True)
    ax0.legend(prop={'size': 10})
    ax0.set_title('Winning White Balls')

    ax1.hist(winningPowerBalls, powerBins, range=None, normed=False, weights=None, cumulative=False,
             bottom=None, histtype='bar', align='left', orientation='vertical', rwidth=None, log=False,
             color='red', label=None, stacked=True)
    ax1.set_title('Winning Power Balls')

    plt.tight_layout()
    plt.show()

def getAverage():
    sum = np.cumsum(averages)
    avg = sum[len(averages) - 1] / len(averages)

    print(avg)

def runTest(runCount):

    for i in range(runCount):
        makeRanList()
        getStats()
        random_list[:] = []
    getAverage()


scrape(URL7)
#runTest(1)
#makeRanList()
plotHist()