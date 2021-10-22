#pragma once
#include <iostream>
#include <deque>
#include <map>
#include "Array.hpp"
#include "Condition.hpp"

class Table
{
private:
	Array<string> columns;
	map<string, int> columns_tree;

	map<string, map<string, int>> indexes;

	deque<Array<string>> values;

public:
	Table();

	Table(const Array<string>& columns);

	Table(const Array<string>& columns, const Array<string>& indexes);

	Table(const Array<string>& columns, const map<string, map<string, int>>& indexes);

	Table(const Array<string>& columns, const deque<Array<string>>& values);

	Table(const Array<string>& columns, const map<string, map<string, int>>& indexes, const deque<Array<string>>& values);

	Table(const Table& table);

	bool insert(const Array<string>& values);

	void erase(const int row_index);

	int erase(const Condition& condition);

	Table join(const Table& table, const Condition& condition) const;

	Table where(const Condition& condition) const;

	Table select(const Array<string>& columns) const;

	void print() const;
};





class Database
{
private:
	map<string, Table> tables;

public:
	void create(const string& table_name, const Array<string>& columns, const Array<string>& indexes);

	void insert(const string& table_name, const Array<string>& values);

	void erase(const string& table_name, const Condition& condition);

	void select(const Array<string>& columns, const string& table_name_from, const string& table_name_join, const Condition& condition_join, const Condition& condition_where);

	Table& operator[](const string& table_name);
};







Table::Table()
{

}

Table::Table(const Array<string>& columns)
{
	this->columns = columns;

	int columns_size = this->columns.size();

	for (int i = 0; i < columns_size; i++)
	{
		this->columns_tree.emplace(this->columns[i], i);
	}
}

Table::Table(const Array<string>& columns, const Array<string>& indexes)
{
	this->columns = columns;

	int columns_size = this->columns.size();

	for (int i = 0; i < columns_size; i++)
	{
		this->columns_tree.emplace(this->columns[i], i);
	}

	int indexes_size = indexes.size();

	for (int i = 0; i < indexes_size; i++)
	{
		const string& column_name = indexes[i];

		if (this->columns_tree.find(column_name) == this->columns_tree.end())
		{
			throw exception(("unknown column " + column_name).c_str());
		}

		this->indexes.emplace(indexes[i], map<string, int>());
	}
}

Table::Table(const Array<string>& columns, const map<string, map<string, int>>& indexes)
{
	this->columns = columns;

	int columns_size = this->columns.size();

	for (int i = 0; i < columns_size; i++)
	{
		this->columns_tree.emplace(this->columns[i], i);
	}

	for (auto index = indexes.begin(); index != indexes.end(); ++index)
	{
		this->indexes.emplace(index->first, map<string, int>());
	}
}

Table::Table(const Array<string>& columns, const deque<Array<string>>& values)
{
	this->columns = columns;

	int columns_size = this->columns.size();

	for (int i = 0; i < columns_size; i++)
	{
		this->columns_tree.emplace(this->columns[i], i);
	}

	this->values = values;
}

Table::Table(const Array<string>& columns, const map<string, map<string, int>>& indexes, const deque<Array<string>>& values)
{
	this->columns = columns;

	int columns_size = this->columns.size();

	for (int i = 0; i < columns_size; i++)
	{
		this->columns_tree.emplace(this->columns[i], i);
	}

	this->indexes = indexes;

	this->values = values;
}

Table::Table(const Table& table)
{
	this->columns = table.columns;

	int columns_size = this->columns.size();

	for (int i = 0; i < columns_size; i++)
	{
		this->columns_tree.emplace(this->columns[i], i);
	}

	this->indexes = table.indexes;

	this->values = table.values;
}

bool Table::insert(const Array<string>& values)
{
	if (this->columns.size() != values.size())
	{
		throw exception("wrong number of parameters");
	}

	for (auto index = this->indexes.begin(); index != this->indexes.end(); ++index)
	{
		const string& column_name = index->first;

		int column_index = this->columns_tree.find(column_name)->second;

		const string& value = values[column_index];

		if (index->second.find(value) != index->second.end())
		{
			throw exception((column_name + " already has value " + value).c_str());
		}
	}

	this->values.push_back(values);

	int row_index = this->values.size() - 1;

	for (auto index = this->indexes.begin(); index != this->indexes.end(); ++index)
	{
		const string& column_name = index->first;

		int column_index = this->columns_tree.find(column_name)->second;

		const string& value = values[column_index];

		index->second.emplace(value, row_index);
	}

	return true;
}

