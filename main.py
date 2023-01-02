import underlying
import option

import datetime as dt

name = "BTC"
S_0 = 20000
r = 20000
underlying_object = underlying.Underlying(name, S_0, r)

strike = 20000
style = "European"
option_type = "Call"
evaluation = dt.datetime.now()
expiration = dt.datetime(2023,12,31)
vol = 0.3

option_object = option.Option(strike, style, option_type, underlying_object, evaluation, expiration, vol)