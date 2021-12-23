# Binary tree
# Binary tree
class Row:
    def __init__(self, values, index_value):
        self.value = values
        self.index_value = index_value
    
    def disp(self):
        return self.value

class Node:
    def __init__(self, row):
        self.value = row
        self.left = None
        self.right = None

class Tree:
    def __init__(self, row_init):
        self.root = Node(row_init)
        self.size = 0
    

    def get_root(self):
        return self.root


    def add(self, row):
        if self.root is None:
            self.root = Node(row)
        else:
            self.__add(row, self.root)


    def __add(self, row, node):
        if row.index_value < node.value.index_value:
            if node.left is None:
                node.left = Node(row)
            else:
                self.__add(row, node.left)

        else:
            if node.right is None:
                node.right = Node(row)
            else:
                self.__add(row, node.right)


    def find(self, row):
        if self.root is None:            
            return None
        else:
            return self.__find(row, self.root)


    def __find(self, row, node):
        if row.index_value == node.value.index_value:
            return node
        elif (row.index_value < node.value.index_value and node.left is not None):
            return self.__find(row, node.left)
        elif (row.index_value > node.value.index_value and node.right is not None):
            return self.__find(row, node.right)
  
        
    def find_successor(self, node):
        while node.left is not None:
            node = node.left
        return node


    def delete(self, root, row):

        if root is None:
            return root
            
            
        if row.index_value < root.value.index_value:
            root.left = self.delete(root.left, row)

        elif(row.index_value > root.value.index_value):
            root.right = self.delete(root.right, row)

        else:
            if root.left is None:
                temp = root.right
                root = None
                return temp

            elif root.right is None:
                temp = root.left
                root = None
                return temp

            temp = self.find_successor(root.right)
            root.value = temp.value

            root.right = self.delete(root.right, temp.value)
            
        return root



    def depth(self, node):
        if node == None:
            return 1
        
        
        return max(self.depth(node.left), self.depth(node.right)) + 1

    def display(self):
        if self.root is not None:
            self.__disp(self.root, self.depth(self.root))

    def __disp(self, node, c):
        if node is not None:
            self.__disp(node.left, c+1)
            if node is not self.root:
                print( '   '*c, str(node.value.disp()))
            self.__disp(node.right, c+1)


def pass_tree(root, node, array):
    if node:
        pass_tree(root, node.left, array)
        if node is not root:
            array.append(node.value.disp() + [node.value])
        pass_tree(root, node.right, array)


def pass_tree_dfs(root, node, array):
    if node:
        if node != root:
            array.append(node.value.value)
        pass_tree_dfs(root, node.left, array)
        pass_tree_dfs(root, node.right, array)

def message(text):
    print(text)