void Table::erase(const int row_index)
{
	if (row_index >= this->values.size() || row_index < 0)
	{
		throw exception(("unknown row index " + to_string(row_index)).c_str());
	}

	for (auto index = this->indexes.begin(); index != this->indexes.end(); ++index)
	{
		const string& column_name = index->first;

		int column_index = this->columns_tree.find(column_name)->second;

		const string& value = this->values[row_index][column_index];

		index->second.erase(value);
	}

	this->values[row_index].clear();
}

int Table::erase(const Condition& condition)
{
	Condition::Type condition_type = condition.get_type();

	if (condition_type == Condition::Type::VALUE_VALUE)
	{
		if (!condition.compare())
		{
			return 0;
		}

		for (auto index = this->indexes.begin(); index != this->indexes.end(); ++index)
		{
			index->second.clear();
		}

		int values_size = this->values.size();

		this->values.clear();

		return values_size;
	}

	if (condition_type == Condition::Type::NAME_VALUE)
	{
		const string& column_name = condition.get_left();

		auto column_index = this->columns_tree.find(column_name);

		if (column_index == this->columns_tree.end())
		{
			throw exception(("unknown column " + column_name).c_str());
		}

		auto index = this->indexes.find(column_name);

		if (index == this->indexes.end())
		{
			int counter = 0;

			int values_size = this->values.size();

			for (int i = 0; i < values_size; i++)
			{
				if (this->values[i].size() > 0)
				{
					const string& value = this->values[i][column_index->second];

					if (condition.compare(value))
					{
						this->erase(i);
						counter++;
					}
				}
			}

			return counter;
		}

		Condition::Operation c_operation = condition.get_operation();
		string condition_value = condition.get_right();

		condition_value = condition_value.substr(1, condition_value.length() - 2);

		if (c_operation == Condition::Operation::EQUAL)
		{
			auto row_index = index->second.find(condition_value);

			if (row_index == index->second.end())
			{
				return 0;
			}

			this->erase(row_index->second);

			return 1;
		}

		if (c_operation == Condition::Operation::NOT_EQUAL)
		{
			auto row_index = index->second.find(condition_value);

			if (row_index == index->second.end())
			{
				for (auto index = this->indexes.begin(); index != this->indexes.end(); ++index)
				{
					index->second.clear();
				}

				int values_size = this->values.size();

				this->values.clear();

				return values_size;
			}

			Array<string> row = this->values[row_index->second];

			for (auto index = this->indexes.begin(); index != this->indexes.end(); ++index)
			{
				index->second.clear();
			}

			int values_size = this->values.size();

			this->values.clear();

			this->insert(row);

			return values_size - 1;
		}

		//<, >, <=, >=

		bool is_equal = c_operation == Condition::Operation::LESS_EQUAL || c_operation == Condition::Operation::GREATER_EQUAL;

		deque<int> correct_rows;

		if (c_operation == Condition::Operation::LESS || c_operation == Condition::Operation::LESS_EQUAL)
		{
			for (auto node = index->second.begin(); node != index->second.end(); ++node)
			{
				if (is_equal && node->first == condition_value)
				{
					correct_rows.push_back(node->second);
				}

				if (node->first < condition_value)
				{
					correct_rows.push_back(node->second);
				}

				else
				{
					break;
				}
			}
		}

		if (c_operation == Condition::Operation::GREATER || c_operation == Condition::Operation::GREATER_EQUAL)
		{
			for (auto node = index->second.rbegin(); node != index->second.rend(); ++node)
			{
				if (is_equal && node->first == condition_value)
				{
					correct_rows.push_back(node->second);
				}

				if (node->first > condition_value)
				{
					correct_rows.push_back(node->second);
				}

				else
				{
					break;
				}
			}
		}

		int rows_size = correct_rows.size();
		
		for (int i = 0; i < rows_size; i++)
		{
			this->erase(correct_rows[i]);
		}

		return rows_size;
	}

	if (condition_type == Condition::Type::NAME_NAME)
	{
		const string& column_name1 = condition.get_left();
		const string& column_name2 = condition.get_right();

		auto column_index1 = this->columns_tree.find(column_name1);
		auto column_index2 = this->columns_tree.find(column_name2);

		if (column_index1 == this->columns_tree.end())
		{
			throw exception(("unknown column " + column_name1).c_str());
		}

		if (column_index2 == this->columns_tree.end())
		{
			throw exception(("unknown column " + column_name2).c_str());
		}

		int counter = 0;

		int values_size = this->values.size();

		for (int i = 0; i < values_size; i++)
		{
			if (this->values[i].size() > 0)
			{
				Array<string> row = this->values[i];

				const string& value1 = row[column_index1->second];
				const string& value2 = row[column_index2->second];

				if (condition.compare(value1, value2))
				{
					this->erase(i);
					counter++;
				}
			}
		}

		return counter;
	}
}

