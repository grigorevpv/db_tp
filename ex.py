import requests
import json

# POST with JSON
url = "http://localhost:5000/user/mentia/profile"
data = {
  "email": "a9@asdf.ru",
  "about": "about-about",
  "fullname": "PeterPeter"
}
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
# r = requests.post(url, data=json.dumps(data), headers=headers)

# data2 = {"slug": "sluggg", "limit": "100", "desc": "true"}
r = requests.get(url, headers=headers)

# Response, status etc
print(r.text)
print(r.status_code)