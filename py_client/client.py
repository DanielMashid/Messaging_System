import requests

endpoint = "http://localhost:8000"
get_response = requests.get(endpoint, json={"query": "Hello world"}) # HTTP Request
print(get_response.text) # print raw text response
print(get_response.status_code)