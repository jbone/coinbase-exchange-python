#
# CoinbaseExchange/CBEOrderDO.py
# Daniel Paquin
#
# A data object to process and track an order on coinbase
#

class CBEOrderDO():
	def __init__(self, order_type = "", side = "", product_id = "", stp = "", price = "", size = "",
						time_in_force = "", cancel_after = "", funds = "", orderId = ""):

		# New properties for CBEOrderDO
		self.order_type = order_type
		self.side = side
		self.product_id = product_id
		self.stp = stp
		self.price = price
		self.size = size
		self.time_in_force = time_in_force
		self.cancel_after = cancel_after
		self.funds = funds
		self.orderId = orderId