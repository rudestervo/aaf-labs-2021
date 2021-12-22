class Node:
    def __init__(self, data):
        self.left = None
        self.right = None
        self.data = data[1]
        self.key = [data[0]]

    def insert(self, data):
        if self.data:
            if data[1] < self.data:
                if self.left is None:
                    self.left = Node(data)
                else:
                    self.left.insert(data)
            elif data[1] > self.data:
                if self.right is None:
                    self.right = Node(data)
                else:
                    self.right.insert(data)
            else:
                self.key.append(data[0])
        else:
            self.data = data[1]
            self.key = [data[0]]

    def search(self, value):
        if self.data is None or self.data == value:
            return self.key
        elif self.data < value:
            return self.right.search(value)
        else:
            return self.left.search(value)

    def search_ind(self, value):
        if self.data is None or self.data == value:
            return self.get_ind()
        elif self.data < value:
            return self.right.search_ind(value)
        else:
            return self.left.search_ind(value)

    def PrintTree(self):
        if self.left:
            self.left.PrintTree()
        print(self.data, self.key)
        if self.right:
            self.right.PrintTree()

    def get_ind(self, arr=None):
        if arr is None:
            arr = []
        if self.left:
            self.left.get_ind(arr)
        for key in self.key:
            if key not in arr:
                arr.append(key)
        if self.right:
            self.right.get_ind(arr)
        return arr

    def greater(self, value, eq=False, arr=None):
        if arr is None:
            arr = []
        if eq:
            if self.data is not None:
                if self.data >= value:
                    for key in self.key:
                        if key not in arr:
                            arr.append(key)
                    if self.right:
                        for key in self.right.get_ind():
                            if key not in arr:
                                arr.append(key)
                    if self.left:
                        self.left.greater(value, eq, arr)
                else:
                    if self.right:
                        self.right.greater(value, eq, arr)
        else:
            if self.data is not None:
                if self.data > value:
                    for key in self.key:
                        if key not in arr:
                            arr.append(key)
                    if self.right:
                        for key in self.right.get_ind():
                            if key not in arr:
                                arr.append(key)
                    if self.left:
                        self.left.greater(value, eq, arr)
                else:
                    if self.right:
                        self.right.greater(value, eq, arr)
        return value, eq, arr

    def smaller(self, value, eq=False, arr=None):
        if arr is None:
            arr = []
        if eq:
            if self.data is not None:
                if self.data <= value:
                    for key in self.key:
                        if key not in arr:
                            arr.append(key)
                    if self.left:
                        for key in self.left.get_ind():
                            if key not in arr:
                                arr.append(key)
                    if self.right:
                        self.right.smaller(value, eq, arr)
                else:
                    if self.left:
                        self.left.smaller(value, eq, arr)
        else:
            if self.data is not None:
                if self.data < value:
                    for key in self.key:
                        if key not in arr:
                            arr.append(key)
                    if self.left:
                        for key in self.left.get_ind():
                            if key not in arr:
                                arr.append(key)
                    if self.right:
                        self.right.smaller(value,eq, arr)
                else:
                    if self.left:
                        self.left.smaller(value, eq, arr)
        return value, eq, arr

# root = Node((None,None))
# root.insert((0, "ff"))
# root.insert((1, "ff3"))
# root.insert((2, "sff3"))
# root.insert((3, "sdf"))
# root.insert((4, "dsf"))
# root.insert((5, "asd"))
# root.insert((6, "sfs"))
# root.insert((7, "sdf"))
# root.insert((8, "sd"))
# root.insert((9, "ff"))
# root.insert((10, "sda"))
# root.insert((11, "daad"))
# root.PrintTree()
# print(root.search(7))
# print(root.get_ind())
# print(root.search_ind(12))
# print(root.greater(8, True))
# print(root.smaller(9, True))


