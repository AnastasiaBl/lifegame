import unittest

from model import Model

class TestModel(unittest.TestCase):

    def test_glider(self):
        model = Model(5, 5)
        model.field_values = [[False, False, False, False, False],
                             [False, False, True, False, False],
                             [False, False, False, True, False],
                             [False, True, True, True, False],
                             [False, False, False, False, False]]

        expected = [[False, False, False, False, False],
                    [False, False, False, False, False],
                    [False, True, False, True, False],
                    [False, False, True, True, False],
                    [False, False, True, False, False]]

        model.step()

        self.assertEqual(model.field_values, expected)

    def test_not_stop_short_glider(self):
        model = Model(5, 5)
        model.field_values = [[False, False, False, False, False],
                             [False, False, True, False, False],
                             [False, False, False, True, False],
                             [False, True, True, True, False],
                             [False, False, False, False, False]]

        last_result = -1
        for x in range(7):
            last_result = model.step()

        self.assertEqual(last_result, False)

    def test_stop_long_game(self):
        model = Model(5, 5)
        model.field_values = [[False, False, False, False, False],
                             [False, False, True, False, False],
                             [False, False, False, True, False],
                             [False, True, True, True, False],
                             [False, False, False, False, False]]

        last_result = -1
        for x in range(50):
            last_result = model.step()

        self.assertEqual(last_result, True)

    def test_long_periodic_game(self):
        model = Model(6, 6)
        model.field_values = [[False, False, False, False, False, False],
                              [False, False, False, True, False, False],
                              [False, True, False, False, True, False],
                              [False, True, False, False, True, False],
                              [False, False, True, False, False, False],
                              [False, False, False, False, False, False]]

        expected = [[False, False, False, False, False, False],
                    [False, False, False, True, False, False],
                    [False, True, False, False, True, False],
                    [False, True, False, False, True, False],
                    [False, False, True, False, False, False],
                    [False, False, False, False, False, False]]

        for x in range(500):
            model.step()

        self.assertEqual(model.field_values, expected)

    def test_clear_history(self):
        model = Model(5, 5)
        model.field_values = [[False, False, False, False, False],
                             [False, False, True, False, False],
                             [False, False, True, False, False],
                             [False, False, True, False, False],
                             [False, False, False, False, False]]

        for x in range(50):
            model.step()

        model.clear_history()
        last_result = model.step()

        self.assertEqual(last_result, False)

if __name__ == '__main__':
    unittest.main()
