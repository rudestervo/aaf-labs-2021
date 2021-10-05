#pragma once
#include <iostream>

using namespace std;

class Condition
{
private:
	string left, right, operation;

public:
	Condition()
	{
		this->left = this->right = "`1`";
		this->operation = "=";
	}

	Condition(string left, string right, string operation = "=")
	{
		this->operation = operation;

		bool change = left[0] == '`' && right[0] != '`';

		if (change)//VALUE ? NAME -> NAME ? VALUE
		{
			this->left = right;
			this->right = left;

			if (operation[0] == '<' || operation[0] == '>')
			{
				this->operation[0] = operation[0] == '<' ? '>' : '<';
			}
		}

		else
		{
			this->left = left;
			this->right = right;
		}
	}

	Condition(const Condition& condition)
	{
		this->left = condition.left;
		this->right = condition.right;
		this->operation = condition.operation;
	}

	int get_type() const
	{
		if (this->left[0] == '`' && this->right[0] == '`')//VALUE ? VALUE
		{
			return 0;
		}

		else if (this->left[0] == '`' || this->right[0] == '`')//NAME ? VALUE
		{
			return 1;
		}

		else//NAME ? NAME
		{
			return 2;
		}
	}

	string get_left() const
	{
		return this->left;
	}

	string get_right() const
	{
		return this->right;
	}

	string get_operation() const
	{
		return this->operation;
	}

	bool get_value(string left_value, string right_value) const//NAME ? NAME
	{
		if (operation == "=")
		{
			return left_value == right_value;
		}

		if (operation == "!=")
		{
			return left_value != right_value;
		}

		if (operation == "<")
		{
			return left_value < right_value;
		}

		if (operation == ">")
		{
			return left_value > right_value;
		}

		if (operation == "<=")
		{
			return left_value <= right_value;
		}

		if (operation == ">=")
		{
			return left_value >= right_value;
		}
	}

	bool get_value(string left_value) const//NAME ? VALUE
	{
		string right_value = this->right.substr(1, this->right.length() - 2);

		return this->get_value(left_value, right_value);
	}

	bool get_value() const//VALUE ? VALUE
	{
		string left_value = this->left.substr(1, this->left.length() - 2);
		string right_value = this->right.substr(1, this->right.length() - 2);

		return this->get_value(left_value, right_value);
	}
};