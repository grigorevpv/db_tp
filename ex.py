import requests
import json

# POST with JSON
url = "http://localhost:5000/user/lingua.8Zw8IZI8bz0p7d/profile"
data = {
  "about": "Ingentibus ipsarum isti fallax. Audiant vocant his. Videns dum qua ne. Ita malim ait. Adversitas tu iudicet dulce. Vera apud putare. Et tuo. Meae resistere agro falsitate periculum advertimus in.",
  "email": "splendeat.Rl8cZS380zYrR@sialis.org",
  "fullname": "Jayden Jones"
}
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
r = requests.post(url, data=json.dumps(data), headers=headers)

# data2 = {"slug": "sluggg", "limit": "100", "desc": "true"}
# r = requests.get(url, headers=headers)

# Response, status etc
print(r.text)
print(r.status_code)