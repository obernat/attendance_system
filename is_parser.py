#!/usr/bin/python3
import requests
import sys
import re

def try_login(s, name, password, timeout=86400):
    #TODO tu vzdy ratame s tym ze user je online, treba nechat aj moznost ze user bude offline
    #vtedy bude treba riesit aj vypisy... toto este treba cele premysliet :(
    if s == None:
        return -4 #session not created

    #Creating form sending to login
    payload = {
    'lang' : 'sk',
    'destination': '/auth',
    'credential_0': name,
    'credential_1': password,
    'credential_2': '86400',
    'login': 'Prihlásenie'
    }

    #Creating session. Session object persist cookies, uses connection pooling
    #s = requests.Session()

    #Creating post with given payload to log in, cookies saved for future
    try:
    	r = s.post("https://test.is.stuba.sk/auth/?lang=sk", data=payload, timeout=10)
    except requests.exceptions.RequestException as e:
        print(e) #Logger
        return -4 #timeout, bad url

    #scheme dependent
    #Parsing div log
    #match = "<div id=\"log\">.*?</div>"
    #result = re.search(match, r.text, re.DOTALL)
    #if not result:
    #    match = "<div id=\"prihlasen\">.*?</div>"
    #    result = re.search(match, r.text, re.DOTALL)
    #if result:
    #    result = str(result.group())
    #    if (result.find("Prihlásený") != -1 or result.find("Logged in") != -1):
    #        return 1
    #    else:
    #        return -1 #login error
    #else:
    #    return -2 #parsing error


    if (r.text.find("Nesprávne prihlasovacie meno alebo heslo.") != -1 or
            r.text.find("Prihlasovací formulár nebol korektne vyplnený.") != -1):
        return -1 #login error
    else:
        return 1



def get_subjects(s):

    if s == None:
        return -4, None #session not created

    #Creating get to teacher page, cookies send automatically
    try:
        r = s.get("https://test.is.stuba.sk/auth/ucitel/?_m=195;lang=sk", timeout=10) #what is _m?
    except requests.exceptions.RequestException as e:
        print(e) #Logger
        return -3, None #timeout, bad url

    #Creating get to delegated teacher page
    #r = s.get("https://test.is.stuba.sk/auth/ucitel/?lang=sk;delegid=10139")

    if r.status_code != 200:
        return -2, None #error getting the page, maybe page down/no internet access

    #Parsing subjects url
    match = "title=\"Sylabus predmetu\">(.*?)<.*?index.pl(\?predmet=[0-9]+)"
    result = re.findall(match, r.text, re.DOTALL)
    if result:
        return 1, result
    else:
        return -1, None #parsing error, no subjects


def get_groups_ids(s, subject_id):

    if s == None:
        return -5, None #session not created

    url = "https://test.is.stuba.sk/auth/nucitel/dochazka.pl?predmet=" + \
            str(subject_id) + ";lang=sk"

    try:
        r = s.get(url, timeout=10)
    except requests.exceptions.RequestException as e:
        print(e) #Logger
        return -4, None #timeout, bad url

    if r.status_code != 200:
        return -3, None #error getting the page, maybe page down/no internet access

    match = "<select name=\"vybrane_cviceni\".*?</select>"
    result_select = re.search(match, r.text, re.DOTALL)
    if not result_select:
        return -1, None #parsing error, no groups
    else:
        result_select = result_select.group()
        match = "<option value=\"([0-9]+)\""
        result = re.findall(match, result_select, re.DOTALL)
        if result:
            print (result)
            return 1, result
        else:
            return -1, None #parsing error, no groups


