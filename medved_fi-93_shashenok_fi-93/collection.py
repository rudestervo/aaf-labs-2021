from rd_tree import RDTree
from pprint import pprint


class Collection:
    tree = RDTree()
    collections = {}

    def create_collection(self, collection_name: str):
        if collection_name in self.collections.keys():
            print('ERROR! Collection with this name already created')
            return 0
        self.collections[collection_name] = None
        print(f'Created collection {collection_name}')

    def print_tree(self, collection_name: str):
        print(f'{collection_name} tree:')
        if collection_name not in self.collections.keys():
            print('ERROR! There is no such collection')
            return 0
        root = self.collections[collection_name]
        dct = RDTree().convert_tree_to_dict(root)
        RDTree().print_dependency_tree(dct, str(root.data))
        print(' ')

    def insert_data(self, collection_name: str, data: list):
        if collection_name not in self.collections.keys():
            print('ERROR! There is no such collection')
            return 0
        root = self.collections[collection_name]
        self.collections[collection_name] = RDTree().insert(root, set(data))

    def get_leaves(self, collection_name: str):
        root = self.collections[collection_name]
        return RDTree().get_leaf_nodes(root)

    def search(self, collection_name: str, options=None, data=None):
        if collection_name not in self.collections.keys():
            print('ERROR! There is no such collection')
            return 0
        if not options:
            for leaf in self.get_leaves(collection_name):
                print(leaf)
        if options == 'intersects':
            for res in self.search_intersects(collection_name, data):
                print(res)
        if options == 'contains':
            for res in self.search_contains(collection_name, data):
                print(res)
        if options == 'contained_by':
            for res in self.search_contained_by(collection_name, data):
                print(res)

    def search_contains(self, collection_name: str, data: list):
        if collection_name not in self.collections.keys():
            print('ERROR! There is no such collection')
            return 0
        root = self.collections[collection_name]
        return RDTree().search_contains(root, set(data))

    def search_intersects(self, collection_name: str, data: list):
        if collection_name not in self.collections.keys():
            print('ERROR! There is no such collection')
            return 0
        root = self.collections[collection_name]
        return RDTree().search_inrersects(root, set(data))

    def search_contained_by(self, collection_name: str, data: list):
        if collection_name not in self.collections.keys():
            print('ERROR! There is no such collection')
            return 0
        root = self.collections[collection_name]
        return RDTree().search_contained_by(root, set(data))

    def contains(self, collection_name: str, data: list):
        if collection_name not in self.collections.keys():
            print('ERROR! There is no such collection')
            return 0
        root = self.collections[collection_name]
        conts = RDTree().contains(root, set(data))
        print(conts)

    def tst(self, coll: str):
        root = self.collections[coll]
        dct = RDTree().convert_tree_to_dict(root)
        RDTree().print_dependency_tree(dct, str(root.data))


def main():
    cl = Collection()
    cl.create_collection('coll1')
    cl.insert_data('coll1', [1, 10])
    cl.insert_data('coll1', [1, 2])
    cl.insert_data('coll1', [8, -7])
    cl.insert_data('coll1', [60, 2])
    # cl.tst('coll1')
    cl.print_tree('coll1')
    # cl.insert_data('coll1', [0, 10])
    cl.insert_data('coll1', [0, 10])
    cl.print_tree('coll1')
    # print(cl.search_intersects('coll1', [2,5]))
    # print({1, 2}.intersection({4, 3}) != set())

if __name__ == '__main__':
    main()
