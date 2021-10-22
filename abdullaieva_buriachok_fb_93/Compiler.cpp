#include <iostream>
#include <regex>
#include <deque>
#include "Array.hpp"
#include "Token.hpp"
#include "Database.hpp"

using namespace std;

int main()
{
	Array<Token_Type> token_types = { {
		{Type::SPACE, " {1,}"},
		{Type::CREATE, "[cC][rR][eE][aA][tT][eE]"},
		{Type::INSERT, "[iI][nN][sS][eE][rR][tT]( {1,}[iI][nN][tT][oO])?"},
		{Type::SELECT, "[sS][eE][lL][eE][cC][tT]"},
		{Type::DELETE, "[d][e][l][e][t][e]( {1,}[fF][rR][oO][mM])?"},
		{Type::WHERE, "[wW][hH][eE][rR][eE]"},
		{Type::INDEXED, "[iI][nN][dD][eE][xX][eE][dD]"},
		{Type::FROM, "[fF][rR][oO][mM]"},
		{Type::JOIN, "[jJ][oO][iI][nN]"},
		{Type::ON, "[oO][nN]"},
		{Type::NAME, "[a-zA-Z][a-zA-Z0-9_]{0,}"},
		{Type::COMMA, ","},
		{Type::VALUE, "\\`[a-zA-Z0-9_]*\\`"},
		{Type::LPAR, "\\("},
		{Type::RPAR, "\\)"},
		{Type::OPERATOR, "(=|!=|<=|>=|<|>)"},
		{Type::ALL, "\\*"}
	} };

	Database database;

	while (true)
	{
		cout << "Enter command:" << endl;

		string code;

		getline(cin, code, ';');

		replace(code.begin(), code.end(), '\t', ' ');
		replace(code.begin(), code.end(), '\n', ' ');
		replace(code.begin(), code.end(), '\r', ' ');

		int code_size = code.length();

		/*for (int i = 0; i < code_size; i++)
		{
			if (code[i] >= 65 && code[i] <= 90)
			{
				code[i] += 32;
			}
		}*/

		//cout << code << endl;

		/*if (code.find(".exit") != string::npos)
		{
			break;
		}*/

		smatch matches;
		regex regular(".[eE][xX][iI][tT]");

		if (regex_search(code, matches, regular))
		{
			break;
		}

		deque<Token> tokens_list;

		try
		{
			lexer_analysis(code, token_types, tokens_list);

			int tokens_array_size = tokens_list.size();

			Array<Token> tokens_array(tokens_list);

			/*for (int i = 0; i < tokens_array.size(); i++)
			{
				cout << "Type: " << tokens_array[i].type << "\tText: " << tokens_array[i].text  << endl;
			}*/

			parser_analysis(database, tokens_array);
		}
		catch (const exception& ex)
		{
			cout << ex.what() << endl;
		}

		cout << endl;
	}
	
	return 0;
}