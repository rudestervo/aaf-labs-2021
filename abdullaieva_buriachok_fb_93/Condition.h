#pragma once
#include <string>

struct Condition
{
	enum class Type
	{
		VALUE_VALUE,
		NAME_VALUE,
		NAME_NAME
	};

	enum class Operation
	{
		EQUAL,
		NOT_EQUAL,
		LESS,
		GREATER,
		LESS_EQUAL,
		GREATER_EQUAL,
	};

	Type type;
	std::string left, right;
	Operation operation;

	Condition()
	{
		this->type = Type::VALUE_VALUE;
		this->left = this->right = "1";
		this->operation = Operation::EQUAL;
	}

	Condition(Type type, const std::string& left, const std::string& right, Operation operation)
	{
		this->type = type;
		this->left = left;
		this->right = right;
		this->operation = operation;
	}

	Condition(const Condition& condition)
	{
		this->left = condition.left;
		this->right = condition.right;
		this->operation = condition.operation;
		this->type = condition.type;
	}

	bool compare(const std::string& left_value, const std::string& right_value) const
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

	bool compare(const std::string& left_value) const
	{
		return this->compare(left_value, this->right);
	}

	bool compare() const
	{
		return this->compare(this->left, this->right);
	}

	Condition reverse() const
	{
		Condition result = *this;
		
		if (this->operation == Operation::EQUAL)
		{
			result.operation = Operation::NOT_EQUAL;
		}

		if (this->operation == Operation::NOT_EQUAL)
		{
			result.operation = Operation::EQUAL;
		}

		if (this->operation == Operation::LESS)
		{
			result.operation = Operation::GREATER_EQUAL;
		}

		if (this->operation == Operation::GREATER)
		{
			result.operation = Operation::LESS_EQUAL;
		}

		if (this->operation == Operation::LESS_EQUAL)
		{
			result.operation = Operation::GREATER;
		}

		if (this->operation == Operation::GREATER_EQUAL)
		{
			result.operation = Operation::LESS;
		}

		return result;
	}
};