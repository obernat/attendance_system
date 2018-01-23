#!/usr/bin/python3
import requests
import sys
import re
from lxml import html

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


class Student:
    def __init__(self, name, cv_string, table_id, attendance):
        self.name = name
        self.cv_string = cv_string
        self.table_id = table_id
        self.attendance = attendance


def get_week_attendance(week):
    week = str(week)
    if week.find("div") > -1:
        if week.find("reqfields") > -1:
            return 0 #nezadane
        elif week.find("checked") > -1:
            return 1 #zucastnil sa
        return 4 #neospravedlnena neucast
    elif week.find("unid=150323") > -1:
        return 7 #skorsi odchod
    elif week.find("unid=149249") > -1:
        return 3 #ospravedlnena neucast
    elif week.find("150269") > -1:
        return 6 #pritomny na inom cviceni
    elif week.find("148793") > -1:
        return 5 #vyluceny z cvicenia
    elif week.find("149101") > -1:
        return 2 #zucastnil sa s neskorym prichodom

    return -1 #parsing failed


def get_all_students_details(s, subject_id, groups):

    if s == None:
        return -5, None #session not created

    url = "https://test.is.stuba.sk/auth/nucitel/dochazka.pl?predmet=" + \
            str(subject_id) + ";lang=sk"

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

    try:
    	r = s.post(url, data=payload, timeout=10)
    except requests.exceptions.RequestException as e:
        print(e) #Logger
        return -4 #timeout, bad url


    #parse students
    tree = html.fromstring(r.text.encode())

    table_id = 1
    student_id = 1
    student_list = []

    while True: #iterate over all tables
        table = tree.xpath("//table[@id='tmtab_%d']//tbody" %table_id)
        if not table:
            break;
        for row in table[0].xpath(".//tr"): #iterate over all rows(students)
            temp_count = 0
            attendance = [-1] * 13
            name = addit_info = ""
            for cell in row.xpath(".//td//small"): #iterate over all cells(one student)
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
                    attendance[0] = get_week_attendance(html.etree.tostring(cell))
                    temp_count = 4
                elif temp_count == 4:
                    attendance[1] = get_week_attendance(html.etree.tostring(cell))
                    temp_count = 5
                elif temp_count == 5:
                    attendance[2] = get_week_attendance(html.etree.tostring(cell))
                    temp_count = 6
                elif temp_count == 6:
                    attendance[3] = get_week_attendance(html.etree.tostring(cell))
                    temp_count = 7
                elif temp_count == 7:
                    attendance[4] = get_week_attendance(html.etree.tostring(cell))
                    temp_count = 8
                elif temp_count == 8:
                    attendance[5] = get_week_attendance(html.etree.tostring(cell))
                    temp_count = 9
                elif temp_count == 9:
                    attendance[6] = get_week_attendance(html.etree.tostring(cell))
                    temp_count = 10
                elif temp_count == 10:
                    attendance[7] = get_week_attendance(html.etree.tostring(cell))
                    temp_count = 11
                elif temp_count == 11:
                    attendance[8] = get_week_attendance(html.etree.tostring(cell))
                    temp_count = 12
                elif temp_count == 12:
                    attendance[9] = get_week_attendance(html.etree.tostring(cell))
                    temp_count = 13
                elif temp_count == 13:
                    attendance[10] = get_week_attendance(html.etree.tostring(cell))
                    temp_count = 14
                elif temp_count == 14:
                    attendance[11] = get_week_attendance(html.etree.tostring(cell))
                    temp_count = 15
                elif temp_count == 15:
                    attendance[12] = get_week_attendance(html.etree.tostring(cell))
                    temp_count = 0
                    student_list.append(Student(name, addit_info, table_id, attendance))
                    break

        table_id += 1
        student_id = 1

    for elem in student_list:
        print (elem.name, elem.cv_string, elem.table_id, elem.attendance)


    def download_routine(name="none",password = "none"):
        session = requests.Session()

        #login
        ret_value = try_login(session, name, password)
        if ret_value < 0:
            printf("Nesprávne prihlasovacie údaje!")
            return

        #download subjects
        ret_value, subjects_list_with_links = get_subjects(self.session)
        if ret_value == -1:
            printf("K dispozícii nie sú žiadne predmety!")
        elif ret_value < -1:
            printf("Nepodarilo sa pripojiť ku sieti!")
            return

        #do it for all subjects

