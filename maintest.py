#!/usr/bin/env python

import main
import unittest
from matplotlib import pyplot as plt


class testGetFileNames(unittest.TestCase):
    def test_takingNames(self):
        c = getFileNames()
        c.sortNames()
        self.assertIn('testimg.jpg', c.fNames, msg="Blad pobierania nazw plikow")


class testImageAnalysis(unittest.TestCase):
    def test_getImages(self):
        c = imageAnalysis()
        c.getImages('testimg.jpg')
        # W komentarzu pokazanie obrazu
        """
        plt.imshow(c.img, cmap='gray', interpolation='bicubic')
        plt.show()
        """
        self.assertTrue(c.img is not None, msg="Blad pobrania obrazu")

if __name__ == '__main__':
    unittest.main()
