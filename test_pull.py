import requests
import urllib.request as req

api_key = "9e42f20edf8c6b2fc46167c7dc8dc42e"
photo_id = "50271413962"
auth_token = "72157674425939158-f6ad7c41a8abe02c"
api_sig = "c3ca33f9e1c22ba5c4843dc9f52ec08c"

url = "https://api.flickr.com/services/rest/?method=flickr.photos.getSizes&api_key=" + \
api_key + "&photo_id=" + photo_id + "&format=json&nojsoncallback=1"
'''      + \
"&auth_token=" + auth_token + "&api_sig=" + api_sig
'''

params=''

response = requests.get(url, params=params)

data = response.json()

print('setting sizes')
sizes = data['sizes']


photo_list = sizes['size']

for item in photo_list:
    if item['label'] == 'Large':
        print('getting photo', item['source'])
        req.urlretrieve(item['source'], 'photo.jpg')

