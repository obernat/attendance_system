#!/usr/bin/python3
import requests
import sys
import re

#Verifing given password, we dont want to store
#passwords in testing phase
if (len(sys.argv) == 1):
    print ("Please, specify your password")
    sys.exit()
password = sys.argv[1]

#Creating form sending to login
payload = {
'destination': '/auth',
'credential_0': 'xbernato',
'credential_1': password,
'credential_2': '86400',
'login': 'Prihlásenie'
}

#Creating session. Session object persist cookies, uses connection pooling
s = requests.Session()

#Creating post with given payload to log in
r = s.post("https://test.is.stuba.sk/auth/?lang=sk", data=payload)
print (s.cookies)

#Creating get to teacher page
#r = s.get("https://test.is.stuba.sk/auth/ucitel")
#print(r.text)

#Creating get to delegated teacher page
r = s.get("https://test.is.stuba.sk/auth/ucitel/?lang=sk;delegid=10139")
print (r.text)


#Parsing subjects url
match = "title=\"Sylabus predmetu\">(.*?)<.*?(index.pl\?predmet=[0-9]+)"
result = re.findall(match, r.text)
if result:
    print (result)
    #print (result.group(0))
    #print (result.group(1))
else:
    print ("no match found")


