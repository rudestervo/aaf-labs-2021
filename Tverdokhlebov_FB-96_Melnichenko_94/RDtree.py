import collections

class Element:
    def __init__(self, value: set):
        self.left = None
        self.data = value
        self.right = None
class RDtree:
    root = None
    l=[]
    m=[]
    def get_element_data(self, data):
        return Element(data)
    def insert(self, element, data: set):
        if not element:
            return self.get_element_data(data)
        self.root = element

        if not self.is_child(element):
            if len(element.left.data.intersection(data)) > len(element.right.data.intersection(data)):
                element.data = element.data.union(data)
                self.insert(element.left, data)
            else:
                element.data = element.data.union(data)
                self.insert(element.right, data)
        else:
            element.left = self.get_element_data(element.data)
            element.data = element.data.union(data)
            element.right = self.get_element_data(data)
        return element

    def is_child(self, element: Element):
        if element.left or element.right:
            return False
        return True

    def tree_to_dict(self, element):
        tree = {}
        def prepare_tree(element):
            if self.is_child(element):
                return tree
            tree[str(element.data)] = {str(element.left.data), str(element.right.data)}
            prepare_tree(element.left)
            prepare_tree(element.right)
        prepare_tree(element)
        tree_dict=tree
        self.print_tree(tree_dict, str(element.data))

    def print_tree(self, tree, root, *, criteria=None):
        depth, branch, visited = criteria or (0, [], set())
        if root not in tree:
            return
        if depth == 0:
            print(" "  + root)
        visited |={root}
        branch += [None]
        fork=len(set(tree[root]) - visited)
        for visited_elem in sorted(set(tree[root]) - visited):
            fork -=1
            branch[depth] = ("├──" if fork else "└──")
            if visited_elem in visited: continue
            print(" " + "".join(branch) + visited_elem)
            if visited_elem in tree:
                branch[depth]=("│   "if fork else "    ")
                new_creteria = depth+1, branch.copy(),visited.copy()
                self.print_tree(tree,visited_elem,  criteria= new_creteria)
    
    def tree_search(self, element, value: set):
        if(element==None): return False
        if(element.data==value): return True
        res1 =self.tree_search(element.left, value)
        if res1: return True
        res2 = self.tree_search(element.right, value)
        return res2
    
    def search_where_intersects(self, element, value):
        if(set(value).intersection(element.data)): return True
        res1 = self.search_where_intersects(element.left, value)
        if res1: return True
        res2= self.search_where_intersects(element.right, value)
        return res2
        

        
    def inorder(self, element):
        res=[]
        if not self.is_child(element):
            res.append(list(element.data))
            res = res + self.inorder(element.left)
            res = res + self.inorder(element.right)
            # res= self.inorder(element.left)
            # res.append(list(element.data))
            # res= res + self.inorder(element.right)
        return res
    
    def search_where_contains(self, element, value):
        # res=self.inorder(element)
        # print(res)
        # for i in res:
        #     if set(value).issubset(element.data): print(list(i))
        if(set(value).issubset(element.data)): return True
        res1 = self.search_where_contains(element.left, value)
        if res1: return True
        res2= self.search_where_contains(element.right, value)
        return res2

    def search_where_contained_by(self,element, value):
        if(set(value).issuperset(element.data)): return True
        res1 = self.search_where_contained_by(element.left, value)
        if res1: return True
        res2= self.search_where_contained_by(element.right, value)
        return res2



