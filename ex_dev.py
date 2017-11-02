import requests
import json
import random
import string

# POST with JSON
for i in range(0, 10000):
	a = string.ascii_letters + string.digits
	nickname = ''.join([random.choice(a) for j in range(5)])
	url = "http://localhost:5000/api/user/" + nickname + "/create"
	data = {
	  "email": nickname+"@asdf.ru",
	  "about": "about-about",
	  "fullname": nickname + "Peter"
	}
	headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
	r = requests.post(url, data=json.dumps(data), headers=headers)
	print(r.text)
	print(r.status_code)

# data2 = {"slug": "sluggg", "limit": "100", "desc": "true"}
# r = requests.get(url, headers=headers)

# Response, status etc
# print(r.text)
# print(r.status_code)