import sys
import requests
import datetime
import json

import getopt

date_to = datetime.date.today() - datetime.timedelta(days=1)
date_from = date_to - datetime.timedelta(days=6)

class LinearRegression():
    slope = 0
    intercept = 0

    def __init__(self, values):
        sumx = 0
        sumy = 0
        sumx2 = 0

        l = len(values)

        for x, y in enumerate(values):
            sumx += x
            sumx2 += x * x
            sumy += y

        xbar = sumx / l
        ybar = sumy / l

        xxbar = 0.0
        xybar = 0.0

        for x, y in enumerate(values):
            xxbar += (x - xbar) * (x - xbar)
            xybar += (x - xbar) * (y - ybar)

        self.slope = xybar / xxbar
        self.intercept = ybar - self.slope * xbar

    def predict(self, value):
        return self.slope * value + self.intercept

def main(argv):
    verbose = False
    opts, args = getopt.gnu_getopt(argv, 'v', ['verbose'])
    
    for o, a in opts:
        if o in ('-v', '--verbose'):
            verbose = True

    try:
        response = requests.get('https://api.coindesk.com/v1/bpi/historical/close.json?start={}&end={}'.format(date_from, date_to))
        if response:
            data = json.loads(response.content)
            bpi = list(map(lambda v: float(v), data['bpi'].values()))

            lr = LinearRegression(bpi)
            todays_price = lr.predict(len(bpi))
            if (verbose):
                print('Today\'s BTC price prediction: ${:.3f}'.format(todays_price))
            else:
                print('{:.3f}'.format(todays_price))
        else:
            print("Unable to fetch BTC prices")
            sys.exit(1)
    except:
        print("Unable to fetch BTC prices")
        sys.exit(1)


if __name__ == '__main__':
  main(sys.argv[1:])