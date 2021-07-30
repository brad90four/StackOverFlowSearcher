# author brad90four
# creation date 07/28/2021
# written from an idea posted on Python Discord

import os
import json
import logging
import requests
from requests_oauthlib import OAuth2Session

# set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
c_handler = logging.StreamHandler()
c_handler.setLevel(logging.INFO)
c_format = logging.Formatter("%(asctime)s | %(lineno)-4d | %(message)s")
c_handler.setFormatter(c_format)
logger.addHandler(c_handler)

# get user data from json file
json_file = os.path.dirname(__file__) + "\\key.json"
logger.debug(f"{json_file = }")

with open(json_file) as f:
    user_data = json.load(f)

# define data used in OAuth2 Implicit flow
auth_data = {
    "key" : user_data["key"],
    "client_id" : user_data["client_id"],
    "client_secret" : user_data["client_secret"],
    "redirect_uri" : user_data["redirect_uri"]
}

# if user does not have access key
def first_auth():
    auth_url = "https://stackoverflow.com/oauth/dialog"
    oauth = OAuth2Session(
        client_id=auth_data["client_id"],
        redirect_uri=auth_data["redirect_uri"]
        )
    authorization, state = oauth.authorization_url(auth_url)
    print(authorization)
    authorization_response = input("\n" + "Enter the full callback URL: " +"\n")
    access_token = authorization_response[40:64]
    return access_token

try:
    access_token = user_data["access_token"]
except:
    access_token = first_auth()

# API url creation
base_url = "https://api.stackexchange.com/2.3"

method = "/search/advanced?"

params = {
    "key" : user_data["key"],
    "client_id" : user_data["client_id"],
    "access_token" : access_token,
    "page": 1,
    "pagesize": 100,
    "order" : "desc",
    "sort" : "votes",
    "tagged" : "python",
    "site" : "stackoverflow"
}

title = str(input("What do you want to search StackOverflow for? : "))
logger.debug(f"{title = }")

params["title"] = title
params["q"] = title

endpoint = []
for key, value in params.items():
    end_point_part = f"{key}={value}"
    logger.debug(f"{end_point_part = }")
    endpoint.append(end_point_part)


api_filters = "&".join([point for point in endpoint])
logger.debug(f"{api_filters = }")

api_endpoint = "".join((method, api_filters))
logger.debug(f"{api_endpoint = }")

api_url = f"{base_url}{api_endpoint}"
logger.debug(f"{api_url = }")

# main call to the API
response = requests.get(api_url)
logger.debug(f"{response = }")

results = json.loads(response.text)
data = results["items"]
logger.debug(f"{len(data)}")
logger.debug(f"Checking the first item in data: {data[0] = }")

quota = results["quota_remaining"]

# create list of links
links = []
for item in data:
    if item["is_answered"] == True and item["score"] >= 10:
        links.append(item["link"])

# display first two links
logger.info(links[0] + "\n" + links[1])
# remaining API calls
logger.info(f"{quota = }")

# create a txt file of links from API call
file_path = os.path.dirname(__file__)
file_name = "search_results.txt"
file = "\\".join((file_path, file_name))

with open(file, "w") as f:
    for link in links:
        f.write(link + "\n")