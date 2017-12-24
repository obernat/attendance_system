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
    def __init__(self, name, cv_string, study_and_group, table_id):
        self.name = name
        self.cv_string = cv_string
        self.study, self.group = self.parse_study_and_group(study_and_group)
        self.table_id = table_id

    def parse_study_and_group(self, study_and_group):
        #match = "c([0-9]+)s([0-9]+)k"
        #result = re.search(match, study_and_group)
        #if result:
        #   return 1, str(result.group(1)), str(result.group(2))
        #else:
        #    return -1 #parsing error

        study = study_and_group[:study_and_group.find("s")].lstrip("c")
        group = study_and_group[study_and_group.find("s")+1:study_and_group.find("k")]

        return study, group


from lxml.html import etree
from lxml import html
print ("------------------------------")
tree = html.fromstring(r.text.encode())
#tree.make_links_absolute(final)

table_id = 1
student_id = 1
temp_count = 0
name = addit_info = stud_and_group = ""
student_list = []

while True:
    table = tree.xpath("//table[@id='tmtab_%d']//tbody" %table_id)
    if not table:
        break;
    for row in table[0].xpath(".//tr"):
        for cell in row.xpath(".//td//small"):
            text = cell.xpath(".//text()")
            if text:
                text = text[0]
                if temp_count == 1:
                    name = text
                    temp_count += 1
                elif temp_count == 2:
                    addit_info = text
                    temp_count == 0
                try:
                    temp_id = int(text.rstrip("."))
                except ValueError:
                    continue
                if temp_id == student_id:
                    student_id += 1
                    temp_count = 1
            result = cell.xpath(".//div//input")
            if result:
                stud_and_group = result[0].attrib["value"]
                temp_count = 0
                print ("RESULT:!",name,addit_info,stud_and_group)
                student_list.append(Student(name, addit_info, stud_and_group, table_id))
                break #one value is sufficient
    table_id += 1
    student_id = 1
    #break;
    #sys.exit()

for elem in student_list:
    print (elem.name, elem.study, elem.group, elem.table_id)


