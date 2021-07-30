import requests
import json
import logging
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
c_handler = logging.StreamHandler()
c_handler.setLevel(logging.DEBUG)
c_format = logging.Formatter("%(asctime)s | %(lineno)-4d | %(message)s")
c_handler.setFormatter(c_format)
logger.addHandler(c_handler)

url = "https://api.stackexchange.com/2.3"


method = "/search/advanced?"

filters = {
    "page" : 1,
    "pagesize" : 100,
    "order" : "desc",
    "sort" : "votes",
    "tagged" : "python",
    "site" : "stackoverflow"
}

"""
q - a free form text parameter, will match all question properties based on an 
    undocumented algorithm.

accepted - true to return only questions with accepted answers, false to return 
    only those without. Omit to elide constraint.

answers - the minimum number of answers returned questions must have.

body - text which must appear in returned questions' bodies.

closed - true to return only closed questions, false to return only open ones. 
    Omit to elide constraint.

migrated - true to return only questions migrated away from a site, false to 
    return only those not. Omit to elide constraint.

notice - true to return only questions with post notices, false to return only 
    those without. Omit to elide constraint.

nottagged - a semicolon delimited list of tags, none of which will be present 
    on returned questions.

tagged - a semicolon delimited list of tags, of which at least one will be 
    present on all returned questions.

title - text which must appear in returned questions' titles.

user - the id of the user who must own the questions returned.

url - a url which must be contained in a post, may include a wildcard.

views - the minimum number of views returned questions must have.

wiki - true to return only community wiki questions, false to return only 
    non-community wiki ones. Omit to elide constraint.
"""

title = str(input("What do you want to search StackOverflow for? : "))
logger.debug(f"{title = }")

filters["title"] = title

endpoint = []
for key, value in filters.items():
    end_point_part = f"{key}={value}"
    endpoint.append(end_point_part)
    logger.debug(f"{end_point_part = }")

api_filters = "&".join([point for point in endpoint])
test_endpoint = "".join((method, api_filters))

logger.debug(f"{api_filters = }")
logger.debug(f"{test_endpoint = }")

test_url = url+test_endpoint

response = requests.get(test_url)
logger.debug(f"{response = }")

results = json.loads(response.text)
data = results["items"]
logger.debug(f"{len(data)}")
logger.debug(f"Checking the first item in data: {data[0] = }")

links = []

for item in data:
    if item["is_answered"] == True and item["score"] >= 10:
        links.append(item["link"])

print(links[0] + "\n" + links[1])

file_path = os.path.dirname(__file__)
file_name = "search_results.txt"
file = "\\".join((file_path, file_name))

with open(file, "w") as f:
    for link in links:
        f.write(link + "\n")