#pragma once
#include <iostream>
#include <deque>
#include <regex>
#include "Array.h"
#include "Database.h"
#include "Condition.h"

using namespace std;

enum Type
{
	SPACE,
	CREATE,
	INSERT,
	SELECT,
	DELETE,
	WHERE,
	INDEXED,
	FROM,
	JOIN,
	ON,
	NAME,
	VALUE,
	COMMA,
	LPAR,
	RPAR,
	OPERATOR,
	ALL
};

struct Token_Type
{
	Type type;
	string regex;

	Token_Type()
	{
		this->regex = "";
	}

	Token_Type(Type type, string regex)
	{
		this->type = type;
		this->regex = regex;
	}

	Token_Type(const Token_Type& token_type)
	{
		this->type = token_type.type;
		this->regex = token_type.regex;
	}
};





struct Token
{
	Type type;
	string text;

	Token()
	{
		this->text = "";
	}

	Token(Type type, string text)
	{
		this->type = type;
		this->text = text;
	}

	Token(const Token& token)
	{
		this->type = token.type;
		this->text = token.text;
	}
};





bool lexer_analysis(string code, Token_Type token_types_array[], const int token_types_size, deque<Token>& tokens_list)
{
	int position = 0;

	while (position < code.length())
	{
		bool check = true;

		string current_code = code.substr(position);
		smatch matches;

		for (int i = 0; i < token_types_size; i++)
		{
			regex regular("^" + token_types_array[i].regex);

			if (regex_search(current_code, matches, regular))
			{
				if (token_types_array[i].type != Type::SPACE)
				{
					Token token(token_types_array[i].type, matches[0]);
					tokens_list.push_back(token);
				}

				position += matches[0].length();

				check = false;

				break;
			}
		}

		if (check)
		{
			cerr << "error at position " << position << endl;	throw;
		}
	}
}





