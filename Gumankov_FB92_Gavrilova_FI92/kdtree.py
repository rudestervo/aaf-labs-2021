from node import Node


class KDTree:

    def __init__(self, Name=None, left=None, right=None, level=None, Node=None):
        self.name = Name
        self.right = right
        self.left = left
        self.node = Node
        self.level = level

    def addNode(self, x, y):
        if self.node is None:
            self.node = Node(x, y)
            return

        if (self.node.X <= x and self.level % 2 == 0) or (self.node.Y <= y and self.level % 2 == 1):
            if self.right is None:
                self.right = KDTree(self.name, None, None, self.level+1, Node(x, y))
            else:
                self.right.addNode(x, y)
        else:
            if self.left is None:
                self.left = KDTree(self.name, None, None, self.level+1, Node(x, y))
            else:
                self.left.addNode(x, y)

    def printTree(self, lr, level, space):
        check = 1
        deletespace = -1
        output = ""

        for el in space:
            if el+1 < level and lr != 0:
                for i in range(check, el+1):
                    output += " "
                output += "│ "
                check = el+2
            elif el+1 == level and lr==2:
                deletespace = space.index(el)

        if deletespace >= 0:
            space.pop(deletespace)
        for i in range(check, level):
            output += " "
        if lr == 1:
            output += "├─"
        if lr == 2:
            output += "└─";
        if self.node is not None:
            print(f"{output}({self.node.X}, {self.node.Y})")
        if self.left is not None:
            if (self.left.left is not None or self.left.right is not None) and self.right is not None:
                space.append(level)
            if self.right is None: #
                self.left.printTree(2, (level + 1), space) #
            else:  #
                self.left.printTree(1, (level + 1), space) #left that call of printTree() instead of if case(marked higher) to see left and right trees better

        if self.right is not None:
            self.right.printTree(2, (level + 1), space)

    def contains(self, x, y):
        if self.node.X == x and self.node.Y == y:
            return True
        if (self.node.X <= x and self.level % 2 == 0) or (self.node.Y <= y and self.level % 2 == 1):
            if self.right is not None:
                return self.right.contains(x,y)

        else:
            if self.left is not None:
               return self.left.contains(x, y)

    def inside(self, x1, y1, x2, y2):
        if x1 <= self.node.X <= x2 and y1 <= self.node.Y <= y2:
            print(f"({self.node.X}, {self.node.Y})")
        if (self.level % 2 == 0 and self.node.X <= x1) or (self.level % 2 == 1 and self.node.Y <= y1):
            if self.right is not None:
                self.right.inside(x1, y1, x2, y2)
        elif (self.level % 2 == 0 and self.node.X > x2) or (self.level % 2 == 1 and self.node.Y > y2):
            if self.left is not None:
                self.left.inside(x1, y1, x2, y2)
        else:
            if self.right is not None:
                self.right.inside(x1, y1, x2, y2)
            if self.left is not None:
                self.left.inside(x1, y1, x2, y2)

    def above(self, y):

        if self.node.Y > y:
            print(f"({self.node.X}, {self.node.Y})")
        if self.level % 2 == 0:
            if self.right is not None:
                self.right.above(y)
            if self.left is not None:
                self.left.above(y)
        else:
            if self.node.Y <= y:
                if self.right is not None:
                    self.right.above(y)
            else:
                if self.left is not None:
                    self.left.above(y)
                if self.right is not None:
                    self.right.above(y)

    def nn(self, x, y, lst, dist=None):
        if dist is None:
            dist = self.dist(self.node.X, self.node.Y, x, y)
            lst.append([self.node.X, self.node.Y])
        else:
            tempdist = self.dist(self.node.X, self.node.Y, x, y)
            if tempdist < dist:
                lst.clear()
                lst.append([self.node.X, self.node.Y])
                dist = tempdist
            elif tempdist == dist:
                lst.append([self.node.X, self.node.Y])
        if self.right is not None:
            self.right.nn(x, y, lst, dist)
        if self.left is not None:
            self.left.nn(x, y, lst, dist)



        return lst

    def dist(self, x1, y1, x2, y2):
        return float(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)
