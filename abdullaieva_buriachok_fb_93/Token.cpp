#include "Token.h"
#include "Join.h"

void lexer_analysis(const std::string& code, const Array<Token_Type>& token_types, std::deque<Token>& tokens_list)
{
	int token_types_size = token_types.size();

	int position = 0;

	while (position < code.length())
	{
		bool check = true;

		std::string current_code = code.substr(position);
		std::smatch matches;

		for (int i = 0; i < token_types_size; i++)
		{
			if (std::regex_search(current_code, matches, token_types[i].regex))
			{
				if (token_types[i].type != Token::Type::SPACE)
				{
					Token token(token_types[i].type, matches[0]);
					tokens_list.push_back(token);
				}

				position += matches[0].length();

				check = false;

				break;
			}
		}

		if (check)
		{
			throw std::exception(("error at position " + std::to_string(position)).c_str());
		}
	}
}



Condition::Type condition_type(const Token::Type& left, const Token::Type& right)
{
	if (left == Token::Type::NAME && right == Token::Type::NAME)
	{
		return Condition::Type::NAME_NAME;
	}

	else if (left == Token::Type::NAME || right == Token::Type::NAME)
	{
		return Condition::Type::NAME_VALUE;
	}

	else
	{
		return Condition::Type::VALUE_VALUE;
	}
}

void condition_operands(std::string& left, std::string& right, const Token::Type& left_t, const Token::Type& right_t)
{
	if (left_t == Token::Type::NAME && right_t == Token::Type::VALUE)
	{
		right = right.substr(1, right.length() - 2);
	}

	if (left_t == Token::Type::VALUE && right_t == Token::Type::NAME)
	{
		std::string temp = left;
		left = right;
		right = temp;

		right = right.substr(1, right.length() - 2);
	}

	if (left_t == Token::Type::VALUE && right_t == Token::Type::VALUE)
	{
		left = left.substr(1, left.length() - 2);
		right = right.substr(1, right.length() - 2);
	}
}

Condition::Operation condition_operation(const std::string& operation)
{
	if (operation == "=")
	{
		return Condition::Operation::EQUAL;
	}

	if (operation == "!=")
	{
		return Condition::Operation::NOT_EQUAL;
	}

	if (operation == "<")
	{
		return Condition::Operation::LESS;
	}

	if (operation == ">")
	{
		return Condition::Operation::GREATER;
	}

	if (operation == "<=")
	{
		return Condition::Operation::LESS_EQUAL;
	}

	if (operation == ">=")
	{
		return Condition::Operation::GREATER_EQUAL;
	}
}



