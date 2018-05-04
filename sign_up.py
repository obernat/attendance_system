#!/usr/bin/python3
import requests
import sys
import re

#Verifing given password, we dont want to store
#passwords in testing phase
if (len(sys.argv) == 1):
    print ("Please, specify your password")
    sys.exit()

#mY
if sys.argv[1] == "mY":
    with open("/home/ondrej/mY.txt") as f:
        password = f.read().strip()
#if not mY
else:
    password = sys.argv[1]
"""
#Creating form sending to login
payload = {
"lang" : "sk",
'destination': '/auth',
#'credential_0': 'xbernato',
'credential_0': 'xjokay',
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
#_--------------------------------------------------



import sqlite3
import http.cookiejar as cookielib

def get_cookies(cj, ff_cookies):
    con = sqlite3.connect(ff_cookies)
    cur = con.cursor()
    cur.execute("SELECT host, path, isSecure, expiry, name, value FROM moz_cookies")
    for item in cur.fetchall():
        if item[0].find("stuba.sk") == -1:
            continue
        c = cookielib.Cookie(0, item[4], item[5],
            None, False,
            item[0], item[0].startswith('.'), item[0].startswith('.'),
            item[1], False,
            item[2],
            item[3], item[3]=="",
            None, None, {})
        print (c)
        cj.set_cookie(c)


cj = cookielib.CookieJar()
ff_cookies = sys.argv[2]
get_cookies(cj, ff_cookies)
print(cj)
s = requests.Session()
s.cookies = cj
print(s.cookies)
sys.exit()
r = s.get("https://test.is.stuba.sk/auth/ucitel/?_m=195;lang=sk") #what is _m?
print (r.text)
"""


url = 'https://test.is.stuba.sk/auth/ucitel/?_m=195;lang=sk'
#cookie_file = sys.argv[2]



def get_cookie_jar(filename):
    """
    Protocol implementation for handling gsocmentors.com transactions
    Author: Noah Fontes nfontes AT cynigram DOT com
    License: MIT
    Original: http://blog.mithis.net/archives/python/90-firefox3-cookies-in-python

    Ported to Python 3 by Dotan Cohen
    """

    from io import StringIO
    import http.cookiejar
    import sqlite3

    con = sqlite3.connect(filename)
    cur = con.cursor()
    cur.execute("SELECT host, path, isSecure, expiry, name, value FROM moz_cookies")

    ftstr = ["FALSE","TRUE"]

    s = StringIO()
    s.write("""\
# Netscape HTTP Cookie File
# http://www.netscape.com/newsref/std/cookie_spec.html
# This is a generated file!  Do not edit.
""")

    for item in cur.fetchall():
        s.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (
            item[0], ftstr[item[0].startswith('.')], item[1],
            ftstr[item[2]], item[3], item[4], item[5]))

    s.seek(0)
    cookie_jar = http.cookiejar.MozillaCookieJar()
    cookie_jar._really_load(s, '', True, True)

    return cookie_jar






































print("asd")
sys.exit()



