#!/usr/bin/python3
import requests
import sys
import re
from lxml import html
import database as db


# PRIVATE FUNCTIONS ---------------------------------------------------------


def try_login(s, name, password, timeout=86400):
    if s is None:
        return -4  # session not created

    # Creating form sending to login
    payload = {
        'lang': 'sk',
        'destination': '/auth',
        'credential_0': name,
        'credential_1': password,
        'credential_2': '86400',
        'login': 'Prihlásenie'
    }

    # Creating session. Session object persist cookies, uses connection pooling
    #s = requests.Session()

    # Creating post with given payload to log in, cookies saved for future
    try:
        r = s.post(
            "https://test.is.stuba.sk/auth/?lang=sk",
            data=payload,
            timeout=10)
    except requests.exceptions.RequestException as e:
        print(e)  # Logger
        return -4  # timeout, bad url

    # scheme dependent
    # Parsing div log
    #match = "<div id=\"log\">.*?</div>"
    #result = re.search(match, r.text, re.DOTALL)
    # if not result:
    #    match = "<div id=\"prihlasen\">.*?</div>"
    #    result = re.search(match, r.text, re.DOTALL)
    # if result:
    #    result = str(result.group())
    #    if (result.find("Prihlásený") != -1 or result.find("Logged in") != -1):
    #        return 1
    #    else:
    #        return -1 #login error
    # else:
    #    return -2 #parsing error

    if (r.text.find("Nesprávne prihlasovacie meno alebo heslo.") != -1 or
            r.text.find("Prihlasovací formulár nebol korektne vyplnený.") != -1):
        return -1  # login error
    else:
        return 1


def get_subjects(s):
    #download only subjects administrating by user!

    if s is None:
        return -4, None  # session not created

    # Creating get to teacher page, cookies send automatically
    try:
        r = s.get(
            "https://test.is.stuba.sk/auth/ucitel/?_m=195;lang=sk",
            timeout=10)  # what is _m?
    except requests.exceptions.RequestException as e:
        print(e)  # Logger
        return -3, None  # timeout, bad url

    # Creating get to delegated teacher page
    #r = s.get("https://test.is.stuba.sk/auth/ucitel/?lang=sk;delegid=10139")

    if r.status_code != 200:
        return -2, None  # error getting the page, maybe page down/no internet access

    # Parsing subjects url
    #download only administratint subjects
    match = "title=\"Sylabus predmetu\">(.*?)<.*?index.pl\?predmet=([0-9]+)"
    result = re.finditer(match, r.text, re.DOTALL)
    list_of_subjects_with_ids = []
    if result:
        for m in result:
            if m.group(0).find("alt=\"Administratíva\"") > -1:
                list_of_subjects_with_ids.append(tuple(m.groups()))
        if len(list_of_subjects_with_ids) == 0:
            return -1, None #parsing error, no administrating subjects
        print (list_of_subjects_with_ids)
        return 1, list_of_subjects_with_ids
    else:
        return -1, None  # parsing error, no subjects


def get_groups_ids(s, subject_id):

    if s is None:
        return -5, None  # session not created

    url = "https://test.is.stuba.sk/auth/nucitel/dochazka.pl?predmet=" + \
        str(subject_id) + ";lang=sk"

    try:
        r = s.get(url, timeout=10)
    except requests.exceptions.RequestException as e:
        print(e)  # Logger
        return -4, None  # timeout, bad url

    if r.status_code != 200:
        return -3, None  # error getting the page, maybe page down/no internet access

    match = "<select name=\"vybrane_cviceni\".*?</select>"
    result_select = re.search(match, r.text, re.DOTALL)
    if not result_select:
        return -1, None  # parsing error, no groups
    else:
        result_select = result_select.group()
        match = "<option value=\"([0-9]+)\""
        result = re.findall(match, result_select, re.DOTALL)
        if result:
            return 1, result
        else:
            return -1, None  # parsing error, no groups


def get_week_attendance(week):
    week = str(week)
    if week.find("div") > -1:
        if week.find("reqfields") > -1:
            return 0  # nezadane
        elif week.find("checked") > -1:
            return 1  # zucastnil sa
        return 4  # neospravedlnena neucast
    elif week.find("unid=188026") > -1 or week.find("unid=150323") > -1:
        return 7  # skorsi odchod
    elif week.find("unid=188914") > -1 or week.find("unid=149249") > -1:
        return 3  # ospravedlnena neucast
    elif week.find("187831") > -1 or week.find("150269") > -1:
        return 6  # pritomny na inom cviceni
    elif week.find("187220") > -1 or week.find("148793") > -1:
        return 5  # vyluceny z cvicenia
    elif week.find("187261") > -1 or week.find("149101") > -1:
        return 2  # zucastnil sa s neskorym prichodom

    return -1  # parsing failed


