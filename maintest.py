#!/usr/bin/env python

import main
import unittest
from matplotlib import pyplot as plt


class TestImageAnalysis(unittest.TestCase):
    def test_get_images(self):
        c = main.ImageAnalysis()
        c.get_images('testimg.jpg')
        # W komentarzu pokazanie obrazu
        """
        plt.imshow(c.img, cmap='gray', interpolation='bicubic')
        plt.show()
        """
        self.assertTrue(c.img is not None, msg="Blad pobrania obrazu")


class TestFrameSizeCheck(unittest.TestCase):
    def test_get_square_top_edge(self):
        marker = [0, 0]
        matrix_size = [5, 5]
        c = main.FrameSizeCheck()
        c.size = 5
        c.get_square_top(marker, matrix_size)
        self.assertEqual(c.square_a, [2, 2],
                         msg="Blad wyznaczania wierzcholka square_a")
        self.assertEqual(c.square_b, [2, 0],
                         msg="Blad wyznaczania wierzcholka square_b")
        self.assertEqual(c.square_c, [0, 2],
                         msg="Blad wyznaczania wierzcholka square_c")
        self.assertEqual(c.square_d, [0, 0],
                         msg="Blad wyznaczania wierzcholka square_d")

    def test_get_square_top_inside(self):
        marker = [2, 2]
        matrix_size = [5, 5]
        c = main.FrameSizeCheck()
        c.size = 5
        c.get_square_top(marker, matrix_size)
        self.assertEqual(c.square_a, [4, 4],
                         msg="Blad wyznaczania wierzcholka square_a")
        self.assertEqual(c.square_b, [4, 0],
                         msg="Blad wyznaczania wierzcholka square_b")
        self.assertEqual(c.square_c, [0, 4],
                         msg="Blad wyznaczania wierzcholka square_c")
        self.assertEqual(c.square_d, [0, 0],
                         msg="Blad wyznaczania wierzcholka square_d")

    def test_get_frame_close_to_edge(self):
        marker = [1, 2]
        matrix = [
            [5, 5, 5, 5, 1, 1],
            [5, 5, 5, 5, 1, 1],
            [5, 5, 5, 5, 1, 1],
            [5, 5, 5, 5, 1, 1],
            [5, 5, 5, 5, 1, 1],
        ]
        matrix_size = [len(matrix[0]), len(matrix)]
        c = main.FrameSizeCheck()
        c.size = 5
        c.get_square_top(marker, matrix_size)
        c.get_frame(matrix)
        self.assertEqual(
            c.frame,
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
            msg="Blad pobierania ramki blisko krawedzi"
            )

    def test_get_frame_inside(self):
        marker = [2, 2]
        matrix = [
            [1, 1, 1, 1, 1, 1],
            [1, 5, 5, 5, 1, 1],
            [1, 5, 5, 5, 1, 1],
            [1, 5, 5, 5, 1, 1],
            [1, 1, 1, 1, 1, 1],
        ]
        matrix_size = [len(matrix[0]), len(matrix)]
        c = main.FrameSizeCheck()
        c.size = 3
        c.get_square_top(marker, matrix_size)
        c.get_frame(matrix)
        self.assertEqual(
            c.frame,
            [5, 5, 5, 5, 5, 5, 5, 5, 5],
            msg="Blad pobierania ramki blisko krawedzi"
            )

    def test_get_frame_edge(self):
        marker = [5, 2]
        matrix = [
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 5, 5],
            [1, 1, 1, 1, 5, 5],
            [1, 1, 1, 1, 5, 5],
            [1, 1, 1, 1, 1, 1],
        ]
        matrix_size = [len(matrix[0]), len(matrix)]
        c = main.FrameSizeCheck()
        c.size = 3
        c.get_square_top(marker, matrix_size)
        c.get_frame(matrix)
        self.assertEqual(
            c.frame,
            [5, 5, 5, 5, 5, 5],
            msg="Blad pobierania ramki blisko krawedzi"
            )

# sprawdzenie k
"""
    # Klasa testowa sprawdzenia ramki
    def test_check_k(self):
        c = main.FrameSizeCheck()
        c.check_k()
        self.assertEqual(c.size, 3, msg="Blad wyznaczania k")
        c.check_k()
        self.assertEqual(c.size, 5, msg="Blad wyznaczania k")
"""
# srednia

