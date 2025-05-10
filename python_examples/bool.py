def is_leap_year(year):
    return is_february(year) and (year % 4 == 0 and year % 100 != 0 or year % 400 == 0)

def is_february(year):
    return year == 2



