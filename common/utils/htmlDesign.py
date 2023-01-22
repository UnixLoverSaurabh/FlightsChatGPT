import re

from common.utils import searchCriteria


def convertStringToBulleted(value: str) -> str:
    items = re.split('\n', value)

    html_list = items[0] + "<ul>"
    for item in items[1:]:
        if searchCriteria.isStringEmpty(item):
            continue
        html_list += f"<li>{item}</li>"
    html_list += "</ul>"
    return html_list