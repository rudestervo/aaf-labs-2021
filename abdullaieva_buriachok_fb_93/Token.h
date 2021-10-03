#pragma once
#include <iostream>
#include <regex>
#include "List.h"
#include "Array.h"
#include "Database.h"
#include "Condition.h"

using namespace std;

struct Token_Type
{
	string name, regex;

	Token_Type()
	{
		this->name = "";
		this->regex = "";
	}

	Token_Type(const Token_Type& token_type)
	{
		this->name = token_type.name;
		this->regex = token_type.regex;
	}

	Token_Type(string name, string regex)
	{
		this->name = name;
		this->regex = regex;
	}
};





struct Token
{
	Token_Type type;
	string text;
	int position;

	Token()
	{
		this->text = "";
		this->position = 0;
	}

	Token(const Token& token)
	{
		this->type = token.type;
		this->text = token.text;
		this->position = token.position;
	}

	Token(Token_Type& type, string text, int position)
	{
		this->type = type;
		this->text = text;
		this->position = position;
	}
};





void lexer_analysis(string code, Token_Type token_types_array[], const int token_types_size, List<Token>& tokens_list)
{
	int position = 0;

	while (position < code.length())
	{
		bool check = true;//не подходит под описание ни одного из токенов

		string current_code = code.substr(position);
		smatch matches;

		for (int i = 0; i < token_types_size; i++)
		{
			regex regular("^" + token_types_array[i].regex);//ищем токен в начале строки

			if (regex_search(current_code, matches, regular))
			{
				if (token_types_array[i].name != "SPACE")//не добавляем токеты пробелов
				{
					Token token(token_types_array[i], matches[0], position);
					tokens_list.push_back(token);
				}

				position += matches[0].length();//перемещаем ползунок

				check = false;

				break;
			}
		}

		if (check)//не нашли ни одного токена
		{
			cerr << "Ошибка на позиции " << position;	throw;
		}
	}
}





