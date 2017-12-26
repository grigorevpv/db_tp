import requests
import json
import random
import string

# POST with JSON

# for i in range(0, 100):
# 	a = string.ascii_letters + string.digits
# 	nickname = ''.join([random.choice(a) for j in range(5)])
# 	url = "http://localhost:5000/api/user/" + nickname + "/create"
# 	data = {
# 	  "email": nickname+"@asdf.ru",
# 	  "about": "about-about",
# 	  "fullname": nickname + "Peter"
# 	}
# 	headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
# 	r = requests.post(url, data=json.dumps(data), headers=headers)
# 	print(r.text)
# 	print(r.status_code)
#
# 	forum = nickname + "forum"
#
# 	forum_url = "http://localhost:5000/api/forum/y9PW3ywuiQh882/create"
#
# 	forum_data = {
# 		"author": nickname,
# 		"created": "2018-06-05T14:26:03.644Z",
# 		"forum": "y9PW3ywuiQh882",
# 		"id": 1,
# 		"message": "Lucem non perdite eoque aqua aliud facies illi amor gloriatur vere. Eo mare id fidem mare venatio qua ea suam tu ad carnem.",
# 		"slug": "yY09ly9YITh8k"+forum,
# 		"title": "Suo terram aqua recti sinu iohannem beatos volatibus."
# 	}
# 	f = requests.post(forum_url, data=json.dumps(forum_data), headers=headers)
# 	print(f.text)
# 	print(f.status_code)

url = "http://localhost:8080/images"

# data2 = {"slug": "sluggg", "limit": "100", "desc": "true"}
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
r = requests.get(url, headers=headers)

# Response, status etc
print(r.text)
print(r.status_code)