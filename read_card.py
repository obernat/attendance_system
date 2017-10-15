#!/usr/bin/python3

from smartcard.CardType import AnyCardType
from smartcard.CardRequest import CardRequest
from smartcard.util import toHexString
from smartcard.ATR import ATR

def int_array_to_hex_separated_string(arr):
    return "".join("{:02x}:".format(item) for item in arr)[:-1]


cardtype = AnyCardType()
cardrequest = CardRequest( timeout=1, cardType=cardtype )
cardservice = cardrequest.waitforcard()

cardservice.connection.connect()
print(toHexString( cardservice.connection.getATR() ))
print(cardservice.connection.getReader())

print("\n\n")
atr = ATR(cardservice.connection.getATR())

print(atr)
print('historical bytes: ', toHexString(atr.getHistoricalBytes()))
print('checksum: ', "0x%X" % atr.getChecksum())
print('checksum OK: ', atr.checksumOK)
print('T0  supported: ', atr.isT0Supported())
print('T1  supported: ', atr.isT1Supported())
print('T15 supported: ', atr.isT15Supported())



SELECT = [0xFF, 0xCA, 0x00, 0x00, 0x00]
data, sw1, sw2 = cardservice.connection.transmit( SELECT )
print ("%x %x" % (sw1, sw2))
print (data)


hex_id = int_array_to_hex_separated_string(data)
chip_id = int("".join(item for item in list(reversed(hex_id.split(':')))), 16)
print (chip_id)


