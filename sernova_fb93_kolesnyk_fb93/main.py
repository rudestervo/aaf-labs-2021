from parser1 import *
from lexer import *



lex = Lexer()
parser = Parser()
#example CREATE TABLE qq(first INDEXED, second) INSERT qq("Kolesnyk", "Andrii") INSERT qq("Sernova", "Asya") INSERT qq("Stolovych", "Mykhailo") SELECT * FROM qq WHERE first==Kolesnyk
while(True):
    b=input("Enter command: ")
    lex.NewCode(b)
    commands = lex.CodeToTokens()
    parser.parse(commands)
    parser.start()

