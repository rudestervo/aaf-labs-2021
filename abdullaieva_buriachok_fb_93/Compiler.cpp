#include <iostream>
#include <regex>
#include <deque>
#include "Array.h"
#include "Token.h"
#include "Database.h"

using namespace std;

int main()
{
	Array<Token_Type> token_types = { {
		{Token::Type::SPACE, regex("^ {1,}")},
		{Token::Type::CREATE, regex("^[cC][rR][eE][aA][tT][eE]")},
		{Token::Type::INSERT, regex("^[iI][nN][sS][eE][rR][tT]( {1,}[iI][nN][tT][oO])?")},
		{Token::Type::SELECT, regex("^[sS][eE][lL][eE][cC][tT]")},
		{Token::Type::DELETE, regex("^[d][e][l][e][t][e]( {1,}[fF][rR][oO][mM])?")},
		{Token::Type::WHERE, regex("^[wW][hH][eE][rR][eE]")},
		{Token::Type::INDEXED, regex("^[iI][nN][dD][eE][xX][eE][dD]")},
		{Token::Type::FROM, regex("^[fF][rR][oO][mM]")},
		{Token::Type::JOIN, regex("^[jJ][oO][iI][nN]")},
		{Token::Type::ON, regex("^[oO][nN]")},
		{Token::Type::NAME, regex("^[a-zA-Z][a-zA-Z0-9_]{0,}")},
		{Token::Type::COMMA, regex("^,")},
		{Token::Type::VALUE, regex("^\\`[a-zA-Z0-9_]*\\`")},
		{Token::Type::LPAR, regex("^\\(")},
		{Token::Type::RPAR, regex("^\\)")},
		{Token::Type::OPERATOR, regex("^(=|!=|<=|>=|<|>)")},
		{Token::Type::ALL, regex("^\\*")}
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

			parser_analysis(database, Array<Token>(tokens_list));
		}
		catch (const exception& ex)
		{
			cout << ex.what() << endl;
		}

		getline(cin, code);
		
		cout << endl;
	}
	
	return 0;
}