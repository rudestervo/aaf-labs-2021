class Interval:
    def _check(self, v1, v2):
        if isinstance(v1, int) and isinstance(v2, int):
            return True
        if (v1 == None and v2== None):
            return True
        else:
            print('X and Y must be an integer!')
            return False
    def __init__(self, user_x, user_y):
        try:
            if self._check(user_x, user_y):
                self.x=user_x
                self.y=user_y
                #print ('Interval successfully created!')
            else:
                raise Exception('Wrong arguments passed')
        except:
            print('Wrong arguments passed, the interval was not created')
class Node:
    def _check(self, dt):
        if isinstance(dt, Interval):return True
        if isinstance(dt, list):
            if(len(dt)==2 and isinstance(dt[0], int) and isinstance(dt[1], int)):
                convert_d=Interval(dt[0], dt[1])
                return convert_d
            if (len(dt) == 2 and dt[0]== None and dt[1]==None):
                convert_d = Interval(dt[0], dt[1])
                return convert_d
            else:
                print('Incorrect number of elements in array or non-integer value is passed')
                return False
        else:
            print('Wrong datatype is transferred')
            return False
    def __init__(self, user_data, p=None, lch=None, rch=None):
        try:
            decision = self._check(user_data)
            if isinstance(decision, bool):
                if decision:
                    self.data=user_data
                    self.left_child = lch
                    self.right_child = rch
                    self.parent = p
                    #print('New Node is created!')
                else: raise Exception('Wrong data transferred')
            elif isinstance(decision, Interval):
                self.data=decision
                self.left_child = lch
                self.right_child = rch
                self.parent = p
                #print('New Node is created!')
            else: raise Exception('Wrong data transferred')
        except:
            print("Error, the Node was not created")
    def print_Node(self):
        return '[' + str(self.data.x) + ', ' + str(self.data.y) + ']'

#складається з:
# - data have to be an Interval -- done
# - вказівника на лівого нащадка -- done
# - вказівника на правого нащадка --done
# - вказівника на предка -- done
# за замовчуванням усі вказівники вказують на нон, бо нода створюється окремо від дерева.
class KD_Tree:
    #function search:
        # contained by -- done
        # right of -- done
        # intersects -- done
    #function add_node -- done
    #function show -- done
    #function contains -- done
    #consists of root + leafs - root is stored within datastructure

    def __init__(self):
        #дерево должно создаваться с пустыми данными в корне, тогда при добавлении новой ноды нужно сделать проверку на наличие данных в корне
        self.root = Node([None, None])

#---------------------------------------------------------------------------
# chained functions to add nodes
    def __go_func(self, NewNode, currentNode, XY_f):
        XY=XY_f
        if XY: #checking by x
            if(currentNode.data.x >= NewNode.data.x):#go on the left?
                if(currentNode.left_child != None):
                    self.__go_func(NewNode, currentNode.left_child, not XY)
                else:
                    currentNode.left_child=NewNode
                    NewNode.parent=currentNode
            else:#go on the right?
                if(currentNode.right_child != None):
                    self.__go_func(NewNode, currentNode.right_child, not XY)
                else:
                    currentNode.right_child = NewNode
                    NewNode.parent=currentNode
        else: #checking by y
            if(currentNode.data.y >= NewNode.data.y):
                if(currentNode.left_child != None):
                    self.__go_func(NewNode, currentNode.left_child, not XY)
                else:
                    currentNode.left_child = NewNode
                    NewNode.parent = currentNode
            else:  # go on the right?
                 if (currentNode.right_child != None):
                    self.__go_func(NewNode, currentNode.right_child, not XY)
                 else:
                    currentNode.right_child = NewNode
                    NewNode.parent = currentNode

    def add_node(self, user_data):#here we should check where to add data by algorithm
        NewNode=Node(user_data) # create new node
        if(self.root.data.x == None and self.root.data.y == None):
            self.root.data.x = NewNode.data.x
            self.root.data.y = NewNode.data.y
        else:
            self.__go_func(NewNode, self.root, True)

#---------------------------------------------------------------------------
# chained functions to show tree

    def print(self):
        buffer = []
        self.__print_recursive(self.root, buffer, "", "")
        print("\n".join(buffer))

    def __print_recursive(self, node, buffer, prefix, childrenPrefix):
        buffer.append(prefix + node.print_Node())

        if node.right_child != None:
            if node.left_child != None:
                self.__print_recursive(node.right_child, buffer, childrenPrefix + "├── ", childrenPrefix + "│   ")
            else:
                self.__print_recursive(node.right_child, buffer, childrenPrefix + "└── ", childrenPrefix + "    ")
        if node.left_child != None:
            self.__print_recursive(node.left_child, buffer, childrenPrefix + "└── ", childrenPrefix + "    ")

#---------------------------------------------------------------------------
#chained functions to find an interval in Tree
    def __go_find(self, currentNode, FindNode, XY_f):
        XY=XY_f
        if(currentNode.data.x==FindNode.data.x and currentNode.data.y == FindNode.data.y):
            return True
        found=False
        if XY:
            if(currentNode.data.x >= FindNode.data.x):
                if(currentNode.left_child != None and not found):
                    found = self.__go_find(currentNode.left_child, FindNode, not XY)
                    return found
                else:
                    return False
            else:
                if(currentNode.right_child != None and not found):
                    found = self.__go_find(currentNode.right_child, FindNode, not XY)
                    return found
                else:
                    return False
        else:
            if (currentNode.data.y >= FindNode.data.y):
                if (currentNode.left_child != None and not found):
                    found = self.__go_find(currentNode.left_child, FindNode, not XY)
                    return found
                else:
                    return False
            else:
                if (currentNode.right_child != None and not found):
                    found = self.__go_find(currentNode.right_child, FindNode, not XY)
                    return found
                else:
                    return False


    def contains(self, user_data):
        FindNode = Node(user_data)
        found = self.__go_find(self.root, FindNode, True)
        if found:
            print('The KD-Tree contains this interval')
            return True
        else:
            print('The KD-Tree doesn`t contain this interval')
            return False

