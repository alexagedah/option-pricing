import underlying
import option

import math
from scipy import stats

class BSMOption(option.Option):
	"""
	This is a class for a European option which is evaluated using the Black-Scholes Merton
	pricing model
		Attributes
			d_1 (float) : The d_1 term in the BSM formula for the value of an option
			d_2 (float) : The d_2 term in the BSM formula for the value of an option
		Methods
			CalculateD12() : Calculates the d_1 and d_2 terms in the BSM formula for the value of an option
			CalculateValue() : Calculates the theoretical value of the option
			CalculateDelta() : Calculate the delta of the option
			CalculateGamma() : Calculates the gamma of the option
			CalculateTheta() : Calculates the theta of the option
			CalculateVega() : Calculates the vega of the option
			CalculateRho() : Calculates the rho of the option
	"""
	def CalculateD12(self):
		"""
		This method calculates and sets the d_1 and d_2 terms
		"""
		self.d_1 = (math.log(self.underlying.S_0/self.K) + (self.underlying.b + (self.vol**2)/2)*self.time_to_expiry)/(self.vol*math.sqrt(self.time_to_expiry))
		self.d_2 = (math.log(self.underlying.S_0/self.K) + (self.underlying.b - (self.vol**2)/2)*self.time_to_expiry)/(self.vol*math.sqrt(self.time_to_expiry))
	def CalculateValue(self):
		"""
		This method calculates and sets the theoretical value of the option
		"""
		S_0 = self.underlying.S_0
		K = self.K
		b = self.underlying.b
		r = self.underlying.r
		t = self.time_to_expiry
		self.CalculateD12()
		d_1 = self.d_1
		d_2 = self.d_2
		if self.style == "European":
			if self.otype == "Call":
				self.value = S_0*math.exp((b - r)*t)*stats.norm.cdf(d_1, 0, 1) - K*math.exp(-r*t)*stats.norm.cdf(d_2, 0 ,1)
			else:
				self.value = K*math.exp(-r*t)*stats.norm.cdf(-d_2) - S_0*math.exp(-r*t)*stats.norm.cdf(-d_1)
	def CalculateDelta(self):
		"""
		This method calculates and sets the delta of the option
		"""
		S_0 = self.underlying.S_0
		b = self.underlying.b
		r = self.underlying.r
		t = self.time_to_expiry
		d_1 = self.d_1
		d_2 = self.d_2
		if self.style == "European":
			if self.otype == "Call":
				self.delta = math.exp((b - r)*t)*stats.norm.cdf(d_1, 0, 1)
			else:
				self.delta = -math.exp((b - r)*t)*stats.norm.cdf(-d_1, 0, 1)
	def CalculateGamma(self):
		"""
		This method calculates and sets the gamma and relative gamma of the option
		"""
		if self.style == "European":
			self.gamma = math.exp((b - r)*t)*stats.norm.pdf(self.d_1, 0, 1)/(self.underlying.S_0*self.vol*math.sqrt(self.time_to_expiry))
		self.relative_gamma = self.gamma
	def CalculateTheta(self):
		"""
		This method calculates and sets the theta of the option
		"""
		if self.style == "European":
			S_0 = self.underlying.S_0
			b = self.underlying.b
			r = self.underlying.r
			t = self.time_to_expiry
			term1 = -(S_0 * math.exp((b - r)*t)*stats.norm.pdf(self.d_1, 0, 1) * self.vol )/(2*math.sqrt(t))
			term2 = -r*self.K*math.exp(-r*t)
			if self.otype == "Call":
				self.theta = term1 - term2*stats.norm.cdf(self.d_2, 0, 1) - S_0*(b - r)*math.exp((b - r)*t)*stats.norm.cdf(self.d_1, 0, 1)
			else:
				self.theta = term1 + term2*stats.norm.cdf(-self.d_2, 0, 1) + S_0*(b - r)*math.exp((b - r)*t)*stats.norm.cdf(-self.d_1, 0, 1)
	def CalculateVega(self):
		"""
		This method calculates and sets the vega of the option
		"""
		if self.style == "European":
			S_0 = self.underlying.S_0
			self.vega = S_0*math.sqrt(self.time_to_expiry)*stats.norm.pdf(self.d_1, 0, 1)*math.exp((b - r)*t)
	def CalculateRho(self):
		"""
		This method calculates and sets the rho of the option
		"""
		if self.style == "European":
			r = self.underlying.r
			if self.otype == "Call":
				self.rho = self.K*self.time_to_expiry*math.exp(-r*self.time_to_expiry)*stats.norm.cdf(self.d_2)
			elif self.otype == "Put":
				self.rho = -self.K*self.time_to_expiry*math.exp(-r*self.time_to_expiry)*stats.norm.cdf(-self.d_2)

import datetime as dt
underlying = underlying.Underlying("BTC","Futures",100, dt.datetime.now(), 0.04, 0)
expiry = dt.datetime(2022,11,1)
option = BSMOption(100,"European","Call",underlying,expiry,0.5)
option.CalculateValue()
print(option.value)

