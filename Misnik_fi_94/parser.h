#include "dlist.h"
#include "stacks.h"
#include "dbase.h"

void parse_string(stacks ** root,char * str);// parsing string whit expression

int parse_comm(stacks * root,dbase * base);

bool isSpacer(char * ch);

bool isDivider(char * ch);

bool isDigit(char * ch);

bool isCharacter(char * ch);

bool isSymbol(char * ch);
