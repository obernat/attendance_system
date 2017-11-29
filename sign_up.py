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

#Creating get to teacher page
r = s.get("https://test.is.stuba.sk/auth/ucitel/?_m=195;lang=sk") #what is _m?
#print(r.text)


#Parsing subjects url
match = "title=\"Sylabus predmetu\">(.*?)<.*?index.pl(\?predmet=[0-9]+)"
result = re.findall(match, r.text)
if result:
    print (result)
    #print (result.group(0))
    #print (result.group(1))
else:
    print ("no match found")

url = "https://test.is.stuba.sk/auth/nucitel/dochazka.pl"
final = url + result[0][1] + ";lang=sk"
print (final)
r = s.get(final)
match = "<select name=\"vybrane_cviceni\".*?</select>"
result = re.search(match, r.text, re.DOTALL)
print (result.group())
b = result.group()

match = "<option value=\"([0-9]+)\">"
result = re.findall(match, b, re.DOTALL)
print (result)

