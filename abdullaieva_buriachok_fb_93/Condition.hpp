#pragma once

using namespace std;

class Condition
{
public:
	enum Operation
	{
		EQUAL,
		NOT_EQUAL,
		LESS,
		GREATER,
		LESS_EQUAL,
		GREATER_EQUAL,
	};

	enum Type
	{
		VALUE_VALUE,
		NAME_VALUE,
		NAME_NAME
	};

private:
	string left, right;
	Operation operation;

public:
	Condition()
	{
		this->left = this->right = "`1`";
		this->operation = Operation::EQUAL;
	}

	Condition(const string& left, const string& right, Operation operation = Operation::EQUAL)
	{
		this->operation = operation;

		if (left[0] == '`' && right[0] != '`')
		{
			this->left = right;
			this->right = left;
			
			if (operation == Condition::Operation::LESS)
			{
				this->operation = Operation::GREATER;
			}

			else if (operation == Condition::Operation::GREATER)
			{
				this->operation = Operation::LESS;
			}

			else if (operation == Condition::Operation::LESS_EQUAL)
			{
				this->operation = Operation::GREATER_EQUAL;
			}

			else if (operation == Condition::Operation::GREATER_EQUAL)
			{
				this->operation = Operation::LESS_EQUAL;
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

	Type get_type() const
	{
		if (this->left[0] == '`' && this->right[0] == '`')
		{
			return Type::VALUE_VALUE;
		}

		if (this->left[0] == '`' || this->right[0] == '`')
		{
			return Type::NAME_VALUE;
		}

		else
		{
			return Type::NAME_NAME;
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

	Operation get_operation() const
	{
		return this->operation;
	}

	bool compare(const string& left_value, const string& right_value) const
	{
		if (this->operation == Operation::EQUAL)
		{
			return left_value == right_value;
		}

		if (this->operation == Operation::NOT_EQUAL)
		{
			return left_value != right_value;
		}

		if (this->operation == Operation::LESS)
		{
			return left_value < right_value;
		}

		if (this->operation == Operation::GREATER)
		{
			return left_value > right_value;
		}

		if (this->operation == Operation::LESS_EQUAL)
		{
			return left_value <= right_value;
		}

		if (this->operation == Operation::GREATER_EQUAL)
		{
			return left_value >= right_value;
		}
	}

	bool compare(const string& left_value) const
	{
		string right_value = this->right.substr(1, this->right.length() - 2);

		return this->compare(left_value, right_value);
	}

	bool compare() const
	{
		string left_value = this->left.substr(1, this->left.length() - 2);
		string right_value = this->right.substr(1, this->right.length() - 2);

		return this->compare(left_value, right_value);
	}
};

Condition::Operation reverse_operation(Condition::Operation operation)
{
	if (operation == Condition::Operation::EQUAL)
	{
		return Condition::Operation::NOT_EQUAL;
	}

	if (operation == Condition::Operation::NOT_EQUAL)
	{
		return Condition::Operation::EQUAL;
	}

	if (operation == Condition::Operation::LESS)
	{
		return Condition::Operation::GREATER_EQUAL;
	}

	if (operation == Condition::Operation::GREATER)
	{
		return Condition::Operation::LESS_EQUAL;
	}

	if (operation == Condition::Operation::LESS_EQUAL)
	{
		return Condition::Operation::GREATER;
	}

	if (operation == Condition::Operation::GREATER_EQUAL)
	{
		return Condition::Operation::LESS;
	}
}

Condition::Operation to_operation(const string& operation)
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