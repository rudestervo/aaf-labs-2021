class Node:

    def __init__(self, data, name):

        self.left = None
        self.right = None
        self.data = data
        print("Range " + str(data) + " has been added to " + name)


    def insert(self, data, name, significative = 0):
        if self.data:
            if self.data == data:
                print("this line consist in")
            else:
                if data[significative] <= self.data[significative]:
                    if self.left is None:
                        self.left = Node(data, name)
                    else:
                        self.left.insert(data, name, significative ^ 1)
                elif data[significative] > self.data[significative]:
                    if self.right is None:
                        self.right = Node(data, name)
                    else:
                        self.right.insert(data, name, significative ^ 1)
        else:
            print("Range " + str(data) + " has been added to " + name)
            self.data = data

    def PrintTree(self, significative = 0):
        if significative != 0:
            if not (self.left) and self.right:
                print("    " * (significative - 1) + "└──", self.right.data)
                self.right.PrintTree(significative + 1)
            else:
                if self.left:
                    print("    " * (significative - 1) + "├──", self.left.data)
                    self.left.PrintTree(significative + 1)
                significative -= 1
                if self.right:
                    print("    " * (significative - 1) + "└──", self.right.data)
                    self.right.PrintTree(significative + 1)
        else:
            print(self.data)
            self.PrintTree(significative + 1)

    def e_Search(self):
        print(self.data)
        if self.right:
            self.right.e_Search()
        if self.left:
            self.left.e_Search()

    def right_Search(self, pos):
        self.Search([float(pos),float('inf')])



    def Search(self, info_for_found, significative = 0):
        if significative == 0:
            if (self.data[0] < info_for_found[0]):
                if self.right:
                    self.right.Search(info_for_found, 1)
            else:
                if (self.data[0] >= info_for_found[0]) and (self.data[1] <= info_for_found[1]):
                    print(self.data)
                if self.data[0] <= info_for_found[1]:
                    if self.right:
                        self.right.Search(info_for_found, 1)
                if self.left:
                    self.left.Search(info_for_found, 1)
        else:
            if (self.data[significative] > info_for_found[1]):
                if self.left:
                    self.left.Search(info_for_found, 1)
            else:
                if (self.data[0] >= info_for_found[0]) and (self.data[1] <= info_for_found[1]):
                    print(self.data)
                if self.right:
                    self.right.Search(info_for_found, 0)
                if self.data[1] >= info_for_found[0]:
                    if self.left:
                        self.left.Search(info_for_found, 0)

    def Intersects(self, info_for_found, significative = 0):
        if significative == 0:
            if (self.data[significative] > info_for_found[significative ^ 1]):
                if self.left:
                    self.left.Intersects(info_for_found, significative ^ 1)
            else:
                if ((self.data[0] <= info_for_found[0]) and (self.data[1] >= info_for_found[0])) or ((self.data[1] >= info_for_found[1]) and (self.data[0] <= info_for_found[1])) or ((self.data[0] >= info_for_found[0]) and (self.data[1] <= info_for_found[1])) or ((self.data[0] <= info_for_found[0]) and (self.data[1] >= info_for_found[1])):
                    print(self.data)
                if self.right:
                    self.right.Intersects(info_for_found, significative ^ 1)
                if self.left:
                    self.left.Intersects(info_for_found, significative ^ 1)
        else:
            if (self.data[significative] < info_for_found[significative ^ 1]):
                if self.right:
                    self.right.Intersects(info_for_found, significative ^ 1)
            else:
                if ((self.data[0] <= info_for_found[0]) and (self.data[1] >= info_for_found[0])) or ((self.data[1] >= info_for_found[1]) and (self.data[0] <= info_for_found[1])) or ((self.data[0] >= info_for_found[0]) and (self.data[1] <= info_for_found[1])) or ((self.data[0] <= info_for_found[0]) and (self.data[1] >= info_for_found[1])):
                    print(self.data)
                if self.right:
                    self.right.Intersects(info_for_found, significative ^ 1)
                if self.left:
                    self.left.Intersects(info_for_found, significative ^ 1)

    def Contains(self, info_for_found):
        if  self.Contains_by(info_for_found) == 1:
            print(True)
        else:
            print(False)

    def Contains_by(self, info_for_found, significative = 0):
        if (self.data[significative] == info_for_found[significative]) and (
                self.data[significative ^ 1] == info_for_found[significative ^ 1]):
            return 1
        if (info_for_found[significative] <= self.data[significative]):
            if self.left:
                if self.left.Contains_by(info_for_found, significative ^ 1) == 1:
                    return 1
        else:
            if self.right:
                if self.right.Contains_by(info_for_found, significative ^ 1) == 1:
                    return 1


        return 0
#
# tree_list = {}
# tree_list["ipt"] = []
#
#
# tree_list["ipt"] = Node([5, 10])
# tree_list["ipt"].insert([7, 15])
# tree_list["ipt"].insert([3, 7])
# tree_list["ipt"].insert([8, 10])
# tree_list["ipt"].insert([10, 20])
# tree_list["ipt"].insert([7, 15])
# tree_list["ipt"].insert([8, 16])
# tree_list["ipt"].insert([1, 4])
# tree_list["ipt"].insert([5, 8])
# tree_list["ipt"].PrintTree()
# tree_list["ipt"].Search([1, 10])
# tree_list["ipt"].Contains([8, 16])
# tree_list["ipt"].Intersects([1, 8])
# # #
# # #


# tree_list["ipt"].insert([6, 18])
# tree_list["ipt"].PrintTree()
#
#print(tree_list["ipt"].get_list())


# tree_list["ipt"] = Node([3, 4])
# tree_list["ipt"].insert([2, 7])
# tree_list["ipt"].insert([5, 8])
# tree_list["ipt"].insert([4, 6])
# tree_list["ipt"].insert([5, 10])
# tree_list["ipt"].PrintTree()
