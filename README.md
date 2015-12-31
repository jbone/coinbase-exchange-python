# coinbase-exchange-python
a simple wrapper for coinbase exchange with some extra goodies

##### Provided under MIT License by Daniel Paquin.

### Coinbase.py
A wrapper for coinbase exchange that needs API keys to functions and has limited usability (for now). 

### CandlestickDO.py
A data object to package an individual candlestick.

### CandleArrayDO.py 
A data object that stores an array of candlestick objects as well as providing functions to analyze the historical data.
Right now, it prints a lot of excess data for validity checking.

### CBEOrderDO.py 
A data object to package an order to make orders easier.
Hasn't been tested yet, but is next on the chopping block.

### runMe.py
A simple script that heavily uses the candlestick objects and calculates SMA and RSI.