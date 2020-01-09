import QuantLib as ql
from FICCwithQuantLib import GET_DATE, GET_QUOTE, TREASURY_CURVE

ref_date = GET_DATE()
quote = GET_QUOTE(ref_date)
curve = TREASURY_CURVE(ref_date, quote)

# Convert into Engine
spotCurveHandle = ql.YieldTermStructureHandle(curve)
bondEngine = ql.DiscountingBondEngine(spotCurveHandle)

# Treasury Bond Specification
issueDate = ql.Date(15, 11, 2019)
maturityDate = ql.Date(15, 11, 2029)
tenor = ql.Period(ql.Semiannual)
calendar = ql.UnitedStates()
convention = ql.ModifiedFollowing
dateGeneration = ql.DateGeneration.Backward
monthEnd = False
schedule = ql.Schedule(issueDate,
                       maturityDate,
                       tenor,
                       calendar,
                       convention,
                       convention,
                       dateGeneration,
                       monthEnd)
dayCount = ql.ActualActual()
couponRate = [0.0175]
settlementDays = 1
faceValue = 100

fixedRateBond = ql.FixedRateBond(settlementDays, faceValue, schedule, couponRate, dayCount)

# Conduct Pricing
fixedRateBond.setPricingEngine(bondEngine)

# Result
print("Bond Price = {}".format(round(fixedRateBond.NPV(), 4)))
for c in fixedRateBond.cashflows():
    print('%20s %12f' % (c.date(), c.amount()))
