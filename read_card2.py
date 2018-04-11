from __future__ import print_function
from time import sleep

from smartcard.CardConnectionObserver import ConsoleCardConnectionObserver
from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.util import toHexString
import  error_handler as er


SELECT = [0xFF, 0xCA, 0x00, 0x00, 0x00]
class read_card2(CardObserver):

    def int_array_to_hex_separated_string(self, arr):
        return "".join("{:02x}:".format(item) for item in arr)[:-1]

    def __init__(self, gui, subject, group, week):
        self.observer = ConsoleCardConnectionObserver()
        self.gui = gui
        self.subject = subject
        self.group = group
        self.week = week

    def update(self, observable, actions):
        (addedcards, removedcards) = actions
        for card in addedcards:
            card.connection = card.createConnection()
            card.connection.connect()
            card.connection.addObserver(self.observer)
            response, sw1, sw2 = card.connection.transmit(SELECT)
            hex_id = self.int_array_to_hex_separated_string(response)
            chip_id = int("".join(item for item in list(reversed(hex_id.split(':')))), 16)
            print("+Inserted: ")
            print(chip_id)

            student_name = ""

            for student in self.gui.students_list:
                if student.ISIC==chip_id:
                    student_name=student.full_name
            #student_name = 'Baka Tomáš, Bc.'
            #print(student_name)
            print(self.subject)
            _, number_of_week = self.week.split(' ')

            if student_name == "":
                er.showError("Neexistuje par meno - isic")

            else:
                self.gui.change_attendance_from_card(self.subject, self.group, int(number_of_week)-1, 6, student_name, self.week)
                self.cards.add(chip_id)
        for card in removedcards:
            print("-Removed: ", toHexString(card.atr))

    #Make new thread and start read cards
    def readCards(self):
        cardmonitor = CardMonitor()
        self.cards = {}
        cardmonitor.addObserver(self)
        return cardmonitor

    #Destroy the thread and stop read cards, return set of read cards
    def stopReadCards(self, cardmonitor):
        cardmonitor.deleteObserver(self)
        return self.cards


