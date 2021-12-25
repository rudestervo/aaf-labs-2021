KDTrees = {}


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, point):
        return (int(self.x) - int(point.x)) ** 2 + (int(self.y) - int(point.y)) ** 2


class KDTree:

    def __init__(self):
        self.root = None

    def insert(self, point: Point):
        if self.root == None:
            self.root = Node(point, True)
        else:
            if self.contains(point):
                print("point with the same coordinates already exist")
                return None
            self.root.put_point_in_node(point)

    def contains(self, point: Point):
        if self.root == None:
            return False
        else:
            return self.root.check_point_in_node(point)

    def search(self):
        if self.root == None:
            print("this tree is empty")
        else:
            self.root.search_in_tree()

    def search_where_inside(self, coordinates: (Point, Point)):
        if self.root == None:
            print("this tree is empty")
        else:
            self.root.search_points_inside(coordinates)

    def search_where_above_to(self, y):
        if self.root == None:
            print("this tree is empty")
        else:
            self.root.search_points_above_to(y)

    def nn(self, point: Point):
        if self.root == None:
            print("this tree is empty")
        else:
            list_of_neighbours = []
            self.root.nearest_neighbour(point, list_of_neighbours)
            for nn in list_of_neighbours: print("(" + str(nn.x) + "," + str(nn.y) + ")")

    def print_tree(self):
        if self.root == None:
            print("this tree is empty")
        else:
            self.root.print_t("")


class Node:

    def __init__(self, point: Point, bool_x):
        self.bool_x = bool_x
        self.left_kid = None
        self.right_kid = None
        self.current_point = point

    def put_point_in_node(self, point: Point):
        if self.bool_x:
            if int(point.x) < int(self.current_point.x):
                if self.left_kid:
                    self.left_kid.put_point_in_node(point)
                else:
                    self.left_kid = Node(point, not self.bool_x)
            else:
                if self.right_kid:
                    self.right_kid.put_point_in_node(point)
                else:
                    self.right_kid = Node(point, not self.bool_x)
        else:
            if int(point.y) < int(self.current_point.y):
                if self.left_kid:
                    self.left_kid.put_point_in_node(point)
                else:
                    self.left_kid = Node(point, not self.bool_x)
            else:
                if self.right_kid:
                    self.right_kid.put_point_in_node(point)
                else:
                    self.right_kid = Node(point, not self.bool_x)

    def search_in_tree(self):
        if self.current_point != None:
            print("(" + str(self.current_point.x) + "," + str(self.current_point.y) + ")")
            if self.left_kid != None:
                self.left_kid.search_in_tree()
            if self.right_kid != None:
                self.right_kid.search_in_tree()
        else:
            return None

    def check_point_in_node(self, point: Point):
        if point.x == self.current_point.x and point.y == self.current_point.y:
            return True
        else:
            if self.bool_x:
                if point.x < self.current_point.x:
                    if self.left_kid:
                        return self.left_kid.check_point_in_node(point)
                    else:
                        return False
                else:
                    if self.right_kid:
                        return self.right_kid.check_point_in_node(point)
                    else:
                        return False
            else:
                if point.y < self.current_point.y:
                    if self.left_kid:
                        return self.left_kid.check_point_in_node(point)
                    else:
                        return False
                else:
                    if self.right_kid:
                        return self.right_kid.check_point_in_node(point)
                    else:
                        return False

    def search_points_inside(self, coordinates: (Point, Point)):
        if self.current_point != None:
            if int(self.current_point.x) >= int(coordinates[0].x) and int(self.current_point.x) <= int(
                    coordinates[1].x):
                if int(self.current_point.y) >= int(coordinates[0].y) and int(self.current_point.y) <= int(
                        coordinates[1].y):
                    print("(" + str(self.current_point.x) + "," + str(self.current_point.y) + ")")
            if self.left_kid != None:
                self.left_kid.search_points_inside(coordinates)
            if self.right_kid != None:
                self.right_kid.search_points_inside(coordinates)
        else:
            return None

    def search_points_above_to(self, y):
        if int(self.current_point.y) >= int(y):
            print("(" + str(self.current_point.x) + "," + str(self.current_point.y) + ")")
        if self.bool_x:
            if self.left_kid != None:
                self.left_kid.search_points_above_to(y)
            if self.right_kid != None:
                self.right_kid.search_points_above_to(y)
        else:
            if int(self.current_point.y) < int(y):
                if self.right_kid != None:
                    self.right_kid.search_points_above_to(y)
            else:
                if self.left_kid != None:
                    self.left_kid.search_points_above_to(y)
                if self.right_kid != None:
                    self.right_kid.search_points_above_to(y)

    def nearest_neighbour(self, point: Point, list_of_neighbours):
        if self.current_point != None:
            if len(list_of_neighbours) == 0:
                list_of_neighbours.append(self.current_point)
                if self.left_kid != None:
                    self.left_kid.nearest_neighbour(point, list_of_neighbours)
                if self.right_kid != None:
                    self.right_kid.nearest_neighbour(point, list_of_neighbours)
            else:
                if self.current_point.distance(point) < list_of_neighbours[0].distance(point):
                    del list_of_neighbours[:]
                    list_of_neighbours.append(self.current_point)
                    if self.left_kid != None:
                        self.left_kid.nearest_neighbour(point, list_of_neighbours)
                    if self.right_kid != None:
                        self.right_kid.nearest_neighbour(point, list_of_neighbours)
                elif self.current_point.distance(point) == list_of_neighbours[0].distance(point):
                    if self.current_point not in list_of_neighbours:
                        list_of_neighbours.append(self.current_point)
                    if self.left_kid != None:
                        self.left_kid.nearest_neighbour(point, list_of_neighbours)
                    if self.right_kid != None:
                        self.right_kid.nearest_neighbour(point, list_of_neighbours)
                else:
                    if self.left_kid != None:
                        self.left_kid.nearest_neighbour(point, list_of_neighbours)
                    if self.right_kid != None:
                        self.right_kid.nearest_neighbour(point, list_of_neighbours)

    def print_t(self, paragraph: str):
        print(paragraph + "(" + str(self.current_point.x) + "," + str(self.current_point.y) + ")")
        new_paragraph = paragraph[0:-4] + "│" if paragraph[-4:] == "├── " else paragraph[0:-4] + " "
        if self.right_kid == None:
            if self.left_kid != None:
                self.left_kid.print_t(new_paragraph + "   └── ")
        else:
            if self.left_kid != None:
                self.left_kid.print_t(new_paragraph + "   ├── ")
            if self.right_kid != None:
                self.right_kid.print_t(new_paragraph + "   └── ")