Table Table::join(const Table& table, const Condition& condition) const
{
	if (condition.get_type() == Condition::Type::VALUE_VALUE)
	{
		Table result(this->columns + table.columns);

		int values_size1 = this->values.size(), values_size2 = table.values.size();

		for (int i = 0; i < values_size1; i++)
		{
			for (int j = 0; j < values_size2; j++)
			{
				if (this->values[i].size() > 0 && table.values[j].size() > 0)
				{
					result.values.push_back(this->values[i] + table.values[j]);
				}
			}
		}

		return result;
	}

	const string& column_name1 = condition.get_left();
	const string& column_name2 = condition.get_right();

	auto column_index1 = this->columns_tree.find(column_name1);
	auto column_index2 = table.columns_tree.find(column_name2);

	if (column_index1 == this->columns_tree.end())
	{
		throw exception(("unknown column " + column_name1).c_str());
	}

	if (column_index2 == table.columns_tree.end())
	{
		throw exception(("unknown column " + column_name2).c_str());
	}

	Table result(this->columns + table.columns);

	int values_size1 = this->values.size(), values_size2 = table.values.size();

	auto index1 = this->indexes.find(column_name1);
	auto index2 = table.indexes.find(column_name2);

	if (index2 != table.indexes.end())
	{
		for (int i = 0; i < values_size1; i++)
		{
			if (this->values[i].size() > 0)
			{
				const string& value = this->values[i][column_index1->second];

				auto row_index = index2->second.find(value);

				if (row_index != index2->second.end())
				{
					result.values.push_back(this->values[i] + table.values[row_index->second]);
				}
			}
		}

		return result;
	}

	if (index1 != this->indexes.end())
	{
		for (int i = 0; i < values_size2; i++)
		{
			if (table.values[i].size() > 0)
			{
				const string& value = table.values[i][column_index2->second];

				auto row_index = index1->second.find(value);

				if (row_index != index1->second.end())
				{
					result.values.push_back(this->values[row_index->second] + table.values[i]);
				}
			}
		}

		return result;
	}

	for (int i = 0; i < values_size1; i++)
	{
		for (int j = 0; j < values_size2; j++)
		{
			if (this->values[i].size() > 0 && table.values[j].size() > 0)
			{
				const string& value1 = this->values[i][column_index1->second];
				const string& value2 = table.values[j][column_index2->second];

				if (condition.compare(value1, value2))
				{
					result.values.push_back(this->values[i] + table.values[j]);
				}
			}
		}
	}

	return result;
}

Table Table::where(const Condition& condition) const
{
	Condition::Type condition_type = condition.get_type();

	if (condition_type == Condition::Type::VALUE_VALUE)
	{
		if (!condition.compare())
		{
			return Table(this->columns);
		}

		return Table(this->columns, this->values);
	}

	if (condition_type == Condition::Type::NAME_VALUE)
	{
		const string& column_name = condition.get_left();

		auto column_index = this->columns_tree.find(column_name);

		if (column_index == this->columns_tree.end())
		{
			throw exception(("unknown column " + column_name).c_str());
		}

		auto index = this->indexes.find(column_name);

		if (index == this->indexes.end())
		{
			Table result(this->columns);

			int values_size = this->values.size();

			for (int i = 0; i < values_size; i++)
			{
				if (this->values[i].size() > 0)
				{
					Array<string> row = values[i];

					if (condition.compare(row[column_index->second]))
					{
						result.values.push_back(row);
					}
				}
			}

			return result;
		}

		Condition::Operation c_operation = condition.get_operation();
		string condition_value = condition.get_right();

		condition_value = condition_value.substr(1, condition_value.length() - 2);

		if (c_operation == Condition::Operation::EQUAL)
		{
			auto row_index = index->second.find(condition_value);

			if (row_index == index->second.end())
			{
				return Table(this->columns);
			}

			Table result(this->columns);

			result.values.push_back(this->values[row_index->second]);

			return result;
		}

		if (c_operation == Condition::Operation::NOT_EQUAL)
		{
			auto row_index = index->second.find(condition_value);

			if (row_index == index->second.end())
			{
				return Table(this->columns, this->values);
			}

			Table result(this->columns, this->values);

			result.values.erase(result.values.begin() + row_index->second);

			return result;
		}

		//<, >, <=, >=

		bool is_equal = c_operation == Condition::Operation::LESS_EQUAL || c_operation == Condition::Operation::GREATER_EQUAL;

		Table result(this->columns, this->values);

		condition_value = '`' + condition_value + '`';

		result.erase(Condition(column_name, condition_value, reverse_operation(c_operation)));

		return result;
	}

	if (condition_type == Condition::Type::NAME_NAME)
	{
		const string& column_name1 = condition.get_left();
		const string& column_name2 = condition.get_right();

		auto column_index1 = this->columns_tree.find(column_name1);
		auto column_index2 = this->columns_tree.find(column_name2);

		if (column_index1 == this->columns_tree.end())
		{
			throw exception(("unknown column " + column_name1).c_str());
		}

		if (column_index2 == this->columns_tree.end())
		{
			throw exception(("unknown column " + column_name2).c_str());
		}

		Table result(this->columns);

		int values_size = this->values.size();

		for (int i = 0; i < values_size; i++)
		{
			if (this->values[i].size() > 0)
			{
				Array<string> row = values[i];

				if (condition.compare(row[column_index1->second], row[column_index2->second]))
				{
					result.values.push_back(row);
				}
			}
		}

		return result;
	}
}

