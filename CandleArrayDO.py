#
# CoinbaseExchange/CandleArrayDO.py
# Daniel Paquin
#
# A data object to store an array of CandlestickDO's
#

class CandleArrayDO():
	def __init__(self, CandlestickArray):

		# CandlestickArray is an array of candletick objects
		self.array = CandlestickArray

	############################
	### Technical Indicators ###
	############################

	def RSI(self, sensitivity):
		#
		# Quantifies momentum.
		# Analysizes the RSI, measuring the number of candles previous to the last
		# in CandlestickArray as noted by sensitivity int. 
		# 100 - 100/(1 + (Average of x periods up / Average of x periods down)
		#
		daysUp, daysDwn = [], [] #to store closing values
		closeUp, closeDown = [], [] #temp array to calculate average
		tot = 0.0 #temp float to calculate averages
		firstCandleNumb = 0 #the first candle - because we want finite eval.

		if len(self.array) < sensitivity:
			# Check to make sure the array is long enough for desired sensitivity.
			firstCandleNumb = 0
		else:
			firstCandleNumb = len(self.array) - sensitivity

		for x in range(firstCandleNumb,len(self.array)):
			# Place closing values in appropriate array
			c = self.array[x]

			if c.close > c.open:
				#If Up period
				closeUp.append(c.close)
				print x+1, "Up", c.close, c.open
			elif c.close < c.open:
				#If Down period
				closeDown.append(c.close)
				print x+1, "Down", c.close, c.open
			else:
				#If no change in period
				print x+1, "No Change", c.close

		if len(closeUp) != 0 and len(closeDown) != 0:
			#Average the values if they aren't zero
			for value in closeUp:
				#TODO: Import numpy.average function
				tot += int(value)
			averageUp = tot/ len(closeUp)
			print "Average close on up candles", averageUp

			tot = 0 #reset temp variable
			for value in closeDown:
				#TODO: Import numpy.average function
				tot += int(value)
			averageDown = tot/ len(closeDown)
			print "Average close on down candles", averageDown
		
			return (100 - 100/(1 + averageUp/averageDown))

		else:
			#Error Result
			return -1

	def SMA(self, period):
		#
		# Simple Moving Average
		# Tells you the average price for the past period
		# Helps you with momentum analysis
		# 
		priceArray = [] #store closing prices to be averaged
		tot = 0 #temp array to calculate averages
		movingAverage = None # final moving average to return

		if len(self.array) < period:
			# Check to make sure the array is long enough for desired period.
			firstCandleNumb = 0
		else:
			firstCandleNumb = len(self.array) - period

		for candleNum in range(firstCandleNumb,len(self.array)):
			priceArray.append( self.array[candleNum] )

		for candle in priceArray:
			tot += candle.close
			movingAverage = tot / period

		return movingAverage

	def EMA(self, period, weight):
		#
		# Exponential Moving Average
		# Tells you the average price for the past period and 
		# discounts older prices given by weight (value 0-1).
		# Higher weight = discounts older prices, faster.
		#
		close = None # closing price of the current candle
		output = None # final moving average to return
		weight = weight or 0.5 # in case user forgets to set a weight
		count = 0

		if len(self.array) < period:
			# Check to make sure the array is long enough for desired period.
			firstCandleNumb = 0
			output = self.array[0].close # inital value is first close

		else:
			firstCandleNumb = len(self.array) - period

			if len(self.array) >= period+5:
				# array is 5 bigger than period, average 5 previous closes as inital value
				output = self.array[firstCandleNumb-5].close
				for prevNum in range(firstCandleNumb-4,firstCandleNumb):
					output += self.array[firstCandleNumb-prevNum].close
					output /= 2

			elif len(self.array) == period:
				# array is same size as period, initalize with first one
				output = self.array[firstCandleNumb].close
				
			else:
				# array is between 0 and 5 bigger than period, initalize with one just before first
				output = self.array[firstCandleNumb-1].close

		for candleNum in range(firstCandleNumb+1,len(self.array)):
			close = self.array[candleNum].close
			output *= 1 - weight
			output += weight * close
			print output, close

		return output

	def percentR(self, period):
		#
		# Williams %R
		# Are the candles trading near the high or low? Output: -100 -> 0
		# Lower the value, the closer the last close is to the lowest in the set.
		# -100 would mean the close is the lowest in the set.
		#
		maximum = None #store highest price in period
		minimum = None #store lowest price in period
		tot = 0 #temp array to calculate averages
		close = None # closing price of the current candle
		output = None # final moving average to return

		if len(self.array) < period:
			# Check to make sure the array is long enough for desired period.
			firstCandleNumb = 0
		else:
			firstCandleNumb = len(self.array) - period

		# Starting point = first close
		maximum = self.array[firstCandleNumb].close
		minimum = self.array[firstCandleNumb].close

		for candleNum in range(firstCandleNumb+1,len(self.array)):
			close = self.array[candleNum].close
			if close > maximum:
				maximum = close
			if close < minimum:
				minimum = close

		# Calculate output
		output = ( (maximum-close) / (maximum-minimum) ) * -100
		print minimum, maximum, output

		return output