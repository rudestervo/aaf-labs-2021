#include <iostream>
#include <deque>
#include "Token.h"
#include "Database.h"

using namespace std;

int main()
{
	Token_Type token_types_array[] = {
		{Type::SPACE, " {1,}"},
		{Type::CREATE, "create"},
		{Type::INSERT, "insert( {1,}into)?"},
		{Type::SELECT, "select"},
		{Type::DELETE, "delete( {1,}from)?"},
		{Type::WHERE, "where"},
		{Type::INDEXED, "indexed"},
		{Type::FROM, "from"},
		{Type::JOIN, "join"},
		{Type::ON, "on"},
		{Type::NAME, "[a-z][a-z0-9_]{0,}"},
		{Type::COMMA, ","},
		{Type::VALUE, "\\`[a-z0-9_]{1,}\\`"},
		{Type::LPAR, "\\("},
		{Type::RPAR, "\\)"},
		{Type::OPERATOR, "(=|!=|<=|>=|<|>)"},
		{Type::ALL, "\\*"}
	};

	int token_types_size = sizeof(token_types_array) / sizeof(*token_types_array);

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

		for (int i = 0; i < code_size; i++)
		{
			if (code[i] >= 65 && code[i] <= 90)
			{
				code[i] += 32;
			}
		}

		//cout << code << endl;

		if (code.find(".exit") != string::npos)
		{
			break;
		}

		deque<Token> tokens_list;

		try
		{
			lexer_analysis(code, token_types_array, token_types_size, tokens_list);
		}
		catch (const exception& ex)
		{
			cout << ex.what() << endl;
		}

		int tokens_array_size = tokens_list.size();

		Array<Token> tokens_array(tokens_array_size);

		for (int i = 0; i < tokens_array_size; i++)
		{
			tokens_array[i] = tokens_list[i];

			//cout << "Type: " << tokens_array[i].type << "\tText: " << tokens_array[i].text  << endl;
		}

		try
		{
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