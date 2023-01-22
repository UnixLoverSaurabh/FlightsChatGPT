from datetime import date
from datetime import timedelta
from common.utils import constants


# https://www.makemytrip.com/flight/search?itinerary=AUH-CNN-20/01/2023&tripType=O&paxType=A-1_C-0_I-0&intl=true&cabinClass=E&ccde=AE&lang=eng


def getTodaysDate():
    today = date.today().strftime("%d/%m/%Y")
    return today


def getFormattedDateForNthDay(days):
    begin_date_string = date.today()
    end_date = begin_date_string + timedelta(days=days)
    return end_date.strftime("%d-%m-%Y")


def isStringEmpty(value: str) -> bool:
    if value == constants.Empty_string or value is None:
        return True
    return False


def isSearchCriteriaSatisfied(response: dict) -> bool:
    source = response.get(constants.SOURCE)
    destination = response.get(constants.DESTINATION)
    departure_date = response.get(constants.DEPARTURE_DATE)

    searchParameter = f'{source}-{destination}-{departure_date}'
    if not isStringEmpty(source) and not isStringEmpty(destination) and not isStringEmpty(departure_date) and searchParameter != constants.SEARCH_PARAMETER:
        constants.SEARCH_PARAMETER = searchParameter
        return True
    return False
