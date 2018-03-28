#!/usr/bin/env python3

from fuzzywuzzy import process
import numpy as np
import cv2
import os
import pytesseract as p
from PIL import Image


def getImages():        #cisto na nacitanie vsetkych nazvov obrazkov do listu

    image_list = []

    for filename in os.listdir('ISIC/photos/'):
        image = cv2.imread('ISIC/photos/' + filename)
        image_list.append(image)

    return image_list


def processImage(image, index):

    #p.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

    #cesta k tesseract
    p.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'

    #otocim obrazok
    image = np.rot90(image, -1)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #aplikujem 'rodo'
    gray = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY)[1]

    cv2.imwrite("img" + str(index) + ".jpg", gray)
    temp = "img" + str(index) + ".jpg"

    name = p.image_to_string(Image.open("ISIC/images" + temp), lang='slk')

    #momentalne len na jediny funkcny obrazok, inak vyuzit riadok vyssie, kde vysklada nazov - asi lepsie spravit este jeden file na ukladanie obrazkov
    #name = p.image_to_string(Image.open("ISIC/fejk.png"), lang='slk')

    return name

    # cv2.imshow("Names", "fejk.png")
    # cv2.waitKey(0)


def closestMatch(studentList):
    #pri nacitani databazy naplnim list studentov menami, ktore tam su, nasledne porovnavam a hladam najblizsiu zhodu

    imageList = getImages()
    index = 0
    justNames = []

    #odstranim tituly z mien, vytvorim cisto zoznam mien a priezvisk
    for name in studentList:
        nameStudent, title = name.split(",")
        justNames.append(nameStudent)

    for image in imageList:
        name = processImage(image, index)

        #treba pip install fuzzywuzzy

        #toto najde nejak 3 najblizsie mena k hladanemu
        #matches = process.extract(name, justNames)

        #tu len top zhoda
        matches = process.extractOne(name, justNames)

        print("Closest match to " + name + " is: ")
        print(matches)

        index += 1


def get_name_from_image(image, studentList):

    name = processImage(image, 0)
    matches = process.extractOne(name, studentList)
    return matches
