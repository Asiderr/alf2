#!/usr/bin/env python

import main
import unittest
from matplotlib import pyplot as plt


class TestGetFileNames(unittest.TestCase):
    def test_taking_names(self):
        c = main.GetFileNames()
        c.sort_names()
        self.assertIn('testimg.jpg', c.f_names, msg="Blad pobierania nazw plikow")


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


"""
    # Klasa testowa sprawdzenia ramki
    def test_check_k(self):
        c = main.FrameSizeCheck()
        c.check_k()
        self.assertEqual(c.size, 3, msg="Blad wyznaczania k")
        c.check_k()
        self.assertEqual(c.size, 5, msg="Blad wyznaczania k")
"""

if __name__ == '__main__':
    unittest.main()
