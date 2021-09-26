#include <iostream>
#include <vector>
#include <regex>

using namespace std;

struct Token_Type
{
	string name, regex;

	Token_Type()
	{
		this->name = "";
		this->regex = "";
	}

	Token_Type(string name, string regex)
	{
		this->name = name;
		this->regex = regex;
	}
};

Token_Type token_types_list[] = {
	{"CREATE", "CREATE"},
	{"INDEXED", "INDEXED"},
	{"INSERT", "INSERT( INTO)?"},
	{"SELECT", "SELECT"},
	{"DELETE", "DELETE( FROM)?"},
	{"FROM", "FROM"},
	{"WHERE", "WHERE"},
	{"JOIN", "JOIN"},
	{"ON", "ON"},
	{"SPACE", "[ \\t\\n\\r]"},
	{"NAME", "[a-z_]{1,}"},
	{"VALUE", "\\`[a-zA-Z0-9_]{1,}\\`"},
	{"LPAR", "\\("},
	{"RPAR", "\\)"},
	{"COMMA", ","},
	{"ALL", "\\*"},
	{"EQUAL", "="},
	{"NOT_EQUAL", "!="},
	{"GREATER_EQUAL", ">="},
	{"LESS_EQUAL", "<="},
	{"GREATER", ">"},
	{"LESS", "<"},
	{"SEMICOLON", ";"},
};

const int token_types_size = sizeof(token_types_list) / sizeof(*token_types_list);

string token_type_regex(string type)
{
	for (int i = 0; i < token_types_size; i++)
	{
		if (token_types_list[i].name == type)
		{
			return token_types_list[i].regex;
		}
	}

	cerr << "Unknown token type" << endl;

	throw;
}

struct Token
{
	Token_Type type;
	string text;
	int position;

	Token(Token_Type &type, string text, int position)
	{
		this->type = type;
		this->text = text;
		this->position = position;
	}

	void print()
	{
		cout << "Type: " << this->type.name << "\tText: " << this->text << "\tPosition: " << this->position << endl;
	}
};

class Lexer
{
private:
	string code;
	int position;
	vector<Token> token_list;

public:
	Lexer(string code)
	{
		this->code = code;
		position = 0;
	}

	vector<Token> analysis()
	{
		while (this->position < this->code.length())
		{
			bool check = true;
			
			string code = this->code.substr(this->position);
			smatch matches;

			for (int i = 0; i < token_types_size; i++)
			{
				regex regular("^" + token_types_list[i].regex);

				if (regex_search(code, matches, regular))
				{
					if (token_types_list[i].name != "SPACE")
					{
						Token token(token_types_list[i], matches[0], this->position);
						this->token_list.push_back(token);
					}

					this->position += matches[0].length();

					check = false;
					
					break;
				}
			}

			if (check)
			{
				cerr << "Error on position " << this->position << endl;

				throw;
			}
		}

		return this->token_list;
	}
};

int main()
{
	string code = "SELECT cat_id, cat_owner_id FROM cats WHERE name = `Murzik`; ";

	//getline(cin, code, ';');	code += ';';

	Lexer lexer(code);

	vector<Token> token_list = lexer.analysis();

	cout << code << endl;
	
	for (int i = 0; i < token_list.size(); i++)
	{
		token_list[i].print();
	}

	return 0;
}