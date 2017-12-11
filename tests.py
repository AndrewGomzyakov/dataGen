import unittest
import dataGen


class MyTestCase(unittest.TestCase):
    def test_get_age(self):
        age = dataGen.get_age(50)
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

    def test_get_email(self):
        mails = []
        mails_gen = dataGen.get_mail()
        for i in range(1000):
            mails.append(mails_gen.__next__())
        mails.sort()
        for i in range(len(mails) - 1):
            self.assertTrue(mails[i] != mails[i + 1])

    def test_get_wt(self):
        ht = dataGen.get_ht("W")
        wt = dataGen.get_wt(ht)
        imt = wt / (ht / 100) ** 2
        self.assertTrue(10 < imt and imt < 55)

    def test_get_name(self):
        man_gen = dataGen.make_persons_name("M")
        woman_gen = dataGen.make_persons_name("W")
        self.assertFalse(str(man_gen.__next__()) == str(woman_gen.__next__()))
        self.assertFalse(str(man_gen.__next__()) == str(woman_gen.__next__()))

    def test_get_surname(self):
        man_gen = dataGen.make_person_surname("M")
        woman_gen = dataGen.make_person_surname("W")
        self.assertFalse(str(man_gen.__next__()) == str(man_gen.__next__()))
        self.assertFalse(str(woman_gen.__next__()) == str(woman_gen.__next__()))


if __name__ == '__main__':
    unittest.main()
