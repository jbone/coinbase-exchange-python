#
# CoinbaseExchange/CandlestickDO.py
# Daniel Paquin
#
# A data object to store an individual candlestick
#

class CandlestickDO():
	def __init__(self, time = "", low = "", high = "", Open = "", close = "", volume = ""):

		# New properties for CBEOrderDO
		self.time = time
		self.low = low
		self.high = high
		self.open = Open
		self.close = close
		self.volume = volume