# ---------------------------------------------------------------------------
# search functions
    def __go_search_contained(self, currentNode, overNode, foundNodes, XY_f):
        XY=XY_f
        #check this node
        if(currentNode.data.x >= overNode.data.x and currentNode.data.y <= overNode.data.y):
            foundNodes.append(currentNode)
        if XY:#if checking by x
            if(currentNode.data.x >= overNode.data.y and currentNode.left_child != None): # doesn`t intersect each other - no sense in going to right child - should go ONLY to the left child
                self.__go_search_contained(currentNode.left_child, overNode, foundNodes, not XY)
            elif(currentNode.data.x < overNode.data.x and currentNode.right_child != None): # no need to go to the left child if current is already lower than searched, because on the left there only lower and lower items
                self.__go_search_contained(currentNode.right_child, overNode, foundNodes, not XY)
            else:
                if(currentNode.right_child != None):self.__go_search_contained(currentNode.right_child, overNode, foundNodes, not XY)
                if(currentNode.left_child != None):self.__go_search_contained(currentNode.left_child, overNode, foundNodes, not XY)
        else: # if checking by y
            if (currentNode.data.y <= overNode.data.x and currentNode.right_child != None):  # doesn`t intersect each other - no sense in going to left child - should go ONLY to the right child
                self.__go_search_contained(currentNode.right_child, overNode, foundNodes, not XY)
            elif(currentNode.data.y > overNode.data.y and currentNode.left_child != None): # no sense to go to the right child if current y is bigger that searched - go on the left
                self.__go_search_contained(currentNode.left_child, overNode, foundNodes, not XY)
            else:
                if(currentNode.right_child != None):self.__go_search_contained(currentNode.right_child, overNode, foundNodes, not XY)
                if(currentNode.left_child != None):self.__go_search_contained(currentNode.left_child, overNode, foundNodes, not XY)
        return foundNodes

    def __go_search_intersects(self, currentNode, overNode, foundNodes, XY_f):
        XY=XY_f
        if(overNode.data.x<=currentNode.data.y and overNode.data.y>=currentNode.data.x):
            foundNodes.append(currentNode)
        if XY: # check by X
            if(currentNode.data.x > overNode.data.y): # doesnt intersect each other - no sense to go on the right
                if(currentNode.left_child != None): self.__go_search_intersects(currentNode.left_child, overNode, foundNodes, not XY)
            else:
                if (currentNode.left_child != None): self.__go_search_intersects(currentNode.left_child, overNode, foundNodes, not XY)
                if (currentNode.right_child != None): self.__go_search_intersects(currentNode.right_child, overNode, foundNodes, not XY)
        else:
            if(currentNode.data.y < overNode.data.x):
                if(currentNode.right_child != None): self.__go_search_intersects(currentNode.right_child, overNode, foundNodes, not XY)
            else:
                if (currentNode.left_child != None): self.__go_search_intersects(currentNode.left_child, overNode, foundNodes, not XY)
                if (currentNode.right_child != None): self.__go_search_intersects(currentNode.right_child, overNode,foundNodes, not XY)
        return foundNodes

    def search(self, user_data, whattodo):
        UserNode = Node(user_data)
        nodes=[]
        if (whattodo=="contained_by"):
            FoundNodes=self.__go_search_contained(self.root, UserNode, nodes, True)
        if(whattodo=="intersects"):
            FoundNodes=self.__go_search_intersects(self.root, UserNode, nodes, True)
        for i in range(0, len(FoundNodes)):
            print(FoundNodes[i].print_Node())

# ---------------------------------------------------------------------------
# right of functions

    def __go_search_right(self, currentNode, key, foundNodes, XY_f):
        XY=XY_f
        if(currentNode.data.x>=key):
            foundNodes.append(currentNode)
        if XY: # checked by X level
            if (currentNode.data.x >= key):
                    # if current x was on the right of key, have to check both children
                    if (currentNode.right_child != None): self.__go_search_right(currentNode.right_child, key, foundNodes, not XY)
                    if (currentNode.left_child != None): self.__go_search_right(currentNode.left_child, key, foundNodes, not XY)
             # если текущий узел не прошёл проверку - влево можно даже не идти, так как там находятся х которые только меньше текущего. Не работает для уровней, где сравнение происходило по у
            else:
                if(currentNode.right_child != None): self.__go_search_right(currentNode.right_child, key, foundNodes, not XY)
        else: #checked by Y level
            if (currentNode.data.y <= key): # go only to the right
                if(currentNode.right_child != None): self.__go_search_right(currentNode.right_child, key, foundNodes, not XY)
            else: #check both
                if (currentNode.right_child != None): self.__go_search_right(currentNode.right_child, key, foundNodes,not XY)
                if (currentNode.left_child != None): self.__go_search_right(currentNode.left_child, key, foundNodes,not XY)
        return foundNodes

    def right_of(self, user_data):
        nodes = []
        FoundNodes = self.__go_search_right(self.root, user_data, nodes, True)
        for i in range(0, len(FoundNodes)):
            print(FoundNodes[i].print_Node())



#----------------------------------------------------------------------------
# testing area








