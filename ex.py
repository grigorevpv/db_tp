import requests
import json

# POST with JSON
url = "http://localhost:5000/forum/u5bpe5G3vm_KS2/create"
data = {
  "author": "quaerens.4NANDiO319yP7u",
  "created": "2016-10-31T15:16:19.981+03:00",
  "forum": "u5bpe5G3vm_KS2",
  "message": "Eo. Audiam nollem porro palpa, tremorem. Eos valent necessitas da oculo ipsi te rem suavi est moderatum tu at intime. Potuero dico si opertis donec te se da ingenti eram lingua sic impium usui scio desperare, maior. Se recognoscitur fateor est dei viribus, vim aliam innecto didicerim piam vocantur. Latine si factis ob decus religione euge ad pax mihi rem te genera qui prosperitatis. Vel superbiam erigo. Ea oderunt alas lux spe, hic interfui ideo quorum nota. Excitentur quo sed nostrae ea. Potestates sub. Eloquiorum erat prae laniato caro malint e iam se, qua tui si noe. Diu curo carnem id en praeterierit eant, id, tui in esse sapores vindicavit fine malis spem nutantibus suavi. Una imaginibus vel minus vasis dubia ac aut ea sub tale mea id nares e. Tuus oblitum os metum audire posco sinus concessisti salvus dei tuae ipsis, ioseph si consulunt me tu consortium vestra. Habeatur malorum. Eo misericordias de alienam pax modi enervandam minusve ex eas, fieret. Dei. O det dum fabricatae ut se possideri o fuisse, suo auribus cupidatatium re.",
  "title": "Fluctuo antiquis ea fundum quotiens perit."
}
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
r = requests.post(url, data=json.dumps(data), headers=headers)

# data2 = {"slug": "sluggg", "limit": "100", "desc": "true"}
# r = requests.get(url, headers=headers)

# Response, status etc
print(r.text)
print(r.status_code)