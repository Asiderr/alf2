#!/usr/bin/env python
import os
import cv2
import numpy as np
from matplotlib import pyplot as plt


class ImageAnalysis:
    def get_images(self, name):
        self.img = cv2.imread('./images/' + name, 0)


class FrameSizeCheck:
    # Sprawdz rozmiar ramki (mean, median)
    # ramka thr adapt w klasie
    # klasa odpowadajaca za sprawdzenie poprawnosci wielkosci
    # parametru k (wielkosci ramki)
    # tu tez bedzie pobierana ramka do dalszych dzialan
    def check_k(self):
        # pobranie liczby k domyslnie 9 do mean i median
        try:
            self.k = int(input("Podaj liczbe k lub wcisnij enter by uzyskac k = 9)\n") or "9")
        except:
            # zabezpieczenie przed podaniem czegos innego niz liczba
            self.check_k()
        # k musi byc nie pazysta liczba calkowita
        x = int(self.k)
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


class Mean(FrameSizeCheck):
    # klasa odpowiadajaca za filtracje usredniajaca
    # 0.5 pkt
    def mean(self, matrix):
        # funkcja usredniajaca
        # prosba o podanie k
        self.check_k()
        # wyznaczenie rozmiaru macierzy
        matrix_size = [len(matrix[0]), len(matrix)]
        # skopiowanie macierzy do macierzy wynikowej
        # nie mozna uzyc list /.copy() bo w srodku i
        # tak beda powiazania do pierwotnej macierzy
        self.result_matrix = []
        for i in matrix:
            temp = i.copy()
            self.result_matrix.append(temp)
        # przeiterowanie obrazu w raz z numerami piksela
        for y, pixel_list in enumerate(matrix):
            for x, single_pixel in enumerate(pixel_list):
                marker = [x, y]
                # uzyskanie wierzcholkow ramki
                self.get_square_top(marker, matrix_size)
                # uzyskanie ramki
                self.get_frame(matrix)
                # wyliczenie sredniej i przypisanie wartosci piksela
                f_sum = sum(self.frame)
                self.result_matrix[y][x] = int(f_sum/len(self.frame))


class Median(FrameSizeCheck):
    # klasa odpowiadajaca za filtracje medianowa
    # 0.5 pkt
    def median(self, matrix):
        # funkcja przypisujaca mediane
        # prosba o podanie k
        self.check_k()
        # wyznaczenie rozmiaru macierzy
        matrix_size = [len(matrix[0]), len(matrix)]
        # skopiowanie macierzy do macierzy wynikowej
        self.result_matrix = []
        for i in matrix:
            temp = i.copy()
            self.result_matrix.append(temp)
        # przeiterowanie obrazu w raz z numerami piksela
        for y, pixel_list in enumerate(matrix):
            for x, single_pixel in enumerate(pixel_list):
                marker = [x, y]
                # uzyskanie wierzcholkow ramki
                self.get_square_top(marker, matrix_size)
                # uzyskanie ramki
                self.get_frame(matrix)
                # przypisanie mediany do macierzy wynikowej
                self.result_matrix[y][x] = np.median(self.frame)


class ThrConst:
    # klasa odpowiadajaca za progowanie stala wartoscia
    def check_Thr(self):
        # pobranie liczby thr domyslnie 80
        try:
            self.Thr = int(input("Podaj Thr lub wcisnij enter by uzyskac thr = 80)\n") or "80")
        except:
            # zabezpieczenie przed podaniem czegos innego niz liczba
            self.check_Thr()
        # thr musi byc mniejsze niz 256
        if(self.Thr > 255 or self.Thr < 0):
            # jesli nie bedzie powtorz pobranie liczby
            self.check_Thr()

    def thr_const(self, matrix):
        # funkcja progujaca
        # 1 pkt
        self.check_Thr()
        # skopiowanie macierzy do macierzy wynikowej
        self.result_matrix = []
        for i in matrix:
            temp = i.copy()
            self.result_matrix.append(temp)
        # progowanie
        for y, pixel_list in enumerate(matrix):
            for x, single_pixel in enumerate(pixel_list):
                # sprawdzenie czy wartosc piksela jest < rowna progowi thr
                # jesli jest to 0 jesli nie to 255
                if single_pixel <= self.Thr:
                    self.result_matrix[y][x] = 0
                else:
                    self.result_matrix[y][x] = 255


class ThrAdapt(Mean):
    # klasa odpowiadajaca za progowanie adaptacyjne
    # 2,5 pkt
    def check_C(self):
        # pobranie liczby C domyslnie 80
        try:
            self.C = int(input("Podaj C lub wcisnij enter by uzyskac C = 0)\n") or "0")
        except:
            # zabezpieczenie przed podaniem czegos innego niz liczba
            self.check_C()
        # C musi byc mniejsze niz 256
        if(self.C > 255 or self.C < 0):
            # jesli nie bedzie powtorz pobranie liczby
            self.check_C()

    def check_k(self):
        # pobranie liczby k domyslnie 9 do thr_adapt
        try:
            self.k = int(input("Podaj liczbe k lub wcisnij enter by uzyskac k = 9)\n") or "9")
        except:
            # zabezpieczenie przed podaniem czegos innego niz liczba
            self.check_k()
        # k po pierwiastkowaniu musi byc nie pazysta liczba calkowita
        # prawidlowe k np. 9, 25, 49 itd.
        x = pow(self.k, 0.5)
        if(x % 2 == 1 and x is not 1):
            self.size = x
        else:
            # jesli nie bedzie powtorz pobranie liczby
            self.check_k()

    def thr_adapt(self, matrix):
        # pobranie liczby C
        self.check_C()
        # wyliczenie srednich dla odpowiednich pikseli
        self.mean(matrix)
        # przypisanie wartosci macierzy oryginalnej do wynikowej
        self.result_matrix_thr_adapt = []
        for i in matrix:
            temp = i.copy()
            self.result_matrix_thr_adapt.append(temp)
        # przeiterowanie macierzy oryginlanej
        for y, pixel_list in enumerate(matrix):
            for x, single_pixel in enumerate(pixel_list):
                # stworzenie progu dla kazdego piksela uwzgledniajacego C
                treshold = self.result_matrix[y][x] + self.C
                # sprawdzenie czy po dodaniu C nie przekracza 255 jesli tak to przypisanie 255 do progu
                if treshold > 255:
                    treshold = 255
                # progowanie adaptacyjne
                if single_pixel < treshold:
                    self.result_matrix_thr_adapt[y][x] = 0
                else:
                    self.result_matrix_thr_adapt[y][x] = 255
