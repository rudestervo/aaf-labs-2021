import functions as func


def console_commands():
    while True:
        print("write a command")
        command = ""
        while command.find(";") == -1:
            command += input() + " "
        right_command = " ".join(command[:command.find(";")].split())
        command_name = right_command.split()[0].lower()
        command_param = right_command[len(command_name) + 1:]


        if len(right_command.split()) < 2 and command_name != ".exit": print("incorrect command")
        elif len(right_command.split()) > 1 and command_name == ".exit": print("exit command doesn`t accept parameters")
        else:
            if command_name == "create": func.create(command_param)
            elif command_name == "insert": func.insert(command_param)
            elif command_name == "search": func.search(command_param)
            elif command_name == "print_tree": func.print_tree(command_param)
            elif command_name == "contains": func.contains(command_param)
            elif command_name == ".exit": func.exit()
            else: print("command name is not correct")

        if command_name == ".exit" and len(right_command.split()) == 1: break