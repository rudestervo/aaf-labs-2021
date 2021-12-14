import unittest
from RTree import *
import random

n = 1000


class MyTestCase(unittest.TestCase):

    def test_insert(self):
        t = RTree()
        points = []
        for i in range(n):
            a = random.randint(-100, 100)
            b = random.randrange(-100, 100)
            if Point(a, b) not in points:
                points.append(Point(a, b))
        # def prt_lst(lst):
        #     print('[', end='')
        #     for i in lst:
        #         print(i, end=',')
        #     print(']')
        #
        # prt_lst(points)
        for i in points:
            # if i==Point(64,4):
            #     t.prt()
            #     print()
            t.insert(i)
        a = True
        for i in points:
            # print(t.search(i), i)
            a = a and t.search(i)
        self.assertEqual(a, True)

    def test_delete(self):
        t = RTree()
        points = []
        for i in range(n):
            a = random.randint(-100, 100)
            b = random.randrange(-100, 100)
            if Point(a, b) not in points:
                points.append(Point(a, b))
        for i in points:
            # if i==Point(64,4):
            #     t.prt()
            #     print()
            t.insert(i)
        # deletion
        k = 500
        deleted = []
        # deletd=[Point(82,-85),Point(-40,-48),Point(-64,54),Point(-77,36),Point(30,59),Point(-64,-37),Point(100,10),Point(22,97),Point(-67,-47),Point(-54,-65),Point(54,24),Point(86,-70),Point(22,94),Point(58,2),Point(-81,97),Point(-50,93),Point(-19,-80),Point(70,35),Point(-24,66),Point(94,-70),Point(-3,-39),Point(-96,-77),Point(65,-66),Point(-18,61),Point(24,-28),Point(12,-19),Point(-84,-1),Point(40,40),Point(24,68),Point(-58,-86),Point(48,88),Point(46,70),Point(43,88),Point(36,26),Point(-31,26),Point(60,-92),Point(-73,-64),Point(-27,-32),Point(97,42),Point(83,15),Point(-17,-84),Point(80,10),Point(-54,-72),Point(-42,-64),Point(-76,-49),Point(27,68),Point(-57,-84),Point(-73,-65),Point(77,38),Point(-56,-81),Point(-26,-76),Point(-83,-7),Point(-44,-52),Point(-71,81),Point(90,46),Point(72,93),Point(64,74),Point(-63,51),Point(2,-3),Point(16,-74),Point(72,44),Point(95,-92),Point(30,-37),Point(-64,60),Point(29,-13),Point(-92,-39),Point(49,73),Point(39,-75),Point(85,44),Point(95,92),Point(1,-46),Point(49,49),Point(57,-34),Point(-36,50),Point(34,-77),Point(-72,-37),Point(70,-45),Point(-10,-27),Point(72,-58),Point(21,70),Point(-98,-14),Point(36,87),Point(-29,-73),Point(-85,-93),Point(-10,-75),Point(38,31),Point(5,-57),Point(31,-50),Point(93,23),Point(65,-17),Point(-66,-40),Point(44,27),Point(67,23),Point(23,-40),Point(-1,97),Point(22,91),Point(-100,-27),Point(-82,76),Point(35,5),Point(57,-73),]
        # for i in deletd:
        #     point.remove(i)
        #     t.delete(i)

        for i in range(k):
            p = points.pop(random.randint(0, (len(points) - 1)))
            # p = point.pop(1)
            deleted.append(p)
            t.delete(p)
        a = True
        for i in points:
            # print(t.search(i), i)
            a = a and t.search(i)
        self.assertEqual(a, True)
        a = False
        for i in deleted:
            # print(t.search(i), i)
            a = a or t.search(i)
        self.assertEqual(a, False)  # add assertion here

    def test_search_all(self):
        t = RTree()
        points = []
        for i in range(n):
            a = random.randint(-100, 100)
            b = random.randrange(-100, 100)
            if (a, b) not in points:
                points.append((a, b))
        for i in points:
            # if i==Point(64,4):
            #     t.prt()
            #     print()
            t.insert(Point(*i))
        expected =points
        actual = [i.to_cortege() for i in t.search_by_condition()]

        self.assertEqual(set(actual), set(expected))

    def test_search_into(self):
        t = RTree()
        points = [] #[(84, 50), (80, 16), (-48, -97), (91, -88), (-89, -100), (95, -14), (91, -49), (-79, -44), (-79, -53), (-53, -27), (21, -85), (63, -89), (23, 13), (6, 75), (47, -26), (-46, -47), (-24, -67), (-65, -91), (-98, -39), (86, -5)]
        for i in range(n):
            a = random.randint(-100, 100)
            b = random.randrange(-100, 100)
            if (a, b) not in points:
                points.append((a, b))
        for i in points:
            # if i==Point(64,4):
            #     t.prt()
            #     print()
            t.insert(Point(*i))
        rect = Rect(Point(-50, -50), Point(50, 50))
        expected = [i for i in points if Point(*i) in rect]
        actual = [i.to_cortege() for i in t.search_by_condition(rect)]
        self.assertEqual(set(actual), set(expected))

    def test_search_left(self):
        t = RTree()
        points = []
        for i in range(n):
            a = random.randint(-100, 100)
            b = random.randrange(-100, 100)
            if (a, b) not in points:
                points.append((a, b))
        for i in points:
            # if i==Point(64,4):
            #     t.prt()
            #     print()
            t.insert(Point(*i))
        x = random.randint(-100, 100)
        expected = [i for i in points if i[0] < x]
        actual = [i.to_cortege() for i in t.search_by_condition(x)]

        self.assertEqual(set(actual), set(expected))

    def test_search_near(self):
        t = RTree()
        points = []
        for i in range(n):
            a = random.randint(-100, 100)
            b = random.randrange(-100, 100)
            if (a, b) not in points:
                points.append((a, b))
        for i in points:
            # if i==Point(64,4):
            #     t.prt()
            #     print()
            t.insert(Point(*i))
        near =Point( random.randint(-100, 100), random.randrange(-100, 100))
        expected=[]
        for i in points:
            if not expected:
                expected.append(i)
            elif Point(*i).distance(near)<near.distance(Point(*expected[0])):
                expected.clear()
                expected.append(i)
            elif Point(*i).distance(near) == near.distance(Point(*expected[0])):
                expected.append(i)
        actual=[i.to_cortege() for i in t.search_by_condition(near)]
        self.assertEqual(set(expected),set(actual))



if __name__ == '__main__':
    unittest.main()
