class Option:
	"""
	This is the base class for an option which stores common attributes and methods for options
		Attributes
			K (float) : The strike of the option
			style (string) : The style of the option
			otype (string) : The type of the option (Call/Put)
			underlying (Underlying) : The underlying contract for the option
			expiry (datetime) : A datetime object for the expiry of the option
			vol (float) : The volatility input for the option
			time_to_expiry (float) : The time until the option expries in years

			value (float) : The theoretical value of the option
			delta (float) : The delta of the option
			gamma (float) : The gamma of the option
			relative_gamma (float) : The relative gamma of the option
			theta (float) : The theta of the option
			vega (float) : The vega of the option
			rho (float) : The rho of the option
		Methods
			CalculateTimeToExpiry() : Calculates and sets the time until the option expires
			CalculateGreeks() : Calculates and sets all the Greeks of the option
			Calculate() : Calculates and sets the value and greeks of the option
	"""
	def __init__(self, K, style, otype, underlying, expiry, vol):
		"""
		Initialises the option class
			Parameters:
				K (float) : THe strike of the option
				style (string) : The style of the option (European/American/Asian)
				otype (string) : The type of the option (Call/Put)
				underlying (Underlying) : The underlying instrument for the option
				expiry (datetime) : The expiry for the option
				vol (float) : The volatility used to price the option
		"""
		self.K = K
		self.style = style
		self.otype = otype
		self.underlying = underlying
		self.expiry = expiry
		self.vol = vol
		self.CalculateTimeToExpiry()

	def CalculateTimeToExpiry(self):
		"""
		This method calculates the time until the option expires
		"""
		days_to_expiry = (self.expiry - self.underlying.t).days
		seconds_to_expiry = (self.expiry - self.underlying.t).seconds
		self.time_to_expiry = days_to_expiry/365.25 + seconds_to_expiry/(60*60*24*365.25)

	def CalculateGreeks(self):
		"""
		Calculates the Greeks for the option
		"""
		self.CalculateDelta()
		self.CalculateGamma()
		self.CalculateTheta()
		self.CalculateVega()
		self.CalculateRho()
	def Calculate(self):
		"""
		This method calculates and sets the theoretical value and greeks of the option
		"""
		self.CalculateTimeToExpiry()
		self.CalculateValue()
		self.CalculateGreeks()