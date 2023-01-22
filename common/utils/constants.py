from common.utils.searchCriteria import getTodaysDate, getFormattedDateForNthDay

Empty_string = ""
SOURCE = "source"
DESTINATION = "destination"
DEPARTURE_DATE = "departure_date"

start_sequence = "\nMakeMyTrip: "
restart_sequence = "\n\nSaurabh: "

SESSION1_CHAT_LOG_VALUE = f"You are talking to MakeMyTrip. We offer flights services. And our website link is https://www.makemytrip.com/" \
                   f"In order to search for a flight we need source city, destination city and departure date. " \
                   f"Lets say today's date is {getTodaysDate()}\nPerson: "
SESSION1_CHAT_LOG_KEY = "chat_log1"

SESSION2_CHAT_LOG_VALUE = f"""{restart_sequence}Book a flight to Goa{start_sequence}{{"{SOURCE}":"", "{DESTINATION}":"GOI", "{DEPARTURE_DATE}":""}}{restart_sequence}my source is Delhi and departure date is tomorrow{start_sequence}{{"{SOURCE}":"DEL", "{DESTINATION}":"GOI", "{DEPARTURE_DATE}":"{getFormattedDateForNthDay(1)}"}}{restart_sequence}flight to BLR for tomorrow{start_sequence}{{"{SOURCE}":"", "{DESTINATION}":"BLR", "{DEPARTURE_DATE}":"{getFormattedDateForNthDay(1)}"}}{restart_sequence}source is DXB{start_sequence}{{"{SOURCE}":"DXB", "{DESTINATION}":"GOI", "{DEPARTURE_DATE}":"{getFormattedDateForNthDay(1)}"}}{restart_sequence}i want to go to London next week{start_sequence}{{"{SOURCE}":"", "{DESTINATION}":"LON", "{DEPARTURE_DATE}":"{getFormattedDateForNthDay(7)}"}}{restart_sequence}from delhi{start_sequence}{{"{SOURCE}":"DEL", "{DESTINATION}":"LON", "{DEPARTURE_DATE}":"{getFormattedDateForNthDay(7)}"}}"""
SESSION2_CHAT_LOG_KEY = "chat_log2"

COLUMN_AIRLINE = "airline"
COLUMN_DEP_TIME = "dep_time"
COLUMN_ARRIVAL_TIME = "arrival_time"
COLUMN_TOTAL_FARE = "total_fare"

SEARCH_PARAMETER = Empty_string
