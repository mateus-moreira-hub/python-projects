from math import sqrt
import unittest
from scripts.computed_property import computed_property

class Vector():
    def __init__(self, x, y, z, color=None) -> None:
        self.x, self.y, self.z = x, y, z
        self.color = color
        self.execution_count = 0

    @computed_property("x", "y", "z", "w")
    def magnitude(self):
        "Returns the magnitude of the vector"
        self.execution_count += 1
        return sqrt(self.x**2 + self.y**2 + self.z**2)

class TestAccount(unittest.TestCase):
    def test_general(self):
        v = Vector(9, 2, 6)
        self.assertEqual((v.magnitude, v.execution_count), (11.0, 1))
        v.color = "red"
        self.assertEqual((v.magnitude, v.execution_count), (11.0, 1))
        v.y = 18
        self.assertEqual((v.magnitude, v.execution_count), (21.0, 2))

if __name__=="__main__":
    unittest.main()