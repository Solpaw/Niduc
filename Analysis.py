import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats


class Analysis:
    def __init__(self):
        self.correctPackets = 0
        self.corruptedPackets = 0
        self.fixedPackets = 0
        self.counter = 0
        self.packets = 3000
        self.chooseEncryption = "Hamming"
        self.originalMsg =[]
        self.decryptedhamming =[]
        self.firstRun = True
        self.firstRunCsv = True
    def setOriginal(self, msg):
        self.originalMsg.clear()
        for x in msg:
            self.originalMsg.append(x)

    def setDecrypted(self, msg):
        self.decryptedhamming.clear()
        for x in msg:
            self.decryptedhamming.append(x)

    def addAmount(self, corr, corrp, fix):
        self.correctPackets += corr
        self.corruptedPackets += corrp
        self.fixedPackets += fix
        if self.chooseEncryption is "BCH":
            if self.correctPackets + self.corruptedPackets + self.fixedPackets >=self.packets:
                self.writeData()
                self.correctPackets = 0
                self.corruptedPackets = 0
                self.fixedPackets = 0
                self.counter +=1
        elif self.chooseEncryption is "Hamming":
            self.if_corrupted( self.originalMsg, self.decryptedhamming)
            if self.correctPackets + self.corruptedPackets + self.fixedPackets >= self.packets:
                self.writeData()
                self.correctPackets = 0
                self.corruptedPackets = 0
                self.fixedPackets = 0
                self.counter +=1


        if self.counter is 50:
            self.drawHistogram()

    def writeData(self):
        if self.firstRun is True:
            with open('data.csv', 'w', newline='') as csvfile:
                datawriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                datawriter.writerow([self.correctPackets, self.corruptedPackets, self.fixedPackets])
            with open('corrected.csv', 'w', newline='') as csvfile:
                datawriter2 = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                datawriter2.writerow([self.correctPackets])
            with open('corrupted.csv', 'w', newline='') as csvfile:
                datawriter3 = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                datawriter3.writerow([self.corruptedPackets])
            with open('fixed.csv', 'w', newline='') as csvfile:
                datawriter4 = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                datawriter4.writerow([self.fixedPackets])
            self.firstRun = False
        else:
            with open('data.csv', 'a', newline='') as csvfile:
                datawriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                datawriter.writerow([self.correctPackets, self.corruptedPackets, self.fixedPackets])
            with open('corrected.csv', 'a', newline='') as csvfile:
                datawriter2 = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                datawriter2.writerow([self.correctPackets])
            with open('corrupted.csv', 'a', newline='') as csvfile:
                datawriter3 = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                datawriter3.writerow([self.corruptedPackets])
            with open('fixed.csv', 'a', newline='') as csvfile:
                datawriter4 = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                datawriter4.writerow([self.fixedPackets])



    def drawHistogram(self):
        array = []

        with open('corrupted.csv', mode='r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                array.append(int(row[0]))
        population = array
        plt.hist(population, density=1)
        xt = plt.xticks()[0]
        xmin, xmax = min(xt), max(xt)
        lnspc = np.linspace(xmin, xmax, len(population))

        m, s = stats.norm.fit(population)
        self.fivePoint(m, s)
        pdf_g = stats.norm.pdf(lnspc, m, s)
        plt.plot(lnspc, pdf_g)


        plt.title("Rozklad prawdopodobienstwa wystapienia danej ilosci bledow")
        plt.ylabel('Prawdopodobienstwo wystapienia')
        plt.xlabel('Ilosc bledow')

        plt.show()

    def if_corrupted(self, send_msg, dec_msg):
        iterator = 0
        while iterator < len(send_msg):
            smsg = self.stworz_wiadomosc(iterator, send_msg)
            dmsg = self.stworz_wiadomosc(iterator, dec_msg)

            if np.array_equal(smsg, dmsg) is False:

                 self.corruptedPackets += 1
                 self.fixedPackets -= 1

            iterator += 4
        return None


    def stworz_wiadomosc(self, i, list=[]):
        tab = []
        for x in range(i, i + 4, 1):
            tab.append(list[x])
        return tab


    def fivenum(self, data):
        return np.percentile(
            data, [0, 25, 50, 75, 100], interpolation='midpoint')

    def fivePoint(self, m, s):
        array = []

        with open('corrupted.csv', mode='r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                array.append(int(row[0]))

        array = self.fivenum(array)
        q = array[3] - array[1]
        data = [array[0], array[1], array[2], array[3], array[4], q, m, s]
        print(array)
        print(q)
        if self.firstRunCsv is True:
            row = ['Q1','Q2','Q3','Q4','Q5','u','m','s']
            with open('fivePoint.csv', 'w') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(row)
                writer.writerow(data)


