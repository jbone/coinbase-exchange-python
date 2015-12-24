#
# CoinbaseExchange/runMe.py
# Daniel Paquin
#
# Technical Indicators
#

import Coinbase
from CandlestickDO import CandlestickDO
from CandleArrayDO import CandleArrayDO
from pprint import pprint

# Initialize Coinbase API Object
cbExchange = Coinbase.Coinbase()

"""
  This script grabs the candles, packages them into a data object, and passes that into 
a function that calculates the RSI value for that historical data set.
"""

# Get Start Time
startTime = "2015-12-20T18:23:24.865Z"
# Get End Time
response = cbExchange.getServerTime()
endTime = response['iso']
# Get Granularity- in seconds
granularity = 60*60

# Make call to CB Exchange
response = cbExchange.getCandlesticks(startTime = startTime, endTime = endTime, granularity = granularity)

# Organize data
CandlestickArray = []
for eachCandle in response:
    # Package candle objects into an array
    Candlestick = CandlestickDO()
    Candlestick.time = eachCandle[0]
    Candlestick.low = eachCandle[1]
    Candlestick.high = eachCandle[2]
    Candlestick.open = eachCandle[3]
    Candlestick.close = eachCandle[4]
    Candlestick.volume = eachCandle[5]
    CandlestickArray.append(Candlestick)

GraphData = CandleArrayDO(CandlestickArray)


calcRSI = GraphData.RSI(14)
print "RSI =", calcRSI

calcSMA = GraphData.SMA(20)
print "SMA(20) =", calcSMA


print startTime, endTime, granularity