void parser_analysis(Database& database, const Array<Token>& tokens_array)
{
	int tokens_array_size = tokens_array.size();
	
	if (tokens_array_size == 0)
	{
		cerr << "empty string" << endl;	throw;
	}

	if (tokens_array[0].type != Type::CREATE && tokens_array[0].type != Type::INSERT && tokens_array[0].type != Type::SELECT && tokens_array[0].type != Type::DELETE)
	{
		cerr << "unknown command" << endl;	throw;
	}

	if (tokens_array[0].type == Type::CREATE)
	{
		if (tokens_array_size < 5)
		{
			cerr << "wrong number of parameters in CREATE command" << endl;	throw;
		}

		if (tokens_array[1].type != Type::NAME)
		{
			cerr << "unexpected token at position 1" << endl;	throw;
		}

		if (tokens_array[2].type != Type::LPAR)
		{
			cerr << "unexpected token at position 2" << endl;	throw;
		}

		if (tokens_array[3].type != Type::NAME)
		{
			cerr << "unexpected token at position 3" << endl;	throw;
		}

		if (tokens_array[tokens_array_size - 1].type != Type::RPAR)
		{
			cerr << "unexpected token at position " << tokens_array_size - 1 << endl;	throw;
		}

		deque<string> columns_list;
		deque<string> indexes_list;

		columns_list.push_back(tokens_array[3].text);

		Type previous_token = Type::NAME;

		for (int i = 4; i < tokens_array_size - 1; i++)
		{
			Type current_token = tokens_array[i].type;

			if (previous_token == Type::NAME && current_token != Type::INDEXED && current_token != Type::COMMA)
			{
				cerr << "unexpected token at position " << i << endl;	throw;
			}

			if (previous_token == Type::INDEXED && current_token != Type::COMMA)
			{
				cerr << "unexpected token at position " << i << endl;	throw;
			}

			if (previous_token == Type::COMMA && current_token != Type::NAME)
			{
				cerr << "unexpected token at position " << i << endl;	throw;
			}

			if (current_token == Type::NAME)
			{
				columns_list.push_back(tokens_array[i].text);
			}

			if (current_token == Type::INDEXED)
			{
				indexes_list.push_back(tokens_array[i - 1].text);
			}

			previous_token = current_token;
		}

		//variables for CREATE

		string table_name = tokens_array[1].text;

		int columns_size = columns_list.size();

		Array<string> columns(columns_size);

		for (int i = 0; i < columns_size; i++)
		{
			columns[i] = columns_list[i];
		}

		int indexes_size = indexes_list.size();

		Array<string> indexes(indexes_size);

		for (int i = 0; i < indexes_size; i++)
		{
			indexes[i] = indexes_list[i];
		}

		//call CREATE command

		database.create(table_name, columns, indexes);
	}

	if (tokens_array[0].type == Type::INSERT)
	{
		if (tokens_array_size < 5)
		{
			cerr << "wrong number of parameters in CREATE command" << endl;	throw;
		}

		Array<Type> pattern(tokens_array_size);

		pattern[0] = Type::INSERT;
		pattern[1] = Type::NAME;
		pattern[2] = Type::LPAR;
		pattern[tokens_array_size - 1] = Type::RPAR;

		for (int i = 3; i < tokens_array_size - 1; i++)
		{
			pattern[i] = (i % 2 ? Type::VALUE : Type::COMMA);
		}

		for (int i = 0; i < tokens_array_size; i++)
		{
			if (tokens_array[i].type != pattern[i])
			{
				cerr << "unexpected token at position " << i << endl;	throw;
			}
		}

		//variables for INSERT

		string table_name = tokens_array[1].text;

		int values_size = (tokens_array_size - 3) / 2;

		Array<string> values(values_size);

		for (int i = 3; i < tokens_array_size; i += 2)
		{
			string text = tokens_array[i].text;

			values[(i - 3) / 2] = text.substr(1, text.length() - 2);
		}

		//call INSERT command

		database.insert(table_name, values);
	}

	if (tokens_array[0].type == Type::SELECT)
	{
		if (tokens_array_size < 4)
		{
			cerr << "wrong number of parameters in SELECT command" << endl;	throw;
		}

		if (tokens_array[1].type != Type::ALL && tokens_array[1].type != Type::NAME)
		{
			cerr << "unexpected token at position 1" << endl;	throw;
		}

		//FROM

		int position_from = -1;

		if (tokens_array[1].type == Type::ALL)
		{
			if (tokens_array[2].type != Type::FROM)
			{
				cerr << "unexpected token at position 2" << endl;	throw;
			}

			position_from = 2;
		}

		if (tokens_array[1].type == Type::NAME)
		{
			for (int i = 2; i < tokens_array_size; i++)
			{
				if (tokens_array[i].type == Type::FROM)
				{
					position_from = i;
					break;
				}

				if (tokens_array[i].type != (i % 2 ? Type::NAME : Type::COMMA))
				{
					cerr << "unexpected token at position " << i << endl;
				}
			}
		}

		if (position_from == -1)
		{
			cerr << "missed keyword FROM" << endl;	throw;
		}

		if (tokens_array_size - 1 == position_from)
		{
			cerr << "wrong number of parameters in FROM construction" << endl;	throw;
		}

		if (tokens_array[position_from + 1].type != Type::NAME)
		{
			cerr << "unexpected token at position " << position_from + 1 << endl;	throw;
		}

		//JOIN

		int position_join = -1;
		string table_name_join = "";
		Condition condition_join;

		if (position_from + 2 < tokens_array_size && tokens_array[position_from + 2].type == Type::JOIN)
		{
			if (position_from + 3 >= tokens_array_size)
			{
				cerr << "wrong number of parameters in JOIN construction" << endl;	throw;
			}

			if (tokens_array[position_from + 3].type != Type::NAME)
			{
				cerr << "unexpected token at position " << position_from + 3 << endl;	throw;
			}

			position_join = position_from + 2;
			table_name_join = tokens_array[position_from + 3].text;

			if (position_join + 2 < tokens_array_size && tokens_array[position_join + 2].type == Type::ON)
			{
				if (position_join + 5 >= tokens_array_size)
				{
					cerr << "wrong number of parameters in ON construction" << endl;	throw;
				}

				if (tokens_array[position_join + 3].type != Type::NAME)
				{
					cerr << "unexpected token at position " << position_join + 3 << endl;	throw;
				}

				if (tokens_array[position_join + 4].text != "=")
				{
					cerr << "unexpected token at position " << position_join + 4 << endl;	throw;
				}

				if (tokens_array[position_join + 5].type != Type::NAME)
				{
					cerr << "unexpected token at position " << position_join + 5 << endl;	throw;
				}

				string left = tokens_array[position_join + 3].text;
				string right = tokens_array[position_join + 5].text;

				condition_join = Condition(left, right);
			}
		}

		//WHERE

		int position_where;
		Condition condition_where;

		if (position_join == -1)
		{
			position_where = position_from + 2;
		}

		else
		{
			if (condition_join.get_type() == 0)
			{
				position_where = position_join + 2;
			}

			else
			{
				position_where = position_join + 6;
			}
		}

		if (position_where < tokens_array_size)
		{
			if (tokens_array[position_where].type != Type::WHERE)
			{
				cerr << "unexpected token at position " << position_where << endl;	throw;
			}

			if (position_where + 3 >= tokens_array_size)
			{
				cerr << "wrong number of parameters in WHERE construction" << endl;	throw;
			}

			if (tokens_array[position_where + 1].type != Type::NAME && tokens_array[position_where + 1].type != Type::VALUE)
			{
				cerr << "unexpected token at position " << position_where + 1 << endl;	throw;
			}

			if (tokens_array[position_where + 2].type != Type::OPERATOR)
			{
				cerr << "unexpected token at position " << position_where + 2 << endl;	throw;
			}

			if (tokens_array[position_where + 3].type != Type::NAME && tokens_array[position_where + 3].type != Type::VALUE)
			{
				cerr << "unexpected token at position " << position_where + 3 << endl;	throw;
			}

			string left = tokens_array[position_where + 1].text;
			string operation = tokens_array[position_where + 2].text;
			string right = tokens_array[position_where + 3].text;

			condition_where = Condition(left, right, operation);
		}

		//variables for SELECT

		string table_name = tokens_array[position_from + 1].text;

		bool select_all = tokens_array[position_from - 1].type == Type::ALL;

		Array<string> columns(select_all ? 0 : position_from / 2);

		if (!select_all)
		{
			for (int i = 1; i < position_from; i += 2)
			{
				columns[(i - 1) / 2] = tokens_array[i].text;
			}
		}

		//call SELECT command

		database.select(columns, table_name, table_name_join, condition_join, condition_where);
	}

	if (tokens_array[0].type == Type::DELETE)
	{
		if (tokens_array_size != 2 && tokens_array_size != 6)
		{
			cerr << "wrong number of parameters in DELETE command" << endl;	throw;
		}

		if (tokens_array[1].type != Type::NAME)
		{
			cerr << "unexpected token at position 1" << endl;	throw;
		}

		//variables for DELETE

		string table_name = tokens_array[1].text;

		Condition condition;

		if (tokens_array_size == 6)
		{
			if (tokens_array[2].type != Type::WHERE)
			{
				cerr << "unexpected token at position 2" << endl;	throw;
			}

			if (tokens_array[3].type != Type::NAME && tokens_array[3].type != Type::VALUE)
			{
				cerr << "unexpected token at position 3" << endl;	throw;
			}

			if (tokens_array[4].type != Type::OPERATOR)
			{
				cerr << "unexpected token at position 4" << endl;	throw;
			}

			if (tokens_array[5].type != Type::NAME && tokens_array[5].type != Type::VALUE)
			{
				cerr << "unexpected token at position 5" << endl;	throw;
			}

			string left = tokens_array[3].text;
			string operation = tokens_array[4].text;
			string right = tokens_array[5].text;

			condition = Condition(left, right, operation);
		}

		//call DELETE command

		database.erase(table_name, condition);
	}
}