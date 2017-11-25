import unittest
import dataGen

class MyTestCase(unittest.TestCase):
    def test_get_age(self):
        age = dataGen.get_age()
        self.assertTrue(age < 121 and age > 14)

    def test_get_sex(self):
        sum = 0
        for i in range(100000):
            if dataGen.get_sex(50) == 'W':
                sum += 1
        chance = sum / 100000
        self.assertTrue(chance > 0.48 and chance < 0.52)

    def test_get_ht(self):
        sum_woman = 0
        sum_man = 0
        for i in range(100000):
            sum_woman += dataGen.get_ht('W')
            sum_man += dataGen.get_ht('M')
        self.assertTrue(sum_man / 100000 > 177 and sum_man / 100000 < 179)
        self.assertTrue(sum_woman / 100000 > 165 and sum_woman / 100000 < 167)
