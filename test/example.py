import unittest

def add_numbers(a, b):
    return a + b

class TestAddNumbers(unittest.TestCase):
    def test_add_positive_numbers(self):
        self.assertEqual(add_numbers(2, 3), 5)
    
    def test_add_negative_numbers(self):
        self.assertEqual(add_numbers(-2, -3), -5)
    
    def test_add_zero(self):
        self.assertEqual(add_numbers(0, 0), 0)

if __name__ == '__main__':
    unittest.main()