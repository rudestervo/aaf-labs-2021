#pragma once
#include <string>
#include <regex>
#include <deque>
#include "Array.h"
#include "Database.h"
#include "Condition.h"

struct Token
{
	enum class Type
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

	Type type;
	std::string text;

	Token()
	{
		this->type = Type::SPACE;
		this->text = "";
	}

	Token(Type type, const std::string& text)
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





struct Token_Type
{
	Token::Type type;
	std::regex regex;

	Token_Type()
	{
		this->type = Token::Type::SPACE;
	}

	Token_Type(Token::Type type, const std::regex& regex)
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



void lexer_analysis(const std::string& code, const Array<Token_Type>& token_types, std::deque<Token>& tokens_list);

Condition::Type condition_type(const Token::Type& left, const Token::Type& right);

void condition_operands(std::string& left, std::string& right, const Token::Type& left_t, const Token::Type& right_t);

Condition::Operation condition_operation(const std::string& operation);

void parser_analysis(Database& database, const Array<Token>& tokens_array);