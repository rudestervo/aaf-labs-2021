import os.path
import re

def create(command__create):
    if command__create[0].lower() == "create" and len(command__create) == 2:
        collection = command__create
        file__name = command__create[1] + '.txt'
        file = open(file__name, 'a+', encoding='utf-8')
        file.close()
        print(str(command__create[1]), "is created")
        del collection[0]
        return collection
    else:
        print("incorrect syntax")

def insert(command__insert):
    if command__insert[0].lower() == "insert" and len(command__insert) >= 3:
        document = command__insert
        file__name = command__insert[1] + '.txt'
        if os.path.exists(file__name):
            del document[:2]
            document = " ".join(document)
            file = open(file__name, "a+", encoding="utf-8")
            file.write(str(document) + '\n')
            print("Document added to collection")
        else:
            print("incorrect collection")
    else:
        print("incorrect syntax")

def index(command__index):
    if command__index[0].lower() == "print_index" and len(command__index) == 2:
        file__name = command__index[1] + '.txt'
        if os.path.exists(file__name):
            file = open(file__name, encoding="utf8").read()
            file = file.split('\n')
            list_ = []
            for i in range(len(file)):
                list_.append((file[i]))

            b = []
            for i in range(0, len(list_)):
                b.append([list_[i]])

            arr = b
            for i in range(len(list_)):
                arr[i] = b[i][0].split(' ')
            print(arr[:-1])

            for i in range(0, len(arr)-1):
                for j in range(0, len(arr[i])):
                    print("Position:", [i, j], str(arr[i][j]))
            return arr
        else:
            print("incorrect collection")
    elif len(command__index) < 2:
        print("choose collection")
    else:
        print("incorrect syntax")

def search(search__command, arr):
    if search__command[0].lower() == "search" and len(search__command) == 2:
        file__name = search__command[1] + '.txt'
        if os.path.exists(file__name):
            print(arr)
        else:
            print('incorrect collection name')
    elif search__command[0].lower() == "search" and search__command[2].lower() == "where" and len(search__command) > 3:
        file__name = search__command[1] + '.txt'
        if os.path.exists(file__name):
            key = search__command[-1]
            key = list(key)
            if key[-1] != "*":
                keyword = search__command[-1]
                for i in range(0, len(arr) - 1):
                    for j in range(0, len(arr[i])):
                        if arr[i][j] == keyword:
                            print(arr[i])
            elif key[-1] == "*":
                key[-1] = key[-1].replace("*", "\w+")
                for i in range(len(key)):
                    key = "".join(key)
                for i in range(0, len(arr) - 1):
                    for j in range(0, len(arr[i])):
                        result = re.findall(key, arr[i][j])
                for i in range(0, len(arr) - 1):
                    for j in range(0, len(arr[i])):
                        if arr[i][j] == result[0]:
                            print(arr[i])
        else:
            print('incorrect collection name')
    else:
        print("incorrect syntax")

array = []
document = []
collection = []

while True:
    check = str(input(">"))
    lst = check.split(" ")
    command = []
    for i in range(len(lst)):
        command.append(lst[i])
        i += 1
    if command[0].lower() == "create":
        collection = create(command)
    elif command[0].lower() == "insert":
        document = insert(command)
    elif command[0].lower() == "print_index":
        array = []
        array = index(command)
    elif command[0].lower() == "exit":
        break
    elif command[0].lower() == "search":
        search(command, array)
    else:
        pass