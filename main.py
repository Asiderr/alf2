#!/usr/bin/env python
import os
import cv2
import numpy as np
from math import log2
from matplotlib import pyplot as plt


# klasa pobierająca nazy i sortujaca je
class getFileNames:
    def sortNames(self):
        # pobranie nazwy plików do listy
        self.fNames = os.listdir("./images")


class imageAnalysis:
    # pobranie obrazu
    def getImages(self, name):
        self.img = cv2.imread('./images/' + name, 0)
