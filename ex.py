import requests
import json

# POST with JSON
url = "http://localhost:5000/forum/N8l8uC_Lu2BsS2/create"
data = {
  "author": "e.vTzk85A3TV0jr1",
  "forum": "N8l8uC_Lu2BsS2",
  "message": "Meis custodis potui boni, incognitam. Eant hos mundis oderunt agro ut recolenda vicinior uspiam dura id eo, meo fit alioquin malorum plus. Ita tuae re poterunt qua. Timuisse o ait id quo erit falsitate vult. Vim id fiat sensu flenda solem. Eo sub gustatae terrae reponens aeger, sum meum paene, nos indagabit vim domi sua tuus viam. Castrorum ore an hi ipse autem continens sive oleat ei, diem re proximum, immo. Nutu plangendae hae ei. Fecisti deo nitidos abs animas fit cupientem recognoscitur contra en. Usum nam spes. Mirandum tale. Graeci ventre recorder redemit ob has noverunt animo peccare rogantem lineas per tuos tum cuiuscemodi erat. Flammam modis quo mirari dicere ceteris illa de fallit vi corrigebat prodest quo esto ab velut, lapsus amo. Iam itidem nec maerores pretium prodest ego sensus mundum lux vicinior agnoscerem cui intendimus. Tu displiceo me ab videbam, hae fluxum munere noe ergone et, cogens at volo metas me et. Praecidere intravi intime mei non ibi credidi cum aurem nolo.",
  "title": "Contristat rogo seu inde immaniter noverunt."
}
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
r = requests.post(url, data=json.dumps(data), headers=headers)

# data2 = {"slug": "sluggg", "limit": "100", "desc": "true"}
# r = requests.get(url, headers=headers)

# Response, status etc
print(r.text)
print(r.status_code)