#!/usr/bin/python3
import requests
import sys

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
'login': 'login'
}

#Creating session. Session object persist cookies, uses connection pooling
s = requests.Session()

#Fetching the form with the Set-Cookie header
r = s.get("https://is.stuba.sk/system/login.pl")

#Creating post with given payload to log in
r = s.post("https://is.stuba.sk/system/login.pl", data=payload)
#print (s.cookies)

#Creating get to teacher page
r = s.get("https://is.stuba.sk/auth/ucitel")


print(r.text)