Table Table::select(const Array<string>& columns) const
{
	int columns_size = columns.size();

	if (columns_size == 0)
	{
		return Table(this->columns, this->values);
	}

	Array<int> columns_indexes(columns_size);

	for (int i = 0; i < columns_size; i++)
	{
		const string& column_name = columns[i];

		auto column_index = this->columns_tree.find(column_name);

		if (column_index == this->columns_tree.end())
		{
			throw exception(("unknown column " + column_name).c_str());
		}

		columns_indexes[i] = column_index->second;
	}

	deque<Array<string>> new_values;

	int values_size = this->values.size();

	for (int i = 0; i < values_size; i++)
	{
		if (this->values[i].size() > 0)
		{
			new_values.push_back(this->values[i] * columns_indexes);
		}
	}

	return Table(columns, new_values);
}

void print_border(const Array<int>& max_columns)
{
	cout << '+';

	int size = max_columns.size();

	for (int i = 0; i < size; i++)
	{
		for (int j = 0; j < max_columns[i] + 2; j++)
		{
			cout << '-';
		}

		cout << '+';
	}

	cout << endl;
}

void print_row(const Array<int>& max_columns, const Array<string>& values)
{
	cout << '|';

	int size = max_columns.size();

	for (int i = 0; i < size; i++)
	{
		cout << ' ';

		const string& value = values[i];

		cout << value;

		for (int j = 0; j < max_columns[i] - value.length() + 1; j++)
		{
			cout << ' ';
		}

		cout << '|';
	}

	cout << endl;
}

void Table::print() const
{
	int columns_size = this->columns.size(), values_size = this->values.size();

	Array<int> max_columns(columns_size);

	for (int i = 0; i < columns_size; i++)
	{
		max_columns[i] = int(this->columns[i].length());
	}

	for (int i = 0; i < values_size; i++)
	{
		if (this->values[i].size() > 0)
		{
			for (int j = 0; j < columns_size; j++)
			{
				int value_length = this->values[i][j].length();

				if (max_columns[j] < value_length)
				{
					max_columns[j] = value_length;
				}
			}
		}
	}

	print_border(max_columns);

	print_row(max_columns, this->columns);

	print_border(max_columns);

	for (int i = 0; i < values_size; i++)
	{
		if (this->values[i].size() > 0)
		{
			print_row(max_columns, this->values[i]);
		}
	}

	print_border(max_columns);
}





void Database::create(const string& table_name, const Array<string>& columns, const Array<string>& indexes)
{
	if (this->tables.find(table_name) != this->tables.end())
	{
		throw exception(("table " + table_name + " already exists").c_str());
	}

	int columns_size = columns.size();

	for (int i = 0; i < columns_size; i++)
	{
		for (int j = 0; j < columns_size; j++)
		{
			if (i != j && columns[i] == columns[j])
			{
				throw exception("few columns have the same name");
			}
		}
	}

	this->tables.emplace(table_name, Table(columns, indexes));

	cout << "Table " << table_name << " has been created successfully" << endl;
}

void Database::insert(const string& table_name, const Array<string>& values)
{
	bool inserted_rows = this->operator[](table_name).insert(values);

	cout << inserted_rows << " rows was added to table " << table_name << endl;
}

void Database::erase(const string& table_name, const Condition& condition)
{
	int deleted_rows = this->operator[](table_name).erase(condition);

	cout << deleted_rows << " rows was removed from table " << table_name << endl;
}

void Database::select(const Array<string>& columns, const string& table_name_from, const string& table_name_join, const Condition& condition_join, const Condition& condition_where)
{
	if (table_name_join != "")
	{
		this->operator[](table_name_from).join(this->operator[](table_name_join), condition_join).where(condition_where).select(columns).print();
	}

	else
	{
		this->operator[](table_name_from).where(condition_where).select(columns).print();
	}
}

Table& Database::operator[](const string& table_name)
{
	auto table = this->tables.find(table_name);
	
	if (table == this->tables.end())
	{
		throw exception(("unknown table " + table_name).c_str());
	}

	else
	{
		return table->second;
	}
}