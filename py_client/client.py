import requests

endpoint = "http://localhost:8000/api/" # http://127.0.0.1:8000/ 
get_response = requests.get(endpoint, params={"abc": 123}, json={"query": "Hello world"}) # HTTP Request
# print(get_response.text) # print raw text response
# print(get_response.status_code)

# HTTP Request -> HTML      
# REST API HTTP Request -> JSON
# JavaScript Object Notation ~ Python Dict
print(get_response.json())
# print(get_response.status_code)