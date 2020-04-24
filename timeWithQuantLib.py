import QuantLib as ql

# Construction -- session 1
date1 = ql.Date(11, 4, 2020)
date2 = ql.Date(43932)

print(date1)
print(date2)

# Basic Functions
date = ql.Date(11, 4, 2020)

dayOfMonth = date.dayOfMonth()
dayOfYear = date.dayOfYear()
month = date.month()
year = date.year()
serialNumber = date.serialNumber()
weekday = date.weekday()

print("Day of Month = {}".format(dayOfMonth))
print("Day of Year = {}".format(dayOfYear))
print("Month = {}".format(month))
print("Serial Number = {}".format(serialNumber))
print("Weekday = {}".format(weekday))

# Advanced Functions
todaysDate = date.todaysDate()
isLeap = date.isLeap(date.year())
isEndOfMonth = date.isEndOfMonth(date)
endOfMonth = date.endOfMonth(date)
nextWeekday = date.nextWeekday(date, 4)
nthWeekday = date.nthWeekday(3, 5, 7, 2020)

print("Today's Date = {}".format(todaysDate))
print("is Leap? = {}".format(isLeap))
print("is End of Month? = {}".format(isEndOfMonth))
print("End of Month = {}".format(endOfMonth))
print("Next Weekday = {}".format(nextWeekday))
print("Nth Weekday = {}".format(nthWeekday))


# Construction -- session 2
period1 = ql.Period(3, ql.Months)
period2 = ql.Period(ql.Semiannual)

# Functions
# date1 = ql.Date(11, 4, 2020)
date3 = ql.Date(31, 12, 2020)

three_weeks = ql.Period(3, ql.Weeks)
three_months = ql.Period(3,ql.Months)
three_years = ql.Period(3, ql.Years)

print("After 3 Weeks : {}".format(date1 + three_weeks))
print("After 3 Months : {}".format(date1 + three_months))
print("After 3 Years : {}".format(date1 + three_years))

print("Days between Date2 and Date1 = {}".format(date3 - date1))


# Construction -- session 3
us = ql.UnitedStates()
eu = ql.TARGET()
kr = ql.SouthKorea()
jp = ql.Japan()
cn = ql.China()

# Calendar Holiday
date4 = ql.Date(1, 1, 2020)
# date2 = ql.Date(31, 12, 2020)

kr_holidayList = kr.holidayList(kr, date4, date3)
print(kr_holidayList)

# Add Holiday & remove Holiday
kr.addHoliday(ql.Date(27, 1, 2020))  # add New Year Substitute Holiday
kr.addHoliday(ql.Date(15, 4, 2020))  # add Voting Day
kr.removeHoliday(ql.Date(6, 5, 2020))  # What is this day?
print(kr_holidayList)

# Business Days between
kr_businessDaysBetween = kr.businessDaysBetween(date4, date3)
print(kr_businessDaysBetween)

# Business Day & Holiday
kr_isBusinessDay = kr.isBusinessDay(date4)
kr_isHoliday = kr.isHoliday(date4)
print(kr_isBusinessDay)
print(kr_isHoliday)

# Advance
kr.advance(date4, ql.Period(6, ql.Months), ql.ModifiedFollowing, True)

# Joint Calendar
new_calendar = ql.JointCalendar(us, eu, kr)
print(new_calendar.holidayList(new_calendar, date4, date3))


# Construction -- session 4
act360 = ql.Actual360()  # Actual/360
act365 = ql.Actual365Fixed()  # Actual/365
actact = ql.ActualActual()  # Actual/Actual
thirty360 = ql.Thirty360()  # 30/360
b252 = ql.Business252()  # BusinessDay/252

# Day Count
date5 = ql.Date(12, 2, 2020)
date6 = ql.Date(14, 5, 2020)

print("Day Count by Actual/360 = {}".format(act360.dayCount(date5, date6)))
print("Day Count by Actual/365 = {}".format(act365.dayCount(date5, date6)))
print("Day Count by Actual/Actual = {}".format(actact.dayCount(date5, date6)))
print("Day Count by 30/360 = {}".format(thirty360.dayCount(date5, date6)))
print("Day Count by BusinessDay/252 = {}".format(b252.dayCount(date5, date6)))

# Year Fraction
print("Year Fraction by Actual/360 = {}".format(round(act360.yearFraction(date5, date6), 4)))
print("Year Fraction by Actual/365 = {}".format(round(act365.yearFraction(date5, date6), 4)))
print("Year Fraction by Actual/Actual = {}".format(round(actact.yearFraction(date5, date6), 4)))
print("Year Fraction by 30/360 = {}".format(round(thirty360.yearFraction(date5, date6), 4)))
print("Year Fraction by BusinessDay/252 = {}".format(round(b252.yearFraction(date5, date6), 4)))

# Components -- session 5
effectiveDate = ql.Date(13, 4, 2020)
maturityDate = ql.Date(15, 4, 2023)
tenor = ql.Period(3, ql.Months)
calendar = ql.SouthKorea()
convention = ql.ModifiedFollowing
rule = ql.DateGeneration.Backward
endOfMonth = False

schedule = ql.Schedule(effectiveDate, maturityDate, tenor, calendar, convention, convention, rule, endOfMonth)

ref_date = ql.Date(4, 10, 2021)

# Functions
print("Next Payment Date from {} : {}".format(ref_date, schedule.nextDate(ref_date)))
print("Previous Payment Date from {} : {}".format(ref_date, schedule.previousDate(ref_date)))

# Components -- session 6
quote = ql.SimpleQuote(2767.88)

# Functions
print(quote.value())

quote.setValue(2800.00)
print(quote.value())

# Componets -- session 7
rate = 0.0148
dc = ql.ActualActual()
comp = ql.Compounded
freq = ql.Annual

# Construction
ir = ql.InterestRate(rate, dc, comp, freq)

# Discount & Compound Factor
start_date = ql.Date(19, 4, 2020)
end_date = ql.Date(19, 4, 2021)

# print("Discount Factor between {} and {} = {}".format(start_date, end_date, round(ir.discountFactor(t), 4)))
# print("Compounding Factor between {} and {} = {}".format(start_date, end_date, round(ir.compoundFactor(t), 4)))

# Equivalent Rate
new_dc = ql.ActualActual()
new_comp = ql.Compounded
new_freq = ql.Quarterly
print("Equivalent Rate = {}".format(ir.equivalentRate(new_dc, new_comp, new_freq, start_date, end_date)))

# Implied Rate
comp_factor = 1.05
new_dc = ql.ActualActual()
new_comp = ql.Compounded
new_freq = ql.Annual
print("Implied Rate = {}".format(ir.impliedRate(comp_factor, new_dc, new_comp, new_freq, start_date, end_date)))
