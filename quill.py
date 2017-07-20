from config import *

import requests
import json

HEADERS = {'x-access-token': ACCESS_TOKEN}

def get_wl():
	r = requests.get(ENDPOINT, headers=HEADERS)
	j = json.loads(r.text)
	return j

def post_wl(lst):
	j = {'emails': lst}
	r = requests.put(ENDPOINT, headers=HEADERS, json=j)

	print r.text

	if r.status_code == 200:
		return True
	else:
		return False


if __name__ == "__main__":
	print post_wl(get_wl() + ['shreyask@mit.edu'])