#!/usr/bin/env python
"""
Do poprawnego dzialania programu w folderze roboczym musi znajdowac sie
folder images, a w nim pliki tekst_big.png, tekst.png, ciemna_strona_ksiezyca_brud.png
Zgodnie z zaleceniem w funkcji zapisu i pokazywania obrazow znajduje sie
argument save (funkcja img_save_n_show linia 251) ktory nalezy zmienic na True
by w folderze roboczym zostal zapisany obraz (result.png).
"""

import os
import cv2
import numpy as np
from matplotlib import pyplot as plt


class ImageAnalysis:
    def get_images(self, name):
        self.img = cv2.imread('./images/' + name, 0)


class FrameSizeCheck:
    # Sprawdz rozmiar ramki
    # 0.5 pkt
    # klasa odpowadajaca za sprawdzenie poprawnosci wielkosci
    # parametru k (wielkosci ramki)
    # tu tez bedzie pobierana ramka do dalszych dzialan
    def check_k(self):
        # pobranie liczby k domyslnie 9
        try:
            print("============================")
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
        # dla marker [2,2] k = 5
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
    # 1 pkt
    def check_Thr(self):
        # pobranie liczby thr domyslnie 80
        try:
            print("============================")
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
            print("============================")
            self.C = int(input("Podaj C lub wcisnij enter by uzyskac C = 0)\n") or "0")
        except:
            # zabezpieczenie przed podaniem czegos innego niz liczba
            self.check_C()
        # C musi byc mniejsze niz 256
        if(self.C > 255 or self.C < 0):
            # jesli nie bedzie powtorz pobranie liczby
            self.check_C()

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


def end_validation():
    # funkcja pytajaca czy urzytkownik chce zakonczyc dzialanie programu
    while(True):
        print("============================")
        end = input("\nCzy chcesz zakonczyc [y/n]:\n")
        if end == "n":
            check_end = True
            return check_end
        elif end == "y":
            check_end = False
            return check_end
        else:
            continue


def img_size_validation():
    # funkcja wyboru wielkosci obrazu dla thr_const i thr_adapt
    while(True):
        print("============================")
        print("Wybierz rozmiar obrazu\nWpisz rozmiar lub numer:")
        print("============================")
        print("1. Duzy\n2. Maly")
        size = input()
        if size == "1" or size == "Duzy" or size == "duzy" or size == "big":
            return "big"
        elif size == "2" or size == "Maly" or size == "maly" or size == "small":
            return "small"
        else:
            continue


def img_save_n_show(matrix_org, matrix_result, name, save=False):
    # funkcja zapisujaca obrazy w folderze
    # by zapisac obraz zmien argument save=True
    # 1 pkt
    fig = plt.figure()
    # sklejenie obrazow
    fig.subplots_adjust(wspace=0.000)
    fig.add_subplot(1, 2, 1)
    # wyswietlenie 1szego
    plt.imshow(matrix_org, cmap='gray')
    # wylaczenie osi
    plt.axis('off')
    # dodanie opisu
    plt.annotate("Oryginalny", (40, len(matrix_org)-20), color="r", size=8)
    fig.add_subplot(1, 2, 2)
    plt.imshow(matrix_result, cmap="gray")
    plt.axis('off')
    plt.annotate(name, (40, len(matrix_result)-20), color="r", size=8)
    # zapis obrazu jako result.png w folderze images
    if save:
        plt.savefig("./result.png", bbox_inches='tight', pad_inches=0, dpi=400)
    # wyswietlenie obrazu
    plt.show()


def main():
    # funkcja main wywolujaca filtracje i progowania
    # 1.5 pkt
    check_end = True
    while(check_end):
        print("============================")
        print("Wybierz filtracje/progowanie\nWpisz nazwe lub numer:")
        print("============================")
        print("1. Mean (Dla k = 9 ok. 30s)\n2. Median (Dla k = 9 ok. 40s)\n3. Thr_const (ok. 5s)\n4. Thr_adapt (k = 9 ok. 4 min, k = 3 ok. 1 min))")
        name = input()
        # 1. Mean
        if name == "1" or name == "Mean" or name == "mean":
            # Uzyskanie macierzy ksiezyca
            d = ImageAnalysis()
            d.get_images("ciemna_strona_ksiezyca_brud.png")
            matrix = d.img
            # Uruchomienie klasy mean odpowiadajacej za srednia
            c = Mean()
            c.mean(matrix)
            # Funkcja zapisujaca (save=True) i pokazujaca obraz wynikowy
            img_save_n_show(matrix, c.result_matrix, "Mean")
            # Sprawdzenie czy urzytkownik chce zakonczyc
            check_end = end_validation()
        # 2. Median
        if name == "2" or name == "Median" or name == "median":
            # Uzyskanie macierzy ksiezyca
            d = ImageAnalysis()
            d.get_images("ciemna_strona_ksiezyca_brud.png")
            # Uruchomienie klasy median odpowiadajacej za mediane
            matrix = d.img
            c = Median()
            c.median(matrix)
            # Funkcja zapisujaca (save=True) i pokazujaca obraz wynikowy
            img_save_n_show(matrix, c.result_matrix, "Median")
            # Sprawdzenie czy urzytkownik chce zakonczyc
            check_end = end_validation()
        # 3. Thr_const
        if name == '3' or name == "Thr const" or name == "Thr_const" or name == "thr_const" or name == "thr const":
            # Wybor rozmiaru tekstu
            size = img_size_validation()
            d = ImageAnalysis()
            if size == "big":
                d.get_images("tekst_big.png")
            else:
                d.get_images("tekst.png")
            matrix = d.img
            # Uruchomienie klasy odpowiadajacej za Thr_const
            C = ThrConst()
            C.thr_const(matrix)
            # Funkcja zapisujaca (save=True) i pokazujaca obraz wynikowy
            img_save_n_show(matrix, C.result_matrix, "Threshold")
            # Sprawdzenie czy urzytkownik chce zakonczyc
            check_end = end_validation()
        # 4. Thr_adapt
        if name == '4' or name == "Thr adapt" or name == "Thr_adapt" or name == "thr_adapt" or name == "thr adapt":
            size = img_size_validation()
            d = ImageAnalysis()
            if size == "big":
                d.get_images("tekst_big.png")
            else:
                d.get_images("tekst.png")
            matrix = d.img
            # Uruchomienie klasy odpowiadajacej za Thr_adapt
            C = ThrAdapt()
            C.thr_adapt(matrix)
            # Funkcja zapisujaca (save=True) i pokazujaca obraz wynikowy
            img_save_n_show(matrix, C.result_matrix_thr_adapt, "Adaptive Threshold")
            # Sprawdzenie czy urzytkownik chce zakonczyc
            check_end = end_validation()

main()