def get_all_students_data(s, subject_id, groups):

    if s is None:
        return -5, None  # session not created

    url = "https://test.is.stuba.sk/auth/nucitel/dochazka.pl?predmet=" + \
        str(subject_id) + ";lang=sk"

    payload = {
        "lang": "sk",
        "predmet": str(subject_id),
        "cviceni": groups[0],
        "vybrane_cviceni": [],
        "vzorek": "",
        "omezit": "Obmedziť",
    }

    for i in groups:
        payload["vybrane_cviceni"].append(i)

    try:
        r = s.post(url, data=payload, timeout=10)
    except requests.exceptions.RequestException as e:
        print(e)  # Logger
        return -4, None  # timeout, bad url

    # parse students
    tree = html.fromstring(r.text.encode())

    table_id = 1
    student_id = 1
    student_list = []

    while True:  # iterate over all tables
        if r.text.find("tmtab_1") != -1:
            table = tree.xpath("//table[@id='tmtab_%d']//tbody" % table_id)
        elif r.text.find("table_1") != -1:
            table = tree.xpath("//table[@id='table_%d']//tbody" % table_id)
        else:
            return -3, None  # html with tables was modified
        if not table:
            break
        for row in table[0].xpath(".//tr"):  # iterate over all rows(students)
            temp_count = 0
            attendance = [-1] * 13
            name = addit_info = stud_and_group = ""
            for cell in row.xpath(
                    ".//td//small"):  # iterate over all cells(one student)
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
                    attendance[0] = get_week_attendance(
                        html.etree.tostring(cell))
                    temp_count = 4
                elif temp_count == 4:
                    attendance[1] = get_week_attendance(
                        html.etree.tostring(cell))
                    temp_count = 5
                elif temp_count == 5:
                    attendance[2] = get_week_attendance(
                        html.etree.tostring(cell))
                    temp_count = 6
                elif temp_count == 6:
                    attendance[3] = get_week_attendance(
                        html.etree.tostring(cell))
                    temp_count = 7
                elif temp_count == 7:
                    attendance[4] = get_week_attendance(
                        html.etree.tostring(cell))
                    temp_count = 8
                elif temp_count == 8:
                    attendance[5] = get_week_attendance(
                        html.etree.tostring(cell))
                    temp_count = 9
                elif temp_count == 9:
                    attendance[6] = get_week_attendance(
                        html.etree.tostring(cell))
                    temp_count = 10
                elif temp_count == 10:
                    attendance[7] = get_week_attendance(
                        html.etree.tostring(cell))
                    temp_count = 11
                elif temp_count == 11:
                    attendance[8] = get_week_attendance(
                        html.etree.tostring(cell))
                    temp_count = 12
                elif temp_count == 12:
                    attendance[9] = get_week_attendance(
                        html.etree.tostring(cell))
                    temp_count = 13
                elif temp_count == 13:
                    attendance[10] = get_week_attendance(
                        html.etree.tostring(cell))
                    temp_count = 14
                elif temp_count == 14:
                    attendance[11] = get_week_attendance(
                        html.etree.tostring(cell))
                    temp_count = 15
                elif temp_count == 15:
                    attendance[12] = get_week_attendance(
                        html.etree.tostring(cell))
                    temp_count = 16
                elif temp_count == 16:
                    result = cell.xpath(".//a")
                    if not result:
                        return -2, None  # html table was modified
                    stud_and_group = result[0].attrib["href"]

                    temp_count = 0
                    student_list.append(
                        db.Student(
                            name,
                            addit_info,
                            table_id,
                            attendance,
                            stud_and_group))
                    break

        table_id += 1
        student_id = 1

    print ("---------------------------------------------------------")
    for elem in student_list:
        print (elem.name, elem.cv_string, elem.table_id, elem.attendance)

    return 1, student_list


def merge_IS_attendance_with_local(IS_student_list, local_student_list):
    # iterate over local student list
    for local_student in local_student_list:
        for IS_student in IS_student_list:
            if IS_student.name != local_student.name:
                continue
            # iterate over IS attendance, if there is some attendance record(>0), apply it
            # we dont care about its value, if is the same as ours, applying change nothing
            # if not, we have to apply, IS has higher priority
            for i in range(0, 13):
                if IS_student.attendance[i] > 0:
                    local_student.attendance[i] = IS_student.attendance[i]


def download_subject_attendance(session, subject):

    if session is None:
        return -5  # session not created

    # download subjects
    ret_value, subjects_list_with_links = get_subjects(session)
    if ret_value == -1:
        print("K dispozícii nie sú žiadne predmety s administrátorskými právami!")
    elif ret_value < -1:
        print("Nepodarilo sa pripojiť ku sieti!")
        return -4

    # iterate all subjects and find given
    for name, sub_id in subjects_list_with_links:
        if name != subject.name:
            continue
        # get list of ids
        ret_value, group_ids = get_groups_ids(session, sub_id)
        if ret_value < 0:
            print("Nepodarilo sa vyparsovať skupiny!")
            return -3

        # get students attendance
        ret_value, stud_list = get_all_students_data(
            session, sub_id, group_ids)
        if ret_value < 0:
            print("Nepodarilo sa vyparsovať údaje o študentoch")
            return -2

        # compare attendance from AIS with local, merge
        merge_IS_attendance_with_local(stud_list, subject.student_list)

    return 1

