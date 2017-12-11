from __future__ import print_function
from time import sleep

from smartcard.CardConnectionObserver import ConsoleCardConnectionObserver
from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.util import toHexString

SELECT = [0xFF, 0xCA, 0x00, 0x00, 0x00]


def int_array_to_hex_separated_string(arr):
    return "".join("{:02x}:".format(item) for item in arr)[:-1]

class selectDFTELECOMObserver(CardObserver):


    def __init__(self):
        self.observer = ConsoleCardConnectionObserver()

    def update(self, observable, actions):
        (addedcards, removedcards) = actions
        for card in addedcards:
            card.connection = card.createConnection()
            card.connection.connect()
            card.connection.addObserver(self.observer)
            response, sw1, sw2 = card.connection.transmit(SELECT)
            hex_id = int_array_to_hex_separated_string(response)
            chip_id = int("".join(item for item in list(reversed(hex_id.split(':')))), 16)
            print("+Inserted: ")
            print(chip_id)

        for card in removedcards:
            print("-Removed: ", toHexString(card.atr))


    def readCards(self):
        cardmonitor = CardMonitor()
        #selectobserver = selectDFTELECOMObserver()
        cardmonitor.addObserver(self)
        return cardmonitor

    def stopReadCards(self, cardmonitor):
        cardmonitor.deleteObserver(self)


print("Insert or remove a SIM card in the system.")
selelectObserver = selectDFTELECOMObserver()
cardmonitor = selelectObserver.readCards()
sleep(10)
selelectObserver.stopReadCards(cardmonitor)


import sys
if 'win32' == sys.platform:
    print('press Enter to continue')
    sys.stdin.read(1)