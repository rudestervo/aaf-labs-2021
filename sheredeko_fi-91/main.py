class TextCollection:

    def insert(self, text):
        pass

    def print_index(self):
        pass

    def get_all(self):
        pass

    def keyword_search(self, keyword):
        pass

    def range_search(self, keyword_from, keyword_to):
        pass

    def distance_search(self, first_keyword, second_keyword, distance):
        pass


if __name__ == '__main__':
    t = TextCollection()

    t.insert("aaa bbb")
    t.insert("aaa ccc")

    t.print_index()

    for doc in t.get_all():
        print(doc)

    for doc in t.range_search('ddd', 'ppp'):
        print(doc)