void parser_analysis(Database& database, const Array<Token>& tokens_array)
{
	int tokens_array_size = tokens_array.size();
	
	if (tokens_array_size > 0)
	{
		if (tokens_array[0].type.name == "CREATE")//команда CREATE
		{
			if (tokens_array_size < 5)
			{
				cerr << "неправильное количество параметров около конструкции CREATE";	throw;
			}

			else
			{
				if (tokens_array[1].type.name != "NAME")
				{
					cerr << "неожиданный токен на позиции 1";	throw;
				}

				else if (tokens_array[2].type.name != "LPAR")
				{
					cerr << "неожиданный токен на позиции 2";	throw;
				}

				else if (tokens_array[3].type.name != "NAME")
				{
					cerr << "неожиданный токен на позиции 3";	throw;
				}

				else if (tokens_array[tokens_array_size - 1].type.name != "RPAR")
				{
					cerr << "неожиданный токен на позиции " << tokens_array_size - 1;	throw;
				}

				else
				{
					List<string> columns_list;
					List<string> indexes_list;

					columns_list.push_back(tokens_array[3].text);

					string previous_token = "NAME";

					for (int i = 4; i < tokens_array_size - 1; i++)
					{
						string current_token = tokens_array[i].type.name;

						if (previous_token == "NAME" && current_token != "INDEXED" && current_token != "COMMA")//после NAME был токен не INDEXED и не COMMA
						{
							cerr << "неожиданный токен на позиции " << i;	throw;
						}

						else if (previous_token == "INDEXED" && current_token != "COMMA")//после INDEXED был токен не COMMA
						{
							cerr << "неожиданный токен на позиции " << i;	throw;
						}

						else if (previous_token == "COMMA" && current_token != "NAME")//после COMMA был токен не NAME
						{
							cerr << "неожиданный токен на позиции " << i;	throw;
						}

						if (current_token == "NAME")
						{
							columns_list.push_back(tokens_array[i].text);
						}

						if (current_token == "INDEXED")
						{
							indexes_list.push_back(tokens_array[i - 1].text);
						}

						previous_token = current_token;
					}

					//переменные для вызова команды CREATE

					string table_name = tokens_array[1].text;

					Array<string> columns = columns_list.to_array();
					Array<string> indexes = indexes_list.to_array();

					//вызов команды CREATE

					database.create(table_name, columns, indexes);
				}
			}
		}

		else if (tokens_array[0].type.name == "INSERT")//команда INSERT
		{
			if (tokens_array_size < 5)
			{
				cerr << "неправильное количество параметров около конструкции INSERT";	throw;
			}

			else
			{
				Array<string> pattern(tokens_array_size);

				pattern[0] = "INSERT";
				pattern[1] = "NAME";
				pattern[2] = "LPAR";
				pattern[tokens_array_size - 1] = "RPAR";

				for (int i = 3; i < tokens_array_size - 1; i++)
				{
					pattern[i] = (i % 2 ? "VALUE" : "COMMA");
				}

				for (int i = 0; i < tokens_array_size; i++)
				{
					if (tokens_array[i].type.name != pattern[i])
					{
						cerr << "неожиданный токен на позиции " << i;	throw;
					}
				}

				//переменные для вызова команды INSERT

				string table_name = tokens_array[1].text;

				int values_size = (tokens_array_size - 3) / 2;

				Array<string> values(values_size);

				for (int i = 3; i < tokens_array_size; i+=2)
				{
					string text = tokens_array[i].text;
					
					values[(i - 3) / 2] = text.substr(1, text.length() - 2);//убираем кавычки
				}

				//вызов команды INSERT

				database.insert(table_name, values);
			}
		}

		else if (tokens_array[0].type.name == "DELETE")//команда DELETE
		{
			if (tokens_array_size != 2 && tokens_array_size != 6)
			{
				cerr << "неправильное количество параметров около конструкции DELETE";	throw;
			}

			else
			{
				if (tokens_array[1].type.name != "NAME")
				{
					cerr << "неожиданный токен на позиции 1";	throw;
				}

				else
				{
					//переменные для вызова команды DELETE

					string table_name = tokens_array[1].text;

					Condition condition;

					if (tokens_array_size == 6)
					{
						if (tokens_array[2].type.name != "WHERE")
						{
							cerr << "неожиданный токен на позиции 2";	throw;
						}

						else if (tokens_array[3].type.name != "NAME" && tokens_array[3].type.name != "VALUE")
						{
							cerr << "неожиданный токен на позиции 3";	throw;
						}

						else if (tokens_array[4].type.name != "OPERATOR")
						{
							cerr << "неожиданный токен на позиции 4";	throw;
						}

						else if (tokens_array[5].type.name != "NAME" && tokens_array[5].type.name != "VALUE")
						{
							cerr << "неожиданный токен на позиции 5";	throw;
						}

						else//правильная конструкция WHERE
						{
							string left = tokens_array[3].text;
							string operation = tokens_array[4].text;
							string right = tokens_array[5].text;

							condition = Condition(left, right, operation);
						}
					}

					//вызов команды DELETE

					database.erase(table_name, condition);
				}
			}
		}

		else if (tokens_array[0].type.name == "SELECT")//команда SELECT
		{
			if (tokens_array_size < 4)
			{
				cerr << "неправильное количество параметров около конструкции SELECT";	throw;
			}

			else
			{
				if (tokens_array[1].type.name != "ALL" && tokens_array[1].type.name != "NAME")
				{
					cerr << "неожиданный токен на позиции 1";	throw;
				}

				else
				{
					//FROM

					int position_from = -1;

					if (tokens_array[1].type.name == "ALL")
					{
						if (tokens_array[2].type.name != "FROM")
						{
							cerr << "неожиданный токен на позиции " << 2;	throw;
						}

						else
						{
							position_from = 2;
						}
					}

					else
					{
						for (int i = 2; i < tokens_array_size; i++)
						{
							if (tokens_array[i].type.name == "FROM")
							{
								position_from = i;
								break;
							}

							if (tokens_array[i].type.name != (i % 2 ? "NAME" : "COMMA"))
							{
								cerr << "неожиданный токен на позиции " << i;	throw;
							}
						}
					}

					if (position_from == -1)
					{
						cerr << "отсутствует ключевое слово FROM";	throw;
					}

					else if (tokens_array_size - 1 == position_from)//FROM последний токен
					{
						cerr << "неправильное количество параметров около конструкции FROM";	throw;
					}

					else if (tokens_array[position_from + 1].type.name != "NAME")
					{
						cerr << "неожиданный токен на позиции " << position_from + 1;	throw;
					}

					else
					{
						//JOIN

						int position_join = -1;
						string table_name_join = "";
						Condition condition_join;

						if (position_from + 2 < tokens_array_size)//хотя бы 2 токен после FROM (JOIN или WHERE)
						{
							if (tokens_array[position_from + 2].type.name == "JOIN")
							{
								if (position_from + 3 >= tokens_array_size)//не полная конструкция JOIN
								{
									cerr << "неправильное количество параметров около конструкции JOIN";	throw;
								}

								else if (tokens_array[position_from + 3].type.name != "NAME")
								{
									cerr << "неожиданный токен на позиции " << position_from + 3;	throw;
								}

								else
								{
									position_join = position_from + 2;
									table_name_join = tokens_array[position_from + 3].text;

									if (position_join + 2 < tokens_array_size)//хотя бы 2 токен после JOIN (ON)
									{
										if (tokens_array[position_join + 2].type.name == "ON")
										{
											if (position_join + 5 >= tokens_array_size)//не полная конструкция ON
											{
												cerr << "неправильное количество параметров около конструкции ON";	throw;
											}

											else
											{
												if (tokens_array[position_join + 3].type.name != "NAME")
												{
													cerr << "неожиданный токен на позиции " << position_join + 3;	throw;
												}

												else if (tokens_array[position_join + 4].text != "=")
												{
													cerr << "неожиданный токен на позиции " << position_join + 4;	throw;
												}

												else if (tokens_array[position_join + 5].type.name != "NAME")
												{
													cerr << "неожиданный токен на позиции " << position_join + 5;	throw;
												}

												else//правильная конструкция JOIN ON
												{
													string left = tokens_array[position_join + 3].text;
													string right = tokens_array[position_join + 5].text;

													condition_join = Condition(left, right);
												}
											}
										}
									}
								}
							}
						}

						//WHERE

						int position_where;//на какой позиции он может быть
						Condition condition_where;

						if (position_join == -1)//не нашли JOIN
						{
							position_where = position_from + 2;
						}

						else//нашли JOIN
						{
							if (condition_join.get_type() == 0)//VALUE ? VALUE
							{
								position_where = position_join + 2;
							}

							else//JOIN ON
							{
								position_where = position_join + 6;
							}
						}

						if (position_where < tokens_array_size)//хотя бы 1 токен для WHERE
						{
							if (tokens_array[position_where].type.name != "WHERE")
							{
								cerr << "неожиданный токен на позиции " << position_where;	throw;
							}

							else
							{
								if (position_where + 3 >= tokens_array_size)
								{
									cerr << "неправильное количество параметров около конструкции WHERE";	throw;
								}

								else
								{
									if (tokens_array[position_where + 1].type.name != "NAME" && tokens_array[position_where + 1].type.name != "VALUE")
									{
										cerr << "неожиданный токен на позиции " << position_where + 1;	throw;
									}

									else if (tokens_array[position_where + 2].type.name != "OPERATOR")
									{
										cerr << "неожиданный токен на позиции " << position_where + 2;	throw;
									}

									else if (tokens_array[position_where + 3].type.name != "NAME" && tokens_array[position_where + 3].type.name != "VALUE")
									{
										cerr << "неожиданный токен на позиции " << position_where + 3;	throw;
									}

									else//правильная конструкция WHERE
									{
										string left = tokens_array[position_where + 1].text;
										string operation = tokens_array[position_where + 2].text;
										string right = tokens_array[position_where + 3].text;

										condition_where = Condition(left, right, operation);
									}
								}
							}
						}

						//переменные для вызова команды SELECT

						string table_name = tokens_array[position_from + 1].text;

						bool select_all = tokens_array[position_from - 1].type.name == "ALL";

						Array<string> columns(select_all ? 0 : position_from / 2);

						if (!select_all)
						{
							for (int i = 1; i < position_from; i += 2)
							{
								columns[(i - 1) / 2] = tokens_array[i].text;
							}
						}

						//вызов команды SELECT

						database.select(columns, table_name, table_name_join, condition_join, condition_where);
					}
				}
			}
		}

		else
		{
			cerr << "неизвестная команда";	throw;
		}
	}

	else
	{
		cerr << "пустая строка";	throw;
	}
}





