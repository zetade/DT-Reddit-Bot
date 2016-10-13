import requests
import pprint
r = requests.get('https://s3.amazonaws.com/dolartoday/data.json')
data=r.json()
pprint.pprint (data['USD']['dolartoday'])
