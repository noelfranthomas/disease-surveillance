import requests
from pprint import pprint

url = "https://api.exa.ai/search"

payload = {
    "query": "Mpox data",
    "useAutoprompt": True,
    "type": "neural",
    "category": "research paper",
    "numResults": 5,
}
headers = {
    "x-api-key": "7bfd8b92-62e3-49ad-8d54-b90d1d125c4e",
    "Content-Type": "application/json"
}

response = requests.request("POST", url, json=payload, headers=headers)

pprint(response.text)
