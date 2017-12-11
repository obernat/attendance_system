#!/usr/bin/python3
import requests
import sys
import re

def try_login(s, name, password, timeout=86400):

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
    r = s.post("https://test.is.stuba.sk/auth/?lang=sk", data=payload)

    if r.status_code != 200:
        return -3 #error posting on page, maybe page down/no internet access

    #Parsing div log
    match = "<div id=\"log\">.*?</div>"
    result = re.search(match, r.text, re.DOTALL)
    if result:
        result = str(result.group())
        if (result.find("Prihlásený") != -1 or result.find("Logged in") != -1):
            return 1
        else:
            return -1 #login error
    else:
        return -2 #parsing error

def get_subjects(s):

    result = []

    if s == None:
        return -4, result #session not created

    #Creating get to teacher page, cookies send automatically
    r = s.get("https://test.is.stuba.sk/auth/ucitel/?_m=195;lang=sk") #what is _m?

    #Creating get to delegated teacher page
    #r = s.get("https://test.is.stuba.sk/auth/ucitel/?lang=sk;delegid=10139")

    if r.status_code != 200:
        return -3, result #error getting the page, maybe page down/no internet access

    #Parsing subjects url
    match = "title=\"Sylabus predmetu\">(.*?)<.*?index.pl(\?predmet=[0-9]+)"
    result = re.findall(match, r.text, re.DOTALL)
    if result:
        return 1, result
    else:
        return -1, result #parsing error, no subjects


def get_groups_ids(s, subject_id):

    if s == None:
        return -4 #session not created

    url = "https://test.is.stuba.sk/auth/nucitel/dochazka.pl?predmet=" + \
            str(subject_id) + ";lang=sk"

    r = s.get(url)
    if r.status_code != 200:
        return -3 #error getting the page, maybe page down/no internet access

    match = "<select name=\"vybrane_cviceni\".*?</select>"
    result_select = re.search(match, r.text, re.DOTALL)
    if not result_select:
        return -1 #parsing error, no groups
    else:
        result_select = result_select.group()
        match = "<option value=\"([0-9]+)\""
        result = re.findall(match, result_select, re.DOTALL)
        if result:
            return 1, result
        else:
            return -1 #parsing error, no groups

