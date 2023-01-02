import underlying
import option

import math
import numpy as np

class BinomialTreeOption(option.Option):
    """
    This is a class for an American option whose theoretical value is evaluated using the
    Cox-Ross-Rubinstein Model
        Attributes
            dt (float) : The time increment for steps in the binomial tree
            a (float) : The growth factor
            u (float) : The factor the underlying moves up by in each time step of the binomial tree
            d (float) : The factor the underlying moves down by in each time step of the binomial tree
            p (float) : The probability of the underlying moving up in the binomial tre
            time_steps (int) : The number of time steps to include in the binomial tree

            binomial_tree (list[ndarray]) : The binomial tree for the underlying contract
        Methods
            GenerateBinomialTree() : Generate the binomial tree for the underlying contract
            FinalValue() : Calcuates the value of the option at expiry
            EvaluateBinomialTree() : Calculates the value of the option at each node of the binomial tree

            CalculateValue() : Calculates the theoretical value of the option
    """
    def __init__(self, K, style, otype, underlying, expiry, vol):
        """
        Initialises the BinomialTreeOption class
            Parameters:
                K (float) : THe strike of the option
                style (string) : The style of the option (European/American/Asian)
                otype (string) : The type of the option (Call/Put)
                underlying (Underlying) : The underlying instrument for the option
                expiry (datetime) : The expiry for the option
                vol (float) : The volatility used to price the option

        """
        super().__init__(K, style, otype, underlying, expiry, vol)
        self.dt = 1/365.25
        self.a = math.exp((underlying.r - underlying.q)*self.dt)
        self.u = math.exp(vol*math.sqrt(self.dt))
        self.d = math.exp(-vol*math.sqrt(self.dt))
        self.p = (self.a - self.d)/(self.u - self.d)
        self.time_steps = int(self.time_to_expiry/self.dt)

    def GenerateBinomialTree(self):
        """
        Generates the binomial tree for the underlying contract
        """
        self.binomial_tree = [ np.array([self.underlying.S_0]) ]
        for i in range(0, self.time_steps):
            # Get the prices from the most recent time step
            prev_prices = self.binomial_tree[-1]
            # Calculate the next prices in the tree
            next_prices = np.concatenate((prev_prices*self.u, [prev_prices[-1]*self.d]))
            # Add the prices to the tree
            self.binomial_tree.append(next_prices)

    def FinalValue(self):
        """
        Calculates the value of the option at expiry
        """
        final_prices = self.binomial_tree[-1]
        self.binomial_tree[-1] = IntrinsicValue(final_prices, self.K, self.otype)

    def EvaluateBinomialTree(self):
        """
        Calculates the value of the option at each node of the binomial tree
        """
        self.FinalValue()
        # The discount factor used in calculations
        df = math.exp(-self.underlying.r*self.dt)
        for i in range(self.time_steps-1,-1,-1):
            # First calculate the theoretical value of the option as the present value of its expected future payoffs
            # The future payoffs of the option
            future_payoffs = self.binomial_tree[i+1]
            # The current value of the option based on the future payoffs
            current_tree_values = df*(self.p*future_payoffs[0:-1] + (1 - self.p)*future_payoffs[1:])

            # Calculate the intrinsic value of the option
            current_prices = self.binomial_tree[i]
            intrinsic_values = IntrinsicValue(current_prices, self.K, self.otype)
            current_values = np.where(current_tree_values > intrinsic_values, current_tree_values, intrinsic_values)

            self.binomial_tree[i] = current_values

    def CalculateValue(self):
        """
        Calculates the theoretical value of the option
        """
        self.GenerateBinomialTree()
        self.EvaluateBinomialTree()
        self.value = self.binomial_tree[0][0]

def IntrinsicValue(prices, K, otype):
    """
    Returns an array which contains the instrinsic value of an optiomn based on different
    prices for the underlying
        Parameters:
            prices (ndarray) : The prices of the underlying
            K (float) : The strike of the option
            otype (string) : The type of the option call/put
        Returns:
            instrinsic_values (ndarray) : The instrinsic values of the option
    """
    instrinsic_values = None
    if otype == "Call":
        instrinsic_values = np.maximum(prices - K, 0)
    elif otype == "Put":
        instrinsic_values = np.maximum(K - prices, 0)
    return instrinsic_values


import datetime as dt
underlying = underlying.Underlying("BTC","Futures ",100, dt.datetime.now(), 0.04, 0)
expiry = dt.datetime(2022,11,1)
option = BinomialTreeOption(100,"American","Call",underlying,expiry,0.5)
option.CalculateValue()
print(option.value)

