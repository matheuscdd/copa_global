from exceptions import InvalidYearCupError, NegativeTitlesError, ImpossibleTitlesError
from constrains import TITLES, FIRST_CUP

def data_processing(team: dict):
    year, titles = int(team[FIRST_CUP][:4]), team[TITLES]
    from datetime import datetime
    valid_years = [y for y in range(1930, datetime.now().year, 4)]
    if year < 1930 or year not in valid_years:
        raise InvalidYearCupError('there was no world cup this year')
    elif titles < 0:
        raise NegativeTitlesError('titles cannot be negative')
    years_after_first_cup = len(valid_years) - (valid_years.index(year)+1)
    if years_after_first_cup < titles:
        raise ImpossibleTitlesError('impossible to have more titles than disputed cups')

