import unittest
from scripts.last_lines import last_lines

class TestAccount(unittest.TestCase):
    def setUp(self):
        self.file_path = "tests/testdata/last_lines.txt"

    def test_general(self):
        ln = last_lines(self.file_path)
        self.assertEqual(next(ln), "And this is line 3\n")
        self.assertEqual(next(ln), "This is line 2\n")
        self.assertEqual(next(ln), "This is a file\n")

    def test_limiting_chunk_size(self):
        ln = last_lines(self.file_path, 8)
        self.assertEqual(next(ln), "And this")

if __name__=="__main__":
    unittest.main()