# PUBLIC FUNCTIONS -------------------------------------------------


def try_connection():
    s = requests.Session()
    try:
        r = s.get("https://test.is.stuba.sk", timeout=10)
    except requests.exceptions.RequestException as e:
        print(e)  # Logger
        return -1  # timeout, bad url

    return 1


def download_routine(name="none", password="none"):
    session = requests.Session()
    teacher = db.Teacher()

    # login
    ret_value = try_login(session, name, password)
    if ret_value < 0:
        print("Nesprávne prihlasovacie údaje!")
        return -4, None

    # download subjects
    ret_value, subjects_list_with_links = get_subjects(session)
    if ret_value == -1:
        print("K dispozícii nie sú žiadne predmety s administrátorskými právami!")
    elif ret_value < -1:
        print("Nepodarilo sa pripojiť ku sieti!")
        return -3, None

    # iterate all subjects
    for name, sub_id in subjects_list_with_links:
        # get list of ids
        ret_value, group_ids = get_groups_ids(session, sub_id)
        if ret_value < 0:
            print("Nepodarilo sa vyparsovať skupiny!")
            return -2, None

        # get students attendance
        ret_value, stud_list = get_all_students_data(
            session, sub_id, group_ids)
        if ret_value < 0:
            print("Nepodarilo sa vyparsovať údaje o študentoch")
            return -1, None
        teacher.subjects_list.append(db.Subject(name, sub_id, stud_list))

    return 1, teacher


def upload_routine(subject, name="none", password="none"):
    session = requests.Session()

    # login
    ret_value = try_login(session, name, password)
    if ret_value < 0:
        print("Nesprávne prihlasovacie údaje!")
        return -3

    # merge attendance with IS
    ret_value = download_subject_attendance(session, subject)
    if ret_value < 0:
        print("Synchronizácia údajov bola neúspešná!")
        return -2

    # upload students attendance for each student
    for student in subject.student_list:
        url = "https://test.is.stuba.sk/auth/nucitel/dochazka.pl"
        url += "?predmet=" + str(subject.sid) + ";"  # predmet
        url += "studium=" + str(student.study) + ";"
        url += "podrobne=" + str(student.group) + ";"
        url += "misto_vyuky=0;"
        url += "vybrane_cviceni=" + str(student.group)

        payload = {
            "lang": "sk",
            "predmet": str(subject.sid),
            "cviceni": str(student.group),
            "vybrane_cviceni": str(student.group),
            "podrobne": str(student.group),
            "studium": str(student.study),
            "misto_vyuky": "0",
            "dochazka1": str(student.attendance[0]),
            "dochazka2": str(student.attendance[1]),
            "dochazka3": str(student.attendance[2]),
            "dochazka4": str(student.attendance[3]),
            "dochazka5": str(student.attendance[4]),
            "dochazka6": str(student.attendance[5]),
            "dochazka7": str(student.attendance[6]),
            "dochazka8": str(student.attendance[7]),
            "dochazka9": str(student.attendance[8]),
            "dochazka10": str(student.attendance[9]),
            "dochazka11": str(student.attendance[10]),
            "dochazka12": str(student.attendance[11]),
            "dochazka13": str(student.attendance[12]),
            "ulozit_podrobne": "Uložiť",
        }

        try:
            r = session.post(url, data=payload, timeout=10)
        except requests.exceptions.RequestException as e:
            print(e)  # Logger
            return -1  # timeout, bad url

        print ("Student " + student.name + " synced.")

    return 1


#ret, a = download_routine("xbernato", sys.argv[1])
#import database_handler as dbh
#dbh.create_database_of_students(a)
# print(a.subjects_list[0].name)
# print(a.subjects_list[0].student_list[0].name)
# print(a.subjects_list[0].student_list[0].study)
# print(a.subjects_list[0].student_list[0].group)
#a.subjects_list[0].student_list[0].attendance[0] = 3
#a.subjects_list[0].student_list[3].attendance[0] = 6
#a.subjects_list[0].student_list[3].attendance[1] = 6
#a.subjects_list[0].student_list[0].attendance[1] = 3
#a.subjects_list[0].student_list[0].attendance[2] = 3
#a.subjects_list[0].student_list[0].attendance[3] = 3
#a.subjects_list[0].student_list[0].attendance[4] = 3
#a.subjects_list[0].student_list[0].attendance[5] = 3
#a.subjects_list[0].student_list[0].attendance[6] = 3
#a.subjects_list[0].student_list[0].attendance[7] = 3
#upload_routine(a.subjects_list[0], "xbernato", sys.argv[1])
