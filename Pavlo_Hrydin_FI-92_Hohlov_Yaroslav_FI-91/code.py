from func import *
import re
name_tree = []
argument = {}

def Create(words):
	if not(words[1] in name_tree):
		if(re.search(r'[a-zA-Z]',words[1])):
			argument[words[1]] = []
			name_tree.append(words[1])
			print("Set", words[1], "has been created")
		else: print("Incorrect name")
	else: print("This name has been created")

def Insert(words):
	if(words[1] in name_tree):
		arg = str.split('[', 1)[1].split(']')[0].replace(',', ' ').split()
		if (int(arg[0]) <= int(arg[1])):
			if (argument[words[1]] == []):
				arg = [int(arg[0]), int(arg[1]),]
				argument[words[1]] = Node(arg, words[1])
			else:
				arg = [int(arg[0]), int(arg[1])]
				argument[words[1]].insert(arg, words[1])

		else: print("segment entered incorrectly")
	else: print("Incorrect name")

def Contains_tree(words):
	if(words[1] in name_tree):
		arg = str.split('[', 1)[1].split(']')[0].replace(',', ' ').split()
		arg = [int(arg[0]), int(arg[1])]
		argument[words[1]].Contains(arg)


def Search_tree(words):

	if(words[1] in name_tree):
		if(len(words) > 2):
			if(re.search(r'(?i)where', words[2])):
				if(re.search(r'(?i)contains_by',words[3])):
					arg = str.split('[', 1)[1].split(']')[0].replace(',', ' ').split()
					arg = [int(arg[0]), int(arg[1])]
					argument[words[1]].Search(arg)
				elif(re.search(r'(?i)intersects', words[3])):
					arg = str.split('[', 1)[1].split(']')[0].replace(',', ' ').split()
					arg = [int(arg[0]), int(arg[1])]
					argument[words[1]].Intersects(arg)
				elif(re.search(r'(?i)right_of', words[3])):
					if(re.search(r'[0-9]',words[4])):
						argument[words[1]].right_Search(int(words[4]))
			else: print("WHERE is error")
		else: argument[words[1]].e_Search()

def Print(words):
	if(words[1] in name_tree):
		if (argument[words[1]] != []):
			argument[words[1]].PrintTree()
		else:
			print("<None inside>")
	else: print("Haven't this tree")

def filter(str):
	"""Create"""
	words = re.findall(r'\S+', str)
	if(re.search(r'(?i)create',words[0])):
		Create(words)
	elif(re.search(r'(?i)insert',words[0])):
		Insert(words)
	elif(re.search(r'(?i)contains',words[0])):
		Contains_tree(words)
	elif(re.search(r'(?i)search',words[0])):
		Search_tree(words)
	elif(re.search(r'(?i)print',words[0])):
		Print(words)
	else:
		print("Incorrect command")

str = ''
while True:
    str += ' ' + input("-->").strip()
    if ';' in str:
    	for command in str.split(';'):
            if command:
                command = command.strip()
                try:
                	filter(command)
                except:
                    print("You have done mistake")
                str = ''

# while True:
#             query += ' ' + input(">").strip()
#             if ';' in query:
#                 for command in query.split(';'): # Split commands with ';' : CREATE ...; SELECT ...
#                     if command:
#                         command = command.strip()
#                         if command.upper() == 'EXIT': # Exit command to stop the program
#                             raise self.exit()
#                         try:
#                             response = self.action(command) # Try to parse and complete the commands
#                         except IndexError:
#                             response = self.error()
#                         except Exception as error:
#                             response = 'Error: {}'.format(str(error))
#                         print(response)
#                         query = ''
#
