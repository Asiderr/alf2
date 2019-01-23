#!/usr/bin/env python
import os
import cv2
import numpy as np
from matplotlib import pyplot as plt


# klasa pobierająca nazy i sortujaca je
class GetFileNames:
    def sort_names(self):
        # pobranie nazwy plikow do listy
        self.f_names = os.listdir("./images")


class ImageAnalysis:
    # pobranie obrazu
    def get_images(self, name):
        self.img = cv2.imread('./images/' + name, 0)


class FrameSizeCheck:
    # Sprawdz rozmiar ramki (0,5 pkt)
    # klasa odpowadajaca za sprawdzenie poprawnosci wielkosci
    # parametru k (wielkosci ramki)
    # tu tez bedzie pobierana ramka do dalszych dzialan
    def check_k(self):
        # pobranie liczby k domyslnie 9
        try:
            self.k = int(input("Podaj liczbe k lub wcisnij enter by uzyskac k = 9)\n") or "9")
        except:
            # zabezpieczenie przed podaniem czegos innego niz liczba
            self.check_k()
        # k po spierwiastokwaniu musi dac nie parzysta liczbe calkowita
        # np. 9, 25, 49 itd.
        x = pow(self.k, 0.5)
        if(x % 2 == 1 and x is not 1):
            self.size = x
        else:
            # jesli nie bedzie powtorz pobranie liczby
            self.check_k()

    def get_frame(self, matrix):
        # funkcja pobierajaca ramke o wierzchokach z funkcji square_top
        self.frame = []
        for i in range(self.square_d[0], self.square_b[0]+1):
            for j in range(self.square_d[1], self.square_c[1]+1):
                    self.frame.append(matrix[j][i])

    def get_square_top(self, marker, matrix_size):
        # okreslenie wierzcholkow kwadratu o ramionach sqrt(k) x sqrt(k)
        # z markerem w punkcie centralnym
        # [x, y]
        # dla marker [2,2] k = 25
        # [
        #   [square_d, c, c,     c, square_b],
        #   [c,        c, c,     c, c       ],
        #   [c,        c, maker, c, c       ],
        #   [c,        c, c,     c, c       ],
        #   [square_c, c, c,     c, square_a],
        # ]
        x = int((self.size - 1)/2)
        self.square_a = [marker[0]+x, marker[1]+x]
        self.square_b = [marker[0]+x, marker[1]-x]
        self.square_c = [marker[0]-x, marker[1]+x]
        self.square_d = [marker[0]-x, marker[1]-x]
        # okreslenie rozmiarow gdy wychodzi poza matrix
        # czy jest wieksze niz rozmiar
        if self.square_a[0] > matrix_size[0]-1:
            self.square_a[0] = matrix_size[0]-1
        if self.square_a[1] > matrix_size[1]-1:
            self.square_a[1] = matrix_size[1]-1
        if self.square_b[0] > matrix_size[0]-1:
            self.square_b[0] = matrix_size[0]-1
        if self.square_c[1] > matrix_size[1]-1:
            self.square_c[1] = matrix_size[1]-1
        # czy jest mniejsze niz rozmiar
        if self.square_b[1] < 0:
            self.square_b[1] = 0
        if self.square_c[0] < 0:
            self.square_c[0] = 0
        if self.square_d[0] < 0:
            self.square_d[0] = 0
        if self.square_d[1] < 0:
            self.square_d[1] = 0
        # dla pikseli granicznych tworzy sie prostokat z oddaleniem
        # od markera maksymalnie na sqrt(k)
