'''
input: (patientonsetage, patientonsetageunit) - both strings
output: integer containing rounded age in years
'''
def age_years(age, unit_code):
    a = float(age)
    c = int(unit_code)
    ans = 0.0
    if c == 800:
        ans = a * 10.0
    else if c == 801:
        ans = a
    else if c == 802:
        ans = a / 12.0
    else if c == 803:
        ans = a / 52.0
    else if c == 804:
        ans = a / 365.242
    else if c == 805:
        ans = a / 8765.81
    return int(round(ans))
