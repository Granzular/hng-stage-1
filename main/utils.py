import requests

GENDERIZE_API_URL = "https://api.genderize.io"
AGIFY_API_URL = "https://api.agify.io"
NATIONALIZE_API_URL = "https://api.nationalize.io"


def test_api(data:dict):
    genderize_res = requests.get(GENDERIZE_API_URL,params=data)
    agify_res = requests.get(AGIFY_API_URL,params=data)
    nationalize_res = requests.get(NATIONALIZE_API_URL,params=data)
    genderize_data = genderize_res.json()
    agify_data = agify_res.json()
    nationalize_data = nationalize_res.json()
    return [genderize_data,agify_data,nationalize_data]


def process_request(data:dict):
    ...
