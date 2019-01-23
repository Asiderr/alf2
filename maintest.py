#!/usr/bin/env python

import main
import unittest


class testGetFileNames(unittest.TestCase):
    def test_takingNames(self):
        c = getFileNames()
        c.sortNames()
        self.assertIn('testimg.jpg', c.fNames, msg="Blad pobierania nazw plikow")

    def test_sortName(self):
        c = getFileNames()
        c.sortNames()
        self.assertFalse(len(c.sortedFl) is 0, msg="Blad - pusta lista")
        for i in range(0, len(c.sortedFl)):
            if i is (len(c.sortedFl) - 1):
                pass
            else:
                self.assertTrue(c.sortedFl[i] <= c.sortedFl[i+1], msg="Blad sortowania nazw")


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

    def test_matrixSum(self):
        c = imageAnalysis()
        matrix = [
            [0, 0, 0, 1, 0],
            [0, 0, 1, 0, 0],
            [0, 2, 0, 0, 0]
        ]
        c.matrixSum(matrix)
        self.assertEqual(c.NM_sum, 4, msg="Blad sumowania macierzy")
        self.assertEqual(c.productNM, 15, msg="Blad wyznaczania wielkosci macierzy")

    def test_matrixAvg(self):
        c = imageAnalysis()
        c.matrixAvg(15, 15)
        self.assertEqual(c.avg, 1, msg="Blad obliczania sredniej")

    def test_matrixVariance(self):
        c = imageAnalysis()
        matrix = [
            [0, 0, 0, 5, 0],
            [0, 0, 5, 0, 0],
            [0, 5, 0, 0, 0]
        ]
        c.matrixVariance(matrix, 1)
        self.assertEqual(c.variance, 4, msg="Blad wyliczania wariancji")

    def test_matrixStd(self):
        c = imageAnalysis()
        c.matrixStd(4)
        self.assertEqual(c.std, 2, msg="Blad wyliczania odchylenia standardowego")

    def test_matrixHistogram(self):
        c = imageAnalysis()
        matrix = [
            [0, 0, 0, 5, 0],
            [0, 0, 5, 0, 0],
            [0, 5, 0, 0, 0]
        ]
        c.matrixHistogram(matrix)
        self.assertEqual(c.histogram[0], 12, msg="Blad wyznaczania histogramu")

    def test_imgEntropy_not_zero(self):
        c = imageAnalysis()
        val_hist = []
        for i in range(0, 256):
            val_hist.append(1/256)
        c.imgEntropy(val_hist)
        self.assertEqual(c.entropy, 8, msg="Blad wyznaczania entropii dla wartości")

    def test_imgEntropy_zero(self):
        c = imageAnalysis()
        val_hist = []
        for i in range(0, 256):
            val_hist.append(0)
        val_hist[0] = 1
        c.imgEntropy(val_hist)
        self.assertEqual(c.entropy, 0, msg="Blad wyznaczania entropii dla zer")


class test_plots(unittest.TestCase):
    def test_figure1(self):
        pl = plots()
        nhist = []
        cnhist = []
        for i in range(0, 256):
            nhist.append(1/256)
        for i in range(0, 6):
            cnhist.append(nhist)
        pl.figure1(cnhist, 6)

    def test_figure2(self):
        pl = plots()
        avg = [2, 2, 2, 2, 2, 2]
        std = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
        ent = [6, 6, 6, 6, 6, 6]
        rough = [0, 4, 10, 12, 15, 18]
        pl.figure2(avg, std, ent, rough)


class testMain(unittest.TestCase):
    def test_main(self):
        test = main()
        self.assertIn([163.19363418367345, 45.64993571527012, 7.205314713880184],
                      test, msg="Blad listy wynikowej")


if __name__ == '__main__':
    unittest.main()
