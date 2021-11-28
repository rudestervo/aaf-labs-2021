#pragma once
#include <string>

struct Join
{
	enum class Type
	{
		JOIN,
		JOIN_ON
	};

	std::string left, right;
	Type type;

	Join()
	{
		this->left = this->right = "";
		this->type = Type::JOIN;
	}

	Join(const std::string& left, const std::string& right)
	{
		this->left = left;
		this->right = right;
		this->type = this->left == "" || this->right == "" ? Type::JOIN : Type::JOIN_ON;
	}

	Join(const Join& join)
	{
		this->left = join.left;
		this->right = join.right;
		this->type = join.type;
	}
};