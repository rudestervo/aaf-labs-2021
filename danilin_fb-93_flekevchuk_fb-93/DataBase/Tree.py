class Node:
    def __init__(self, value, id):
      self.left = None
      self.right = None
      self.value = value
      self.ids = [id]

    def insert(self, value, id):
        if self.value != None:
            if value < self.value:
                if self.left is None:
                    self.left = Node(value, id)
                else:
                    self.left.insert(value, id)
            elif value > self.value:
                if self.right is None:
                    self.right = Node(value, id)
                else:
                    self.right.insert(value, id)
            else: 
                self.ids.append(id)
        else:
            self.value = value
            self.ids = [id]

    def find(self, value, node = False):
        current = self
        while current != None:
            if value < current.value:
                current = current.left 
            elif value > current.value:
                current = current.right
            else: return current.ids if not node else current
        return [] if not node else node

    
    def getAllIDsMore( self, value, equal):
        allIDs = []
        current = self
        while current != None:
            if current.value > value:
                allIDs += current.ids
                if current.right:
                    current.right.getAllIDs(allIDs)
                if current.left:
                    current = current.left
                else:
                    return allIDs
            elif current.value < value:
                if current.right:
                    current = current.right
                else:
                    return allIDs
            else:
                if equal:
                    allIDs += current.ids
                if current.right:
                    current.right.getAllIDs(allIDs)
                    return allIDs
                else: return allIDs

    def getAllIDs(self, arr = []):
        if self.left:
            self.left.getAllIDs(arr)
        arr += self.ids
        if self.right:
            self.right.getAllIDs(arr)
        return arr


    def getAllIDsLess(self, value, equal ):
        allIDs = []
        current = self
        while current != None:
            if current.value < value:
                allIDs += current.ids
                if current.left:
                    current.left.getAllIDs(allIDs)
                if current.right:
                    current = current.right
                else:
                    return allIDs
            elif current.value > value:
                if current.left:
                    current = current.left
                else:
                    return allIDs
            else:
                if equal:
                    allIDs += current.ids
                if current.left:
                    current.left.getAllIDs(allIDs)
                    return allIDs  
                return allIDs

    def DeleteWithID(self, value, id):
        current = self.find(value, True)
        if len(current.ids) > 1:
            current.ids.remove(id)
            return 
        current.ids.remove(id)
        self.Delete(value)
        
    def Delete(self, data):
        parent = None
        node = self
        while node and node.value != data:
            parent = node
            if data < node.value:
               node = node.left
            elif data > node.value:
                node = node.right
		
        if node is None or node.value != data:
            return False
			
        elif node.left is None and node.right is None:
            if data < parent.value:
                parent.left = None
            else:
                parent.right = None
            return True
			
        elif node.left and node.right is None:
            if data < parent.value:
                parent.left = node.left
            else:
                parent.right = node.left
            return True
			
        elif node.left is None and node.right:
            if data < parent.value:
                parent.left = node.right
            else:
                parent.right = node.right
            return True
			
        else:
            delNodeParent = node
            delNode = node.right
            while delNode.left:
                delNodeParent = delNode
                delNode = delNode.left
				
            node.value = delNode.value
            node.ids = delNode.ids
            if delNode.right:
                if delNodeParent.value > delNode.value:
                    delNodeParent.left = delNode.right
                elif delNodeParent.value < delNode.value:
                    delNodeParent.right = delNode.right
            else:
                if delNode.value < delNodeParent.value:
                    delNodeParent.left = None
                else:
                    delNodeParent.right = None


    def PrintTree(self):
        if self.left:
            self.left.PrintTree()
        print( self.value,self.ids, end=', ')
        if self.right:
            self.right.PrintTree()



'''
root = Node(11,11)
root.insert(10,10)
root.insert(14,14)
root.insert(14,15)
root.insert(9.5,9.5)
root.insert(9.4,9.4)
root.insert(16,16)
root.insert(9.7,9.7)
root.insert(9.6,9.6)
root.insert(3,3)

root.PrintTree()
root.DeleteWithID(9.5,9.5)
print()
root.PrintTree()
print()

print('a0', root.getAllIDsMore(11, True))
print('a0', root.getAllIDsMore(0, True))
print('a0', root.getAllIDsLess(9.4, True))
print('a0', root.getAllIDsLess(4, True))
print('a0', root.getAllIDsMore(9.4, True))
print('a0', root.getAllIDsMore(1000, True))
print('a0', root.getAllIDsLess(9.4, True))

'''






