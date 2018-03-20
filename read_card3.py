from __future__ import print_function
from time import sleep

from smartcard.CardConnectionObserver import ConsoleCardConnectionObserver
from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.util import toHexString
import glob
import os

SELECT = [0xFF, 0xCA, 0x00, 0x00, 0x00]
class read_card2(CardObserver):

    def int_array_to_hex_separated_string(self, arr):
        return "".join("{:02x}:".format(item) for item in arr)[:-1]

    def __init__(self, gui, page_number):
        self.observer = ConsoleCardConnectionObserver()
        self.gui = gui
        self.page_number = page_number

    def update(self, observable, actions):
        (addedcards, removedcards) = actions
        for card in addedcards:
            card.connection = card.createConnection()
            card.connection.connect()
            card.connection.addObserver(self.observer)
            response, sw1, sw2 = card.connection.transmit(SELECT)
            hex_id = self.int_array_to_hex_separated_string(response)
            chip_id = int("".join(item for item in list(reversed(hex_id.split(':')))), 16)
            print("+Inserted: pokus")
            list_of_files = glob.glob('ISIC/images/*')  # * means all if need specific format then *.csv
            latest_file = max(list_of_files, key=os.path.getctime)
            print(latest_file)
            if(1):
                self.gui.students_dict['Baka Tomáš, Bc.']=chip_id
                self.gui.database_page(self.page_number)
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