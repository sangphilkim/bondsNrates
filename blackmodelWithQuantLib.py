import QuantLib as ql

valuationDate = ql.Date(2, 3, 2020)
ql.Settings.instance().evaluationDate = valuationDate
calendar = ql.SouthKorea()
dayCount = ql.ActualActual()

# Simple Quote Objects
futures_qt = ql.SimpleQuote(270.90) # KOSPI 200 Futures Mar20
riskfreerate_qt = ql.SimpleQuote(0.01) # Risk-Free Rate
volatility_qt = ql.SimpleQuote(0.40) # Volatility

# Quote Handle Objects
f_qhd = ql.QuoteHandle(futures_qt)
r_qhd = ql.QuoteHandle(riskfreerate_qt)
v_qhd = ql.QuoteHandle(volatility_qt)

# Term-Structure Objects
r_ts = ql.FlatForward(valuationDate, r_qhd, dayCount)
v_ts = ql.BlackConstantVol(valuationDate, calendar, v_qhd, dayCount)

# Term-Sturcture Handle Objects
r_thd = ql.YieldTermStructureHandle(r_ts)
v_thd = ql.BlackVolTermStructureHandle(v_ts)

# Process & Engine
process = ql.BlackProcess(f_qhd, r_thd, v_thd)
engine = ql.AnalyticEuropeanEngine(process)

# Option Objects
option_type = ql.Option.Call
strikePrice = 267.50
expiryDate = ql.Date(12, 3, 2020)

exercise = ql.EuropeanExercise(expiryDate)
payoff = ql.PlainVanillaPayoff(option_type, strikePrice)
option = ql.VanillaOption(payoff, exercise)

# Pricing
option.setPricingEngine(engine)

# Price & Greeks Results
print('== Price & Greeks Results ==')
print('Option Premium = ', round(option.NPV(), 2)) # option premium
print('Option Delta = ', round(option.delta(), 4)) # delta
print('Option Gamma = ', round(option.gamma(), 4)) # gamma
print('Option Theta = ', round(option.thetaPerDay(), 4)) #theta
print('Option Vega = ', round(option.vega() / 100, 4)) # vega
print('Option Rho = ', round(option.rho() / 100, 4)) # rho

# Implied Volatility
mkt_price = 8.95
implied_volatiltity = option.impliedVolatility(mkt_price, process)
volatility_qt.setValue(implied_volatiltity)
print('== Implied Volatiltity ==')
print('Option Premium = ', round(option.NPV(), 2)) # option premium
print('Option Delta = ', round(option.delta(), 4)) # delta
print('Option Gamma = ', round(option.gamma(), 4)) # gamma
print('Option Theta = ', round(option.thetaPerDay(), 4)) #theta
print('Option Vega = ', round(option.vega() / 100, 4)) # vega
print('Option Rho = ', round(option.rho() / 100, 4)) # rho