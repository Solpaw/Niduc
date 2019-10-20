import bchlib
import bitstring
import struct
from Analysis import Analysis
import numpy as np
class Receiver:
    def __init__(self):
        self.analysis = Analysis()

    def stworz_wiadomosc(self, i, lista=[]):
        tab = np.array([], dtype=int)
        for x in range(i, i + 7, 1):
            tab=np.append(tab, lista[x])
        return tab

    def decodeHamming(self, message):
        # m_wykrywania_bledow
        H = np.array([
            [1, 0, 1, 0, 1, 0, 1],
            [0, 1, 1, 0, 0, 1, 1],
            [0, 0, 0, 1, 1, 1, 1]])
        # tablica dekodowania
        R = np.array([
            [0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 1]
        ])
        # tablica naprawcza
        e = np.array([0, 0, 0, 0, 0, 0, 0])

        iterator = 0
        flips = 0

        whole_msg = np.array([], dtype=int)

        while iterator < len(message):
            msg = self.stworz_wiadomosc(iterator, message)
            iterator += 7
            # tablica bledow
            parity = (H @ msg) % 2

            try:
                e[self.przeszukaj_slownik(parity) - 1] = 1
                flips += 1
            except:
                np.array_equal(parity, np.zeros(3, int))


            msg = (msg + e) % 2
            recived = (R @ msg) % 2
            whole_msg = np.append(whole_msg, recived)
            e = np.array([0, 0, 0, 0, 0, 0, 0])

        self.analysis.setDecrypted(whole_msg)
        if flips == 0:
            self.analysis.addAmount(1, 0, 0)
        else:
            self.analysis.addAmount(0, 0, 1)

        print("Odkodowana wiadomość: ")
        print(whole_msg)


        return whole_msg




    def przeszukaj_slownik(self, parity=[]):
        binarne = {
            1: np.array([1, 0, 0]),
            2: np.array([0, 1, 0]),
            3: np.array([1, 1, 0]),
            4: np.array([0, 0, 1]),
            5: np.array([1, 0, 1]),
            6: np.array([0, 1, 1]),
            7: np.array([1, 1, 1])}

        for item in binarne.keys():
            if np.array_equal(binarne[item], parity):
                return item
        return None



    def decodeBCH(self, array):
        polynomial = 8219
        t = 2
        bch = bchlib.BCH(polynomial, t)
        data, code = array[:-bch.ecc_bytes], array[-bch.ecc_bytes:]
        data = bytearray(data)
        code = bytearray(code)
        flips, data, code = bch.decode(data, code)
        data = list(data)
        print("Odkodowana wiadomość: ")
        if flips is -1:
            self.analysis.addAmount(0, 1, 0)
        elif flips > 0:
            self.analysis.addAmount(0, 0, 1)
        elif flips is 0:
            self.analysis.addAmount(1, 0, 0)
        print(data)


