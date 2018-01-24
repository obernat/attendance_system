from __future__ import print_function
from time import sleep

from smartcard.CardConnectionObserver import ConsoleCardConnectionObserver
from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.util import toHexString


SELECT = [0xFF, 0xCA, 0x00, 0x00, 0x00]
class read_card2(CardObserver):

    def change_attendance_card(self, guj, subject_name, group, week_selected, a, name, week):
        guj.attendance[str(name)][int(week)] = a
        guj.save_attendace()
        guj.subject_info_page(subject_name, group, week_selected)

    def int_array_to_hex_separated_string(self, arr):
        return "".join("{:02x}:".format(item) for item in arr)[:-1]

    def __init__(self, gui):
        self.observer = ConsoleCardConnectionObserver()
        self.gui = gui

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
            self.change_attendance_card(self.gui, "Operačné systémy", "Skupina 1", "Tyzden 1", 1, "Tomas", 0)
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