#Creating form sending to login
payload = {
"lang" : "sk",
'destination': '/auth',
#'credential_0': 'xbernato',
'credential_0': 'xjokay',
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
print(s.cookies)
from requests.utils import dict_from_cookiejar
cookies = dict_from_cookiejar(s.cookies) # s is your session object

for key, value in cookies.items():
    print("1:", key, value)

cj = get_cookie_jar(cookie_file)
cookies = dict_from_cookiejar(cj) # s is your session object
for key, value in cookies.items():
    print("2:", key, value)



sys.exit()
#s = requests.Session()
#r = s.get("https://test.is.stuba.sk/") #what is _m?
s.cookies = cj
r = requests.get("https://test.is.stuba.sk/auth/student/moje_studium.pl?_m=3110", cookies=cj) #what is _m?
print (r.text)







sys.exit()










#_--------------------------------------------------
















########################################################################################
from selenium import webdriver

profile = webdriver.FirefoxProfile('/home/ondrej/.mozilla/firefox/azo5kg9b.default')
browser = webdriver.Firefox(profile)



from requests.utils import dict_from_cookiejar
cookies = dict_from_cookiejar(s.cookies) # s is your session object

browser.get("https://test.is.stuba.sk/")
for key, value in cookies.items():
        browser.add_cookie({'name': key, 'value': value})

browser.get("https://test.is.stuba.sk/auth/ucitel/?_m=195;lang=sk")

browser.close()
sys.exit()

from threading import Thread
from time import sleep
import pyautogui

def threaded_write_pin(browser):
    print (browser.get_cookies())
    pin = "2144"
    sleep(3)
    pyautogui.keyDown('shift')  #SVK layout
    pyautogui.typewrite(pin, interval=0.25)
    pyautogui.keyUp('shift')    #SVK layout

    pyautogui.press('enter')
    sleep(3)
    pyautogui.press('enter')
    sleep(3)
    print("test")
    url = browser.command_executor._url       #"http://127.0.0.1:60622/hub"
    session_id = browser.session_id            #'4e167f26-dc1d-4f51-a207-f761eaf73c31'
    browser.quit()
    print (url, session_id)
    return url, session_id


print("0")
#thread = Thread(target=threaded_write_pin, args=(browser, ))
#browser.find_element_by_id("loginButton").click()
from selenium.webdriver.common.keys import Keys
#browser.set_page_load_timeout(4)
browser.find_element_by_id("loginButton").send_keys(Keys.ENTER)

print("1")
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#thread.start()
#wait = WebDriverWait(browser, 10)
#table = wait.until(EC.presence_of_element_located((By.ID, 'tmtab_1')))
print("2")
url, session_id = threaded_write_pin(browser)
#thread.join()







sys.exit()




profile = webdriver.FirefoxProfile('/home/ondrej/.mozilla/firefox/azo5kg9b.default')
driver = webdriver.Firefox(profile)



driver.get("https://centrum.sk")
print("test3")
print (driver.get_cookies())
print("3")
sys.exit()













def create_driver_session(session_id, executor_url):
    from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver

    # Save the original function, so we can revert our patch
    org_command_execute = RemoteWebDriver.execute

    def new_command_execute(self, command, params=None):
        if command == "newSession":
            # Mock the response
            return {'success': 0, 'value': None, 'sessionId': session_id}
        else:
            return org_command_execute(self, command, params)

    # Patch the function before creating the driver object
    RemoteWebDriver.execute = new_command_execute

    new_driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
    new_driver.session_id = session_id

    # Replace the patched function with original function
    RemoteWebDriver.execute = org_command_execute

    return new_driver

#driver = create_driver_session(session_id, url)



#driver = webdriver.Remote(command_executor=url,desired_capabilities=firefox_capabilities)
#driver.session_id = session_id























#print (browser.get_cookies())

sys.exit()
############################################################################
print("cookie")
print (browser.get_cookies())
sys.exit()
for cookie in browser.get_cookies():
    print (cookie)
    #c = {cookie['name']: cookie['value']}
    #s.cookies.update(c)


sys.exit() #TODOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO

#Parsing subjects url
match = "title=\"Sylabus predmetu\">(.*?)<.*?index.pl(\?predmet=[0-9]+)"
result = re.findall(match, r.text)
if result:
    print (result)
    #print (result.group(0))
    #print (result.group(1))
else:
    print ("no match found")

print (result[0][1])
#get group id
url = "https://test.is.stuba.sk/auth/nucitel/dochazka.pl"
final = url + result[0][1] + ";lang=sk"
r = s.get(final)
match = "<select name=\"vybrane_cviceni\".*?</select>"
result = re.search(match, r.text, re.DOTALL)
b = result.group()

match = "<option value=\"([0-9]+)\""
result = re.findall(match, b, re.DOTALL)
print ("vybrane cvicenia: ",b)
print ("value for option :", result)


payload = {
"lang" : "sk",
"predmet" : "313909",
"cviceni" : result[0],
"vybrane_cviceni" : [],
"vzorek" : "",
"omezit" : "Obmedziť",
}

for i in result:
    payload["vybrane_cviceni"].append(i)

print (payload)
print (final)
r = s.post(final, data=payload)







#get students data



#match = "<a href=\"/auth/lide/clovek.pl\?id=[0-9]+.*?>.*?<a href=\"/auth/nucitel/dochadzka.pl\?predmet="
#result = re.search(match, r.text, re.DOTALL)
#print (result)

#import lxml.html as h
#html = h.fromstring(r.text.encode())
#print (html)



#start = r.text.find("<a href=\"/auth/lide/clovek.pl?id=")
#print (start)
#end = r.text[start:].find("<a href=\"/auth/nucitel/dochazka.pl?predmet=")
#print (end)
#def find_all(a_str, sub):
#    start = 0
#    while True:
#        start = a_str.find(sub, start)
#        if start == -1: return
#        yield start
#        start += len(sub)
#print (list(find_all(r.text[start:start + end], "value")))




class Student:
    def __init__(self, name, cv_string, table_id, attendance, stud_and_group):
        self.name = name
        self.cv_string = cv_string
        self.table_id = table_id
        self.attendance = attendance
        self.study, self.group = self.parse_study_and_group(stud_and_group)

    def parse_study_and_group(self, study_and_group):
        group = study_and_group[:study_and_group.find("s")].lstrip("c")
        study = study_and_group[study_and_group.find("s")+1:study_and_group.find("k")]

        return study, group


def get_week_attendance(week):
    week = str(week)
    if week.find("div") > -1:
        if week.find("reqfields") > -1:
            return 0 #nezadane
        elif week.find("checked") > -1:
            return 1 #zucastnil sa
        return 4 #neospravedlnena neucast
    #elif week.find("unid=150323") > -1:
    elif week.find("unid=188026") > -1:
        return 7 #skorsi odchod
    #elif week.find("unid=149249") > -1:
    elif week.find("unid=188914") > -1:
        return 3 #ospravedlnena neucast
    #elif week.find("150269") > -1:
    elif week.find("187831") > -1:
        return 6 #pritomny na inom cviceni
    #elif week.find("148793") > -1:
    elif week.find("187220") > -1:
        return 5 #vyluceny z cvicenia
    #elif week.find("149101") > -1:
    elif week.find("187261") > -1:
        return 2 #zucastnil sa s neskorym prichodom

    return -1 #parsing failed

#from lxml.html import etree
from lxml import html
print ("------------------------------")
tree = html.fromstring(r.text.encode())
#tree.make_links_absolute(final)

table_id = 1
student_id = 1
name = addit_info = stud_and_group = ""
student_list = []


while True:
    table = tree.xpath("//table[@id='tmtab_%d']//tbody" %table_id)
    if not table:
        break;
    for row in table[0].xpath(".//tr"):
        temp_count = 0
        attendance = [-1] * 13
        for cell in row.xpath(".//td//small"):
            text = cell.xpath(".//text()")
            if text:
                text = text[0]
                if temp_count == 1:
                    name = text
                    temp_count += 1
                elif temp_count == 2:
                    addit_info = text
                    temp_count = 3
                try:
                    temp_id = int(text.rstrip("."))
                except ValueError:
                    continue
                if temp_id == student_id:
                    student_id += 1
                    temp_count = 1
                    continue
            if temp_count == 3:
                result = cell.xpath(".//div//input")
                if result:
                    stud_and_group = result[0].attrib["value"]
                    print(stud_and_group)

                print(html.etree.tostring(cell))
                attendance[0] = get_week_attendance(html.etree.tostring(cell))
                temp_count = 4
            elif temp_count == 4:
                print(html.etree.tostring(cell))
                attendance[1] = get_week_attendance(html.etree.tostring(cell))
                temp_count = 5
            elif temp_count == 5:
                attendance[2] = get_week_attendance(html.etree.tostring(cell))
                print(html.etree.tostring(cell))
                temp_count = 6
            elif temp_count == 6:
                attendance[3] = get_week_attendance(html.etree.tostring(cell))
                print(html.etree.tostring(cell))
                temp_count = 7
            elif temp_count == 7:
                attendance[4] = get_week_attendance(html.etree.tostring(cell))
                print(html.etree.tostring(cell))
                temp_count = 8
            elif temp_count == 8:
                attendance[5] = get_week_attendance(html.etree.tostring(cell))
                print(html.etree.tostring(cell))
                temp_count = 9
            elif temp_count == 9:
                attendance[6] = get_week_attendance(html.etree.tostring(cell))
                print(html.etree.tostring(cell))
                temp_count = 10
            elif temp_count == 10:
                attendance[7] = get_week_attendance(html.etree.tostring(cell))
                print(html.etree.tostring(cell))
                temp_count = 11
            elif temp_count == 11:
                attendance[8] = get_week_attendance(html.etree.tostring(cell))
                print(html.etree.tostring(cell))
                temp_count = 12
            elif temp_count == 12:
                attendance[9] = get_week_attendance(html.etree.tostring(cell))
                print(html.etree.tostring(cell))
                temp_count = 13
            elif temp_count == 13:
                attendance[10] = get_week_attendance(html.etree.tostring(cell))
                print(html.etree.tostring(cell))
                temp_count = 14
            elif temp_count == 14:
                attendance[11] = get_week_attendance(html.etree.tostring(cell))
                print(html.etree.tostring(cell))
                temp_count = 15
            elif temp_count == 15:
                attendance[12] = get_week_attendance(html.etree.tostring(cell))
                print(html.etree.tostring(cell))
                temp_count = 0
                print(name, attendance)
                student_list.append(Student(name, addit_info, table_id, attendance, stud_and_group))
                break


            #result = cell.xpath(".//div//input")
            #if result:
            #    stud_and_group = result[0].attrib["value"]
            #    temp_count = 0
            #    print ("RESULT:!",name,addit_info,stud_and_group)
            #    student_list.append(Student(name, addit_info, stud_and_group, table_id))
            #    break #one value is sufficient
    table_id += 1
    student_id = 1
    #break;
    #sys.exit()

for elem in student_list:
    print (elem.name, elem.cv_string, elem.table_id, elem.attendance, elem.study, elem.group)





url = "https://test.is.stuba.sk/auth/nucitel/dochazka.pl"
url += "?predmet=313909;" #predmet
url += "studium=" + str(student_list[0].study) + ";"
url += "podrobne=" + str(student_list[0].group) + ";"
url += "misto_vyuky=0;"
url += "vybrane_cviceni=" + str(student_list[0].group)

print (url)






payload = {
"lang" : "sk",
"predmet" : "313909",
"cviceni" : str(student_list[0].group),
"vybrane_cviceni" : str(student_list[0].group),
"podrobne" : str(student_list[0].group),
"studium" : str(student_list[0].study),
"misto_vyuky" : "0",
"dochazka1" : "0",
"dochazka2" : "1",
"dochazka3" : "2",
"dochazka4" : "4",
"dochazka5" : "0",
"dochazka6" : "0",
"dochazka7" : "0",
"dochazka8" : "0",
"dochazka9" : "0",
"dochazka10" : "0",
"dochazka11" : "0",
"dochazka12" : "0",
"dochazka13" : "6",
"ulozit_podrobne" : "Uložiť",
}


print (payload)


r = s.post(url, data=payload)











sys.exit()
    #############################################################
    #for row in table[0].xpath(".//tr"):
    #    for cell in row.xpath(".//td//small"):
    #        text = cell.xpath(".//text()")
    #        if text:
    #            text = text[0]
    #            if temp_count == 1:
    #                name = text
    #                temp_count += 1
    #            elif temp_count == 2:
    #                addit_info = text
    #                temp_count == 0
    #            try:
    #                temp_id = int(text.rstrip("."))
    #            except ValueError:
    #                continue
    #            if temp_id == student_id:
    #                student_id += 1
    #                temp_count = 1
    #        result = cell.xpath(".//div//input")
    #        if result:
    #            stud_and_group = result[0].attrib["value"]
    #            temp_count = 0
    #            print ("RESULT:!",name,addit_info,stud_and_group)
    #            student_list.append(Student(name, addit_info, stud_and_group, table_id))
    #            break #one value is sufficient
    #table_id += 1
    #student_id = 1
    ##break;
    ##sys.exit()