void parser_analysis(Database& database, const Array<Token>& tokens_array)
{
	int tokens_array_size = tokens_array.size();

	if (tokens_array_size == 0)
	{
		throw std::exception("empty std::string");
	}

	if (tokens_array[0].type != Token::Type::CREATE && tokens_array[0].type != Token::Type::INSERT && tokens_array[0].type != Token::Type::SELECT && tokens_array[0].type != Token::Type::DELETE)
	{
		throw std::exception("unknown command");
	}

	if (tokens_array[0].type == Token::Type::CREATE)
	{
		if (tokens_array_size < 5)
		{
			throw std::exception("wrong number of parameters in CREATE command");
		}

		if (tokens_array[1].type != Token::Type::NAME)
		{
			throw std::exception("unexpected token at position 1");
		}

		if (tokens_array[2].type != Token::Type::LPAR)
		{
			throw std::exception("unexpected token at position 2");
		}

		if (tokens_array[3].type != Token::Type::NAME)
		{
			throw std::exception("unexpected token at position 3");
		}

		if (tokens_array[tokens_array_size - 1].type != Token::Type::RPAR)
		{
			throw std::exception(("unexpected token at position " + std::to_string(tokens_array_size - 1)).c_str());
		}

		std::deque<std::string> columns_list;
		std::deque<std::string> indexes_list;

		columns_list.push_back(tokens_array[3].text);

		Token::Type previous_token = Token::Type::NAME;

		for (int i = 4; i < tokens_array_size - 1; i++)
		{
			Token::Type current_token = tokens_array[i].type;

			if (previous_token == Token::Type::NAME && current_token != Token::Type::INDEXED && current_token != Token::Type::COMMA)
			{
				throw std::exception(("unexpected token at position " + std::to_string(i)).c_str());
			}

			if (previous_token == Token::Type::INDEXED && current_token != Token::Type::COMMA)
			{
				throw std::exception(("unexpected token at position " + std::to_string(i)).c_str());
			}

			if (previous_token == Token::Type::COMMA && current_token != Token::Type::NAME)
			{
				throw std::exception(("unexpected token at position " + std::to_string(i)).c_str());
			}

			if (current_token == Token::Type::NAME)
			{
				columns_list.push_back(tokens_array[i].text);
			}

			if (current_token == Token::Type::INDEXED)
			{
				indexes_list.push_back(tokens_array[i - 1].text);
			}

			previous_token = current_token;
		}

		//variables for CREATE

		const std::string& table_name = tokens_array[1].text;

		//call CREATE command

		database.create(table_name, Array<std::string>(columns_list), Array<std::string>(indexes_list));
	}

	if (tokens_array[0].type == Token::Type::INSERT)
	{
		if (tokens_array_size < 5 || tokens_array_size % 2 == 0)
		{
			throw std::exception("wrong number of parameters in INSERT command");
		}

		Array<Token::Type> pattern(tokens_array_size);

		pattern[0] = Token::Type::INSERT;
		pattern[1] = Token::Type::NAME;
		pattern[2] = Token::Type::LPAR;
		pattern[tokens_array_size - 1] = Token::Type::RPAR;

		for (int i = 3; i < tokens_array_size - 1; i++)
		{
			pattern[i] = (i % 2 ? Token::Type::VALUE : Token::Type::COMMA);
		}

		for (int i = 0; i < tokens_array_size; i++)
		{
			if (tokens_array[i].type != pattern[i])
			{
				throw std::exception(("unexpected token at position " + std::to_string(i)).c_str());
			}
		}

		//variables for INSERT

		const std::string& table_name = tokens_array[1].text;

		int values_size = (tokens_array_size - 3) / 2;

		Array<std::string> values(values_size);

		for (int i = 3; i < tokens_array_size; i += 2)
		{
			const std::string& text = tokens_array[i].text;

			values[(i - 3) / 2] = text.substr(1, text.length() - 2);
		}

		//call INSERT command

		database.insert(table_name, values);
	}

	if (tokens_array[0].type == Token::Type::SELECT)
	{
		if (tokens_array_size < 4)
		{
			throw std::exception("wrong number of parameters in SELECT command");
		}

		if (tokens_array[1].type != Token::Type::ALL && tokens_array[1].type != Token::Type::NAME)
		{
			throw std::exception("unexpected token at position 1");
		}

		//FROM

		int position_from = -1;

		if (tokens_array[1].type == Token::Type::ALL)
		{
			if (tokens_array[2].type != Token::Type::FROM)
			{
				throw std::exception("unexpected token at position 2");
			}

			position_from = 2;
		}

		if (tokens_array[1].type == Token::Type::NAME)
		{
			for (int i = 2; i < tokens_array_size; i++)
			{
				if (i % 2 == 0 && tokens_array[i].type == Token::Type::FROM)
				{
					position_from = i;

					break;
				}

				if (tokens_array[i].type != (i % 2 ? Token::Type::NAME : Token::Type::COMMA))
				{
					throw std::exception(("unexpected token at position " + std::to_string(i)).c_str());
				}
			}
		}

		if (position_from == -1)
		{
			throw std::exception("missed keyword FROM");
		}

		if (tokens_array_size == position_from + 1)
		{
			throw std::exception("wrong number of parameters in FROM construction");
		}

		if (tokens_array[position_from + 1].type != Token::Type::NAME)
		{
			throw std::exception(("unexpected token at position " + std::to_string(position_from + 1)).c_str());
		}

		//JOIN

		int position_join = -1;
		std::string table_name_join = "";
		Join join;

		if (position_from + 2 < tokens_array_size && tokens_array[position_from + 2].type == Token::Type::JOIN)
		{
			if (position_from + 3 >= tokens_array_size)
			{
				throw std::exception("wrong number of parameters in JOIN construction");
			}

			if (tokens_array[position_from + 3].type != Token::Type::NAME)
			{
				throw std::exception(("unexpected token at position " + std::to_string(position_from + 3)).c_str());
			}

			position_join = position_from + 2;
			table_name_join = tokens_array[position_from + 3].text;

			if (position_join + 2 < tokens_array_size && tokens_array[position_join + 2].type == Token::Type::ON)
			{
				if (position_join + 5 >= tokens_array_size)
				{
					throw std::exception("wrong number of parameters in ON construction");
				}

				if (tokens_array[position_join + 3].type != Token::Type::NAME)
				{
					throw std::exception(("unexpected token at position " + std::to_string(position_join + 3)).c_str());
				}

				if (tokens_array[position_join + 4].text != "=")
				{
					throw std::exception(("unexpected token at position " + std::to_string(position_join + 4)).c_str());
				}

				if (tokens_array[position_join + 5].type != Token::Type::NAME)
				{
					throw std::exception(("unexpected token at position " + std::to_string(position_join + 5)).c_str());
				}

				const std::string& left = tokens_array[position_join + 3].text;
				const std::string& right = tokens_array[position_join + 5].text;

				join = Join(left, right);
			}
		}

		//WHERE

		int position_where;
		Condition condition;

		if (position_join == -1)
		{
			position_where = position_from + 2;
		}

		else
		{
			if (join.type == Join::Type::JOIN)
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
			if (tokens_array[position_where].type != Token::Type::WHERE)
			{
				throw std::exception(("unexpected token at position " + std::to_string(position_where)).c_str());
			}

			if (position_where + 3 >= tokens_array_size)
			{
				throw std::exception("wrong number of parameters in WHERE construction");
			}

			if (tokens_array[position_where + 1].type != Token::Type::NAME && tokens_array[position_where + 1].type != Token::Type::VALUE)
			{
				throw std::exception(("unexpected token at position " + std::to_string(position_where + 1)).c_str());
			}

			if (tokens_array[position_where + 2].type != Token::Type::OPERATOR)
			{
				throw std::exception(("unexpected token at position " + std::to_string(position_where + 2)).c_str());
			}

			if (tokens_array[position_where + 3].type != Token::Type::NAME && tokens_array[position_where + 3].type != Token::Type::VALUE)
			{
				throw std::exception(("unexpected token at position " + std::to_string(position_where + 3)).c_str());
			}

			Condition::Type type = condition_type(tokens_array[position_where + 1].type, tokens_array[position_where + 3].type);
			std::string left = tokens_array[position_where + 1].text;
			std::string right = tokens_array[position_where + 3].text;
			condition_operands(left, right, tokens_array[position_where + 1].type, tokens_array[position_where + 3].type);
			Condition::Operation operation = condition_operation(tokens_array[position_where + 2].text);

			condition = Condition(type, left, right, operation);
		}

		//variables for SELECT

		const std::string& table_name = tokens_array[position_from + 1].text;

		bool select_all = tokens_array[position_from - 1].type == Token::Type::ALL;

		Array<std::string> columns(select_all ? 0 : position_from / 2);

		if (!select_all)
		{
			for (int i = 1; i < position_from; i += 2)
			{
				columns[(i - 1) / 2] = tokens_array[i].text;
			}
		}

		//call SELECT command

		database.select(columns, table_name, table_name_join, join, condition);
	}

	if (tokens_array[0].type == Token::Type::DELETE)
	{
		if (tokens_array_size != 2 && tokens_array_size != 6)
		{
			throw std::exception("wrong number of parameters in DELETE command");
		}

		if (tokens_array[1].type != Token::Type::NAME)
		{
			throw std::exception("unexpected token at position 1");
		}

		//variables for DELETE

		const std::string& table_name = tokens_array[1].text;

		Condition condition;

		if (tokens_array_size == 6)
		{
			if (tokens_array[2].type != Token::Type::WHERE)
			{
				throw std::exception("unexpected token at position 2");
			}

			if (tokens_array[3].type != Token::Type::NAME && tokens_array[3].type != Token::Type::VALUE)
			{
				throw std::exception("unexpected token at position 3");
			}

			if (tokens_array[4].type != Token::Type::OPERATOR)
			{
				throw std::exception("unexpected token at position 4");
			}

			if (tokens_array[5].type != Token::Type::NAME && tokens_array[5].type != Token::Type::VALUE)
			{
				throw std::exception("unexpected token at position 5");
			}

			Condition::Type type = condition_type(tokens_array[3].type, tokens_array[5].type);
			std::string left = tokens_array[3].text;
			std::string right = tokens_array[5].text;
			condition_operands(left, right, tokens_array[3].type, tokens_array[5].type);
			Condition::Operation operation = condition_operation(tokens_array[4].text);

			condition = Condition(type, left, right, operation);
		}

		//call DELETE command

		database.erase(table_name, condition);
	}
}