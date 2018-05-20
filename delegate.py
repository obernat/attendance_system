#!/usr/bin/env python3

import re
import sys
import requests


#Verifing given password, we dont want to store
#passwords in testing phase
if (len(sys.argv) == 1):
    print ("Please, specify your password")
    sys.exit()

password=sys.argv[1]
#Creating form sending to login
payload = {
"lang" : "sk",
'destination': '/auth',
'credential_0': 'xbernato',
'credential_1': password,
'credential_2': '86400',
'login': 'Prihlásenie'
}

#Creating session. Session object persist cookies, uses connection pooling
s = requests.Session()

#Creating post with given payload to log in
r = s.post("https://is.stuba.sk/auth/?lang=sk", data=payload)


def get_delegates(s):
    #function returns list of possible delegators

    if s is None:
        return -4, None  # session not created

    try:
        r = s.get(
            "https://is.stuba.sk/auth/system/zmena_identity.pl?_m=287;lang=sk",
            timeout=10)  # what is _m?
    except requests.exceptions.RequestException as e:
        print(e)  # Logger
        return -3, None  # timeout, bad url

    if r.status_code != 200:
        return -2, None  # error getting the page, maybe page down/no internet access

    match = "<a href=\"/auth/lide/clovek.pl\?id=([0-9]+).*?>(.*?)</a>"
    result = re.findall(match, r.text, re.DOTALL)

    if result:
        return 1, result
    else:
        return -1, None  # parsing error, no delegators



print (get_delegates(s))