void start(Database& database, string code)
{
	Token_Type token_types_array[] = {
		{"CREATE", "[cC][rR][eE][aA][tT][eE]"},
		{"INSERT", "[iI][nN][sS][eE][rR][tT]([ \t\n\r]{0,}[iI][nN][tT][oO])?"},
		{"SELECT", "[sS][eE][lL][eE][cC][tT]"},
		{"DELETE", "[dD][eE][lL][eE][tT][eE]([ \t\n\r]{0,}[fF][rR][oO][mM])?"},
		{"INDEXED", "[iI][nN][dD][eE][xX][eE][dD]"},
		{"FROM", "[fF][rR][oO][mM]"},
		{"JOIN", "[jJ][oO][iI][nN]"},
		{"ON", "[oO][nN]"},
		{"WHERE", "[wW][hH][eE][rR][eE]"},
		{"SPACE", "[ \\t\\n\\r]"},
		{"NAME", "[a-zA-Z][a-zA-Z0-9_]{0,}"},
		{"VALUE", "\\`[a-zA-Z0-9_]{1,}\\`"},
		{"LPAR", "\\("},
		{"RPAR", "\\)"},
		{"COMMA", ","},
		{"ALL", "\\*"},
		{"OPERATOR", "(=|!=|<=|>=|<|>)"},
		{"EXIT", "\\.[eE][xX][iI][tT]"},
		//{"SEMICOLON", ";"},
	};

	int token_types_size = sizeof(token_types_array) / sizeof(*token_types_array);

	cout << code << endl;
	
	List<Token> tokens_list;

	lexer_analysis(code, token_types_array, token_types_size, tokens_list);

	Array<Token> tokens_array = tokens_list.to_array();

	/*int tokens_array_size = tokens_array.size();

	for (int i = 0; i < tokens_array_size; i++)
	{
		cout << "Type: " << tokens_array[i].type.name << "\tText: " << tokens_array[i].text  << endl;
	}*/

	parser_analysis(database, tokens_array);

	cout << endl;
}