"""
class TestMean(unittest.TestCase):
    def test_mean(self):
        c = main.Mean()
        matrix = [
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 5, 5],
            [1, 1, 1, 1, 5, 5],
            [1, 1, 1, 1, 5, 5],
            [1, 1, 1, 1, 1, 1],
        ]
        c.mean(matrix)
        # dla k = 3
        self.assertEqual(c.result_matrix[2][4], 3, msg="Blad wyznaczania sredniej")

    def test_mean_moon(self):
        d = main.ImageAnalysis()
        d.get_images("ciemna_strona_ksiezyca_brud.png")
        matrix = d.img
        c = main.Mean()
        c.mean(matrix)
        plt.imshow(c.result_matrix, cmap='gray')
        plt.show()

"""
# mediana

"""
class TestMedian(unittest.TestCase):
    def test_median(self):
        c = main.Median()
        matrix = [
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 5, 5],
            [1, 1, 1, 1, 5, 5],
            [1, 1, 1, 1, 5, 5],
            [1, 1, 1, 1, 1, 1],
        ]
        c.median(matrix)
        # dla k = 3
        self.assertEqual(c.result_matrix[2][4], 5, msg="Blad wyznaczania mediany")

    def test_median_moon(self):
        d = main.ImageAnalysis()
        d.get_images("ciemna_strona_ksiezyca_brud.png")
        matrix = d.img
        c = main.Median()
        c.median(matrix)
        plt.imshow(c.result_matrix, cmap='gray')
        plt.show()
"""

# thr const
"""
class TestThrConst(unittest.TestCase):
    def test_chcek_Thr(self):
        c = main.ThrConst()
        c.check_Thr()
        self.assertEqual(c.Thr, 80, msg="Blad Thr (enter)")
        c.check_Thr()
        self.assertEqual(c.Thr, 90, msg="Blad Thr (wprowadzanie)")

    def test_thr_const(self):
        matrix = [
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 5, 5],
            [1, 1, 1, 1, 5, 5],
            [1, 1, 1, 1, 5, 5],
            [1, 1, 1, 1, 1, 1],
        ]
        c = main.ThrConst()
        c.thr_const(matrix)
        # thr = 2 lub 3 lub 4
        self.assertEqual(
            c.result_matrix,
            [
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 255, 255],
                [0, 0, 0, 0, 255, 255],
                [0, 0, 0, 0, 255, 255],
                [0, 0, 0, 0, 0, 0],
            ],
            msg="Blad progowania Thr"
        )

    def test_thr_const_tekst(self):
        d = main.ImageAnalysis()
        d.get_images("tekst_big.png")
        matrix = d.img
        c = main.ThrConst()
        c.thr_const(d.img)
        plt.imshow(c.result_matrix, cmap='gray')
        plt.show()
"""
# THR_adapt


class TestThrAdapt(unittest.TestCase):
    def test_check_C(self):
        c = main.ThrAdapt()
        c.check_C()
        # enter
        self.assertEqual(c.C, 0, msg="Blad wprowadzania C enter")
        c.check_C()
        # 90
        self.assertEqual(c.C, 90, msg="Blad wprowadzania C (wprowadzanie")

    def test_thr_adapt(self):
        matrix = [
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 5, 5],
            [1, 1, 1, 1, 5, 5],
            [1, 1, 1, 1, 5, 5],
            [1, 1, 1, 1, 1, 1],
        ]
        c = main.ThrAdapt()
        c.thr_adapt(matrix)
        self.assertEqual(
            c.result_matrix_thr_adapt,
            [
                [255, 255, 255, 255, 0, 0],
                [255, 255, 255, 255, 255, 255],
                [255, 255, 255, 0, 255, 255],
                [255, 255, 255, 255, 255, 255],
                [255, 255, 255, 255, 0, 0],
            ],
            msg="Blad progowania Thr"
        )

    def test_thr_adapt_img(self):
        d = main.ImageAnalysis()
        d.get_images("tekst_big.png")
        matrix = d.img
        c = main.ThrAdapt()
        c.thr_adapt(matrix)
        plt.imshow(c.result_matrix_thr_adapt, cmap='gray')
        plt.show()


if __name__ == '__main__':
    unittest.main()
