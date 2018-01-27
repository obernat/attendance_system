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
