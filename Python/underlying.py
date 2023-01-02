import math
import numpy as np

class Underlying:
	"""
	Instances of this class represent the underlying contract for an option
		Attributes:
			name (string) : The name of the underlying contract
			settlement (string) : Spot/Futures
			S_0 (float) : The current price of the underlying contract
			t (datetime) : The current time
			r (float) : The risk free rate
			q (float) : The dividend yield
			b (float) : The generalised cost of carry parameter

			trading_days_per_year (float) : The number of trading days per year for the underlying contract
	"""
	def __init__(self, name, settlement, S_0, t, r, q):
		"""
		Initialises the class for the underlying contract
			Parameters:
				name (string) : The name of the underlying contract
				settlement (string) : Spot/Futures
				S_0 (float) : The current price of the underlying contract
				t (datetime) : The time for the underlying contract
				r (float) : The risk free rate
				q (float) : The dividend yield
		"""
		self.name = name
		self.S_0 = S_0
		self.t = t
		self.r = r
		self.q = q
		if settlement == "Spot":
			self.b = r - q
		elif settlement == "Futures":
			self.b = 0
		trading_days_per_year_dict = {"BTC":365.25, "SPX":252}
		self.trading_days_per_year = trading_days_per_year_dict[name]

	def __repr__(self):
		string = f"""Name: {self.name}
		Current price: {self.S_0}
		Time: {self.t}
		Risk free rate: {self.r}
		"""
		return string