class Point:
    def __str__(self):
        return 'Point(' + str(self.x) + ',' + str(self.y) + ')'

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, point):
        return point != None and self.x == point.x and self.y == point.y

    def distance(self, point):
        return ((self.x - point.x) ** 2 + (self.y - point.y) ** 2) ** 0.5

    def to_cortege(self):
        return self.x, self.y


class Rect:
    def __contains__(self, item: Point):
        return self.min_x <= item.x <= self.max_x and self.min_y <= item.y <= self.max_y

    def __init__(self, a, b):
        if isinstance(a, Point):
            self.init_by_point(a, b)
        else:
            self.init_by_rect(a, b)

    def init_by_point(self, point1: Point, point2: Point):
        if point1.x < point2.x:
            self.min_x = point1.x
            self.max_x = point2.x
        else:
            self.min_x = point2.x
            self.max_x = point1.x
        if point1.y < point2.y:
            self.min_y = point1.y
            self.max_y = point2.y
        else:
            self.min_y = point2.y
            self.max_y = point1.y

    def init_by_rect(self, rect1, rect2):
        self.min_x = min(rect1.min_x, rect2.min_x)
        self.max_x = max(rect1.max_x, rect2.max_x)
        self.min_y = min(rect1.min_y, rect2.min_y)
        self.max_y = max(rect1.max_y, rect2.max_y)

    def is_intersected(self, rect):
        return not (self.max_y<rect.min_y or self.min_y>rect.max_y or self.max_x<rect.min_x or self.min_x>rect.max_x)


class RTree:
    def __init__(self):
        self.root = None

    def insert(self, point: Point):
        if self.root == None:
            self.root = RTreeLeaf(point)
        elif not self.search(point):
            if point in self.root:
                self.root = self.root.insert(point)
            else:
                self.root = self.root.extend(point)

    def search(self, point):
        if point in self.root.rect:
            return self.root.search(point)
        return False

    def search_by_condition(self,param=None):
        if self.root is None:
            return []
        set_of_points=[]
        if param is None:
            self.root.search_all(set_of_points)
            return set_of_points
        elif isinstance(param, int):
            self.root.search_left(param,set_of_points)
            return set_of_points
        elif isinstance(param, Rect):
            self.root.search_into(param,set_of_points)
            return set_of_points
        elif isinstance(param,Point):
            self.root.search_near(param,set_of_points)
            return set_of_points
        else:
            return []

    def delete(self, point: Point):
        if not self.search(point):
            return False
        self.root.delete(point)
        return True

    def prt(self):
        if self.root == None:
            print("Empty tree")
        else:
            self.root.prt('')


class RTreeNode:

    def prt(self, place: str):
        if place == '':
            print(f'[({self.rect.min_x},{self.rect.min_y}),({self.rect.max_x},{self.rect.max_y})]')
            if self.right == None:
                self.left.prt('└── ')
            else:
                self.left.prt('├── ')
                self.right.prt('└── ')
            return
        print(place + f'[({self.rect.min_x},{self.rect.min_y}),({self.rect.max_x},{self.rect.max_y})]')
        new_place = place[0:-4] + '│' if place[-4:] == '├── ' else place[0:-4] + ' '
        if self.right == None:
            self.left.prt(new_place + '   └── ')
        else:
            self.left.prt(new_place + '   ├── ')
            self.right.prt(new_place + '   └── ')

    def __init__(self, left, right=None):
        self.left = left
        self.right = right
        if self.right == None:
            self.rect = self.left.rect
        else:
            self.rect = Rect(self.left.rect, self.right.rect)

    def __contains__(self, item):
        return item in self.rect

    def is_full(self):
        return self.left != None and self.right != None

    def insert(self, point: Point):
        if not self.left.is_full():
            self.left = self.left.extend(point)
        elif self.right == None:
            self.right = RTreeLeaf(point)
        elif point in self.left:
            self.left = self.left.insert(point)
        elif point in self.right:
            self.right = self.right.insert(point)
        elif distanse_between_point_and_rect(point, self.left.rect) < distanse_between_point_and_rect(point,
                                                                                                      self.right.rect):
            self.right, self.left = self.left, self.right
            self.right = self.right.extend(point)
        else:
            self.right = self.right.extend(point)
        self.rect = Rect(self.left.rect, self.right.rect)
        return self

    def extend(self, point: Point):
        if not self.left.is_full():
            self.left = self.left.extend(point)
        elif self.right == None:
            self.right = RTreeLeaf(point)
        else:
            if distanse_between_point_and_rect(point, self.left.rect) < distanse_between_point_and_rect(point,
                                                                                                        self.right.rect):
                self.right, self.left = self.left, self.right
            self.right = self.right.extend(point)
        self.rect = Rect(self.left.rect, self.right.rect)
        return self

    def search(self, point: Point):
        a = False
        if point in self.left:
            a = a or self.left.search(point)
        if self.right != None and point in self.right:
            a = a or self.right.search(point)
        return a

    def search_all(self, ls: list):
        self.left.search_all(ls)
        if self.right!=None:
            self.right.search_all(ls)

    def search_left(self, x: int, ls: list):
        if self.left.rect.min_x < x:
            self.left.search_left(x,ls)
        if self.right != None and self.right.rect.min_x < x:
            self.right.search_left(x,ls)

    def search_near(self, point: Point, ls: list):
        if self.right==None:
            self.left.search_near(point, ls)
        else:
            self.left.search_near(point, ls)
            self.right.search_near(point, ls)


    def search_into(self, rect:Rect, ls:list):
        if self.left.rect.is_intersected(rect):
            self.left.search_into(rect, ls)
        if self.right!=None and self.right.rect.is_intersected(rect):
            self.right.search_into(rect, ls)


    def delete(self, point: Point):
        if self.right != None:
            if point in self.right:
                self.right = self.right.delete(point)
            if point in self.left:
                self.right, self.left = self.left, self.right
                self.right = self.right.delete(point)
            if self.right == None:
                return self.left
            if self.left == None:
                return self.right
            if isinstance(self.right, RTreeLeaf) and isinstance(self.left, RTreeLeaf):
                if self.left.point2 == None and self.right.point2 == None:
                    return RTreeLeaf(self.left.point1, self.right.point1)
            self.rect = Rect(self.left.rect, self.right.rect)
            return self
        else:
            return self.left.delete(point)


class RTreeLeaf:
    def is_full(self):
        return self.point1 != None and self.point2 != None

    def prt(self, place):
        print(place + f'[({self.rect.min_x},{self.rect.min_y}),({self.rect.max_x},{self.rect.max_y})]')
        new_place = place[0:-4] + '│' if place[-4:] == '├── ' else place[0:-4] + ' '
        if self.point2 == None:
            print(new_place + f'   └── {self.point1}')
        else:
            print(new_place + f'   ├── {self.point1}')
            print(new_place + f'   └── {self.point2}')

    def __init__(self, point1, point2=None):
        self.point1 = point1
        self.point2 = point2
        if point2 == None:
            self.rect = Rect(point1, point1)
        else:
            self.rect = Rect(point1, point2)

    def __contains__(self, item):
        return item in self.rect

    def insert(self, point):
        return self.extend(point)

    def extend(self, point: Point):
        if self.point2 == None:
            self.point2 = point
            self.rect = Rect(self.point1, self.point2)
            return self
        if point.distance(self.point1) < self.point1.distance(self.point2):
            if point.distance(self.point2) < point.distance(self.point1):
                return RTreeNode(RTreeLeaf(point, self.point2), RTreeLeaf(self.point1))
            return RTreeNode(RTreeLeaf(point, self.point1), RTreeLeaf(self.point2))
        if point.distance(self.point2) < self.point1.distance(self.point2):
            return RTreeNode(RTreeLeaf(point, self.point2), RTreeLeaf(self.point1))
        return RTreeNode(self, RTreeLeaf(point))

    def search(self, point: Point):
        return point == self.point1 or point == self.point2

    def search_all(self, ls: list):
        if self.point2!= None:
            ls.append(self.point2)
        ls.append(self.point1)

    def search_left(self, x: int, ls:list):
        if self.point1.x < x:
            ls.append(self.point1)
        if self.point2!=None and self.point2.x < x:
            ls.append(self.point2)

    def search_near(self, nearest: Point, ls:list):
        if not ls:
            ls.append(self.point1)
        else:
            if self.point1.distance(nearest) < ls[0].distance(nearest):
                ls.clear()
                ls.append(self.point1)
            elif self.point1.distance(nearest) == ls[0].distance(nearest):
                ls.append(self.point1)
        if self.point2 != None:
            if self.point2.distance(nearest) < ls[0].distance(nearest):
                ls.clear()
                ls.append(self.point2)
            elif self.point2.distance(nearest) == ls[0].distance(nearest):
                ls.append(self.point2)

    def search_into(self, rect: Rect, ls:list):
        if self.point2!=None and self.point2 in rect:
            ls.append(self.point2)
        if self.point1 in rect:
            ls.append(self.point1)


    def delete(self, point):
        if self.point2 != None:
            if self.point1 == point:
                self.point2, self.point1 = self.point1, self.point2
                self.point2 = None
            elif self.point2 == point:
                self.point2 = None
            return self
        elif self.point1 == point:
            return None
        else:
            return self


def distanse_between_point_and_rect(point: Point, rect: Rect):
    if point in rect:
        return 0
    if (rect.min_x <= point.x) and (point.x  <= rect.max_x):
        return min(abs(rect.min_y-point.y),abs(rect.max_y-point.y))
    if (rect.min_y <= point.y) and (point.y  <= rect.max_y):
        return min(abs(rect.min_x-point.x),abs(rect.max_x-point.x))
    return (min(rect.min_x - point.x, rect.max_x - point.x) ** 2 +
            min(rect.min_x - point.x, rect.max_x - point.x) ** 2) ** 0.5
