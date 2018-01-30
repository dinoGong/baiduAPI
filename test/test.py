import unittest

class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("This setUpClass() method only called once.")
    @classmethod
    def tearDownClass(cls):
        print("This tearDownClass() method only called once too.")
    def test_a(self):
        print("a\n")
    def test_b(self):
        print("b\n")
if __name__=="__main__":
    unittest.main()
