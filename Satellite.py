import bitstring
import random
import time
from random import randint
from Receiver import Receiver
import bchlib
import struct
import numpy as np
import random

class Satellite:
    def __init__(self):
        self.frequency = 0
        self.posX = 0
        self.posY = 0
        self.posZ = 0
        self.chooseEncryption = "Hamming"
        self.receiver = Receiver()
        self.noiseLevel = 0.05

    def sendPositionHamming(self, array):

        self.receiver.decodeHamming(self.Noise(array, self.noiseLevel))



    def sendPositionBCH(self, array):
        self.receiver.decodeBCH(self.Noise(array, self.noiseLevel))

    def Noise(self, array, noise):

        amountOfMistakes = len(array) * noise
        amountOfMistakes = round(amountOfMistakes)

        temp = []
        y = 0

        while y < amountOfMistakes:
            help = False
            r = random.randint(0, len(array) - 1)
            for z in range(len(temp)):
                if temp[z] is r:
                    help = True
                    break
            if help is False:
                temp.append(r)
                y += 1
        for l in temp:
            q = random.randint(0, 1)
            if q == 0:
                if array[l] is 1:
                    array[l] = 0

                else:
                    array[l] = 1
        return array

    def encryptHamming(self, list):

        self.receiver.analysis.setOriginal(list)

        czy_dopisac = 4 - ((len(list)) % 4)
        if czy_dopisac < 4:
            self.dopisz(czy_dopisac)

        whole_msg= np.array([], dtype=int)

        iterator = 0

        while iterator < len(list):
            msg = self.stworz_wiadomosc( iterator, list)
            iterator += 4

            kod = self.kod_hamming(msg)


            whole_msg = np.append(whole_msg, kod)
        print("Zakodowana wiadomość: ")
        print(whole_msg)
        return whole_msg

    def encryptBCH(selfself, array):
        polynomial = 8219
        t = 2
        bch = bchlib.BCH(polynomial, t)

        data = bytearray(array)

        code = bch.encode(data)
        result = data + code
        result = list(result)
        return result

    def generatePosition(self):
        while True:
            self.posX = random.uniform(-180.0, 180.0)
            self.posY = random.uniform(-90.0, 90.0)
            self.posZ = randint(10000, 11000)
            self.posX = round(self.posX, 6)
            self.posY = round(self.posY, 6)
            print("Pozycja X: ")
            print(self.posX)
            print("Pozycja Y: ")
            print(self.posY)
            print("Wysokość: ")

            print(self.posZ)
            print()

            self.posX = bitstring.BitArray(float = self.posX, length = 64)
            self.receiver.analysis.setOriginal(self.posX)
            print("Pozycja X: ")
            #print(self.posX.bin)
            for x in self.posX.bin :
                print(x, end=' ')
            print('\n')
            if self.chooseEncryption == "Hamming":
                self.sendPositionHamming(self.encryptHamming(self.posX))
            elif self.chooseEncryption == "BCH":
                self.sendPositionBCH(self.encryptBCH(self.posX))
            self.posY = bitstring.BitArray(float = self.posY, length = 64)
            self.receiver.analysis.setOriginal(self.posY)
            print()
            print("Pozycja Y: ")
            print(self.posY.bin)
            if self.chooseEncryption == "Hamming":
                self.sendPositionHamming(self.encryptHamming(self.posY))
            elif self.chooseEncryption == "BCH":
                self.sendPositionBCH(self.encryptBCH(self.posY))
            self.posZ = bitstring.BitArray(int = self.posZ, length = 64)
            self.receiver.analysis.setOriginal(self.posZ)
            print()
            print("Wysokość: ")
            print(self.posZ.bin)
            if self.chooseEncryption == "Hamming":
                self.sendPositionHamming(self.encryptHamming(self.posZ))
            elif self.chooseEncryption == "BCH":
                self.sendPositionBCH(self.encryptBCH(self.posZ))

            time.sleep(self.frequency)

    def kod_hamming(self, msg=[]):
        G = np.array([  # macierz generująca
            [1, 1, 0, 1],
            [1, 0, 1, 1],
            [1, 0, 0, 0],
            [0, 1, 1, 1],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1], ])

        kod = (G @ msg) % 2

        return kod


    def dopisz(self, dopisanie):
        for i in range(0, dopisanie, 1):
            list.append(0)

    def stworz_wiadomosc(self, i, list=[]):
        tab = []
        for x in range(i, i + 4, 1):
            tab.append(list[x])
        return tab

