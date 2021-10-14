#pragma once
#include <deque>
#include <map>
#include "Array.h"
#include "Condition.h"

using namespace std;

class Table
{
private:
	Array<string> columns;
	map<string, int> columns_tree;

	Array<string> indexes;
	map<string, int> indexes_tree;
	Array<map<string, int>> indexes_array;

	deque<Array<string>> values;

public:
	Table();

	Table(const Array<string>& columns);

	Table(const Array<string>& columns, const Array<string>& indexes);

	Table(const Array<string>& columns, const Array<string>& indexes, const deque<Array<string>>& values);

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
	deque<Table> tables;
	map<string, int> tables_tree;

public:
	void create(string table_name, const Array<string>& columns, const Array<string>& indexes);

	void insert(string table_name, const Array<string>& values);

	void erase(string table_name, const Condition& condition);

	void select(const Array<string>& columns, string table_name_from, string table_name_join, const Condition& condition_join, const Condition& condition_where);

	Table& operator[](string table_name);
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

	this->indexes = indexes;

	int indexes_size = this->indexes.size();

	for (int i = 0; i < indexes_size; i++)
	{
		this->indexes_tree.emplace(this->indexes[i], i);
	}

	this->indexes_array = Array<map<string, int>>(indexes_size);
}

Table::Table(const Array<string>& columns, const Array<string>& indexes, const deque<Array<string>>& values)
{
	this->columns = columns;

	int columns_size = this->columns.size();

	for (int i = 0; i < columns_size; i++)
	{
		this->columns_tree.emplace(this->columns[i], i);
	}

	this->indexes = indexes;

	int indexes_size = this->indexes.size();

	this->indexes_array = Array<map<string, int>>(indexes_size);

	for (int i = 0; i < indexes_size; i++)
	{
		this->indexes_tree.emplace(this->indexes[i], i);
	}

	int values_size = values.size();

	for (int i = 0; i < values_size; i++)
	{
		this->insert(values[i]);
	}
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

	int indexes_size = this->indexes.size();

	this->indexes_array = Array<map<string, int>>(indexes_size);

	for (int i = 0; i < indexes_size; i++)
	{
		this->indexes_tree.emplace(this->indexes[i], i);
	}

	int values_size = table.values.size();

	for (int i = 0; i < values_size; i++)
	{
		this->insert(table.values[i]);
	}
}

bool Table::insert(const Array<string>& values)
{
	if (this->columns.size() != values.size())
	{
		throw exception("wrong number of parameters");
	}

	int indexes_size = this->indexes.size();

	for (int i = 0; i < indexes_size; i++)
	{
		string column_name = this->indexes[i];

		int column_index = this->columns_tree.find(column_name)->second;

		string value = values[column_index];

		if (this->indexes_array[i].find(value) != this->indexes_array[i].end())
		{
			string ex = column_name + " already has value " + value;

			throw exception(ex.c_str());
		}
	}

	this->values.push_back(values);

	int row_index = this->values.size() - 1;

	for (int i = 0; i < indexes_size; i++)
	{
		string column_name = this->indexes[i];

		int column_index = this->columns_tree.find(column_name)->second;

		this->indexes_array[i].emplace(values[column_index], row_index);
	}

	return true;
}

void Table::erase(const int row_index)
{
	if (row_index >= this->values.size() || row_index < 0)
	{
		string ex = "unknown row index " + to_string(row_index);

		throw exception(ex.c_str());
	}

	int indexes_size = this->indexes.size();

	for (int i = 0; i < indexes_size; i++)
	{
		string column_name = this->indexes[i];

		int column_index = this->columns_tree.find(column_name)->second;

		string value = this->values[row_index][column_index];

		this->indexes_array[i].erase(value);

		for (auto node = this->indexes_array[i].begin(); node != this->indexes_array[i].end(); ++node)
		{
			if (node->second > row_index)
			{
				node->second--;
			}
		}
	}

	this->values.erase(this->values.begin() + row_index);
}

int Table::erase(const Condition& condition)
{
	int condition_type = condition.get_type();

	if (condition_type == 0)//VALUE ? VALUE
	{
		if (!condition.get_value())
		{
			return 0;
		}

		int values_size = this->values.size();

		this->values = deque<Array<string>>();

		this->indexes_array = Array<map<string, int>>(this->indexes.size());

		return values_size;
	}

	if (condition_type == 1)//NAME ? VALUE
	{
		string column_name = condition.get_left();

		auto column_index = this->columns_tree.find(column_name);

		if (column_index == this->columns_tree.end())
		{
			string ex = "unknown column " + column_name;

			throw exception(ex.c_str());
		}

		auto index_index = this->indexes_tree.find(column_name);

		if (index_index == this->indexes_tree.end())
		{
			int counter = 0;

			int values_size = this->values.size();

			for (int i = 0; i < values_size; i++)
			{
				string value = this->values[i - counter][column_index->second];

				if (condition.get_value(value))
				{
					this->erase(i - counter);
					counter++;
				}
			}

			return counter;
		}

		string condition_operation = condition.get_operation();
		string condition_value = condition.get_right();

		condition_value = condition_value.substr(1, condition_value.length() - 2);

		if (condition_operation == "=")
		{
			auto row_index = this->indexes_array[index_index->second].find(condition_value);

			if (row_index == this->indexes_array[index_index->second].end())
			{
				return 0;
			}

			this->erase(row_index->second);

			return 1;
		}

		if (condition_operation == "!=")
		{
			int values_size = this->values.size();

			auto row_index = this->indexes_array[index_index->second].find(condition_value);

			if (row_index == this->indexes_array[index_index->second].end())
			{
				int values_size = this->values.size();

				this->values = deque<Array<string>>();

				this->indexes_array = Array<map<string, int>>(this->indexes.size());

				return values_size;
			}

			Array<string> row = this->values[row_index->second];

			this->values = deque<Array<string>>();

			this->indexes_array = Array<map<string, int>>(this->indexes.size());

			this->insert(row);

			return values_size - 1;
		}

		//<, >, <=, >=

		bool is_equal = condition_operation.length() == 2;

		deque<int> correct_rows;

		if (condition_operation[0] == '<')
		{
			for (auto node = this->indexes_array[index_index->second].begin(); node != this->indexes_array[column_index->second].end(); ++node)
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

		if (condition_operation[0] == '>')
		{
			for (auto node = this->indexes_array[index_index->second].rbegin(); node != this->indexes_array[column_index->second].rend(); ++node)
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

		Array<int> rows_array(rows_size);

		for (int i = 0; i < rows_size; i++)
		{
			rows_array[i] = correct_rows[i];
		}

		rows_array.sort();

		int counter = 0;

		for (int i = 0; i < rows_size; i++)
		{
			this->erase(rows_array[i] - counter);
			counter++;
		}

		return counter;
	}

	if (condition_type == 2)//NAME ? NAME
	{
		string column_name1 = condition.get_left();
		string column_name2 = condition.get_right();

		auto column_index1 = this->columns_tree.find(column_name1);
		auto column_index2 = this->columns_tree.find(column_name2);

		if (column_index1 == this->columns_tree.end())
		{
			string ex = "unknown column " + column_name1;

			throw exception(ex.c_str());
		}

		if (column_index2 == this->columns_tree.end())
		{
			string ex = "unknown column " + column_name2;

			throw exception(ex.c_str());
		}

		int counter = 0;

		int values_size = this->values.size();

		for (int i = 0; i < values_size; i++)
		{
			Array<string> row = this->values[i - counter];

			string value1 = row[column_index1->second];
			string value2 = row[column_index2->second];

			if (condition.get_value(value1, value2))
			{
				this->erase(i - counter);
				counter++;
			}
		}

		return counter;
	}
}

Table Table::join(const Table& table, const Condition& condition) const
{
	if (condition.get_type() == 0)//VALUE ? VALUE
	{
		Table result;

		result.columns = this->columns + table.columns;

		int values_size1 = this->values.size(), values_size2 = table.values.size();

		for (int i = 0; i < values_size1; i++)
		{
			for (int j = 0; j < values_size2; j++)
			{
				result.values.push_back(this->values[i] + table.values[j]);
			}
		}

		return result;
	}

	string column_name1 = condition.get_left();
	string column_name2 = condition.get_right();

	auto column_index1 = this->columns_tree.find(column_name1);
	auto column_index2 = table.columns_tree.find(column_name2);

	if (column_index1 == this->columns_tree.end())
	{
		string ex = "unknown column " + column_name1;

		throw exception(ex.c_str());
	}

	if (column_index2 == table.columns_tree.end())
	{
		string ex = "unknown column " + column_name2;

		throw exception(ex.c_str());
	}

	Table result;

	result.columns = this->columns + table.columns;

	int values_size1 = this->values.size(), values_size2 = table.values.size();

	auto index_index1 = this->indexes_tree.find(column_name1);
	auto index_index2 = table.indexes_tree.find(column_name2);

	if (index_index2 != table.indexes_tree.end())
	{
		for (int i = 0; i < values_size1; i++)
		{
			string value = this->values[i][column_index1->second];

			auto row_index = table.indexes_array[index_index2->second].find(value);

			if (row_index != table.indexes_array[index_index2->second].end())
			{
				result.values.push_back(this->values[i] + table.values[row_index->second]);
			}
		}

		return result;
	}

	if (index_index1 != this->indexes_tree.end())
	{
		for (int i = 0; i < values_size2; i++)
		{
			string value = table.values[i][column_index2->second];

			auto row_index = this->indexes_array[index_index1->second].find(value);

			if (row_index != this->indexes_array[index_index1->second].end())
			{
				result.values.push_back(this->values[row_index->second] + table.values[i]);
			}
		}

		return result;
	}

	for (int i = 0; i < values_size1; i++)
	{
		for (int j = 0; j < values_size2; j++)
		{
			string value1 = this->values[i][column_index1->second];
			string value2 = this->values[i][column_index2->second];

			if (condition.get_value(value1, value2))
			{
				result.values.push_back(this->values[i] + table.values[j]);
			}
		}
	}

	return result;
}

Table Table::where(const Condition& condition) const
{
	int condition_type = condition.get_type();

	if (condition_type == 0)//VALUE ? VALUE
	{
		if (!condition.get_value())
		{
			return Table(this->columns, this->indexes);
		}

		return Table(this->columns, this->indexes, this->values);
	}

	if (condition_type == 1)//NAME ? VALUE
	{
		string column_name = condition.get_left();

		auto column_index = this->columns_tree.find(column_name);

		if (column_index == this->columns_tree.end())
		{
			string ex = "unknown column " + column_name;

			throw exception(ex.c_str());
		}

		auto index_index = this->indexes_tree.find(column_name);

		if (index_index == this->indexes_tree.end())
		{
			Table result(this->columns, this->indexes);

			int values_size = this->values.size();

			for (int i = 0; i < values_size; i++)
			{
				Array<string> row = values[i];

				if (condition.get_value(row[column_index->second]))
				{
					result.insert(row);
				}
			}

			return result;
		}

		string condition_operation = condition.get_operation();
		string condition_value = condition.get_right();

		condition_value = condition_value.substr(1, condition_value.length() - 2);

		if (condition_operation == "=")
		{
			auto row_index = this->indexes_array[index_index->second].find(condition_value);

			if (row_index == this->indexes_array[column_index->second].end())
			{
				return Table(this->columns, this->indexes);
			}

			Table result(this->columns, this->indexes);

			result.insert(this->values[row_index->second]);

			return result;
		}

		if (condition_operation == "!=")
		{
			auto row_index = this->indexes_array[index_index->second].find(condition_value);

			if (row_index == this->indexes_array[column_index->second].end())
			{
				return Table(this->columns, this->indexes, this->values);
			}

			Table result(this->columns, this->indexes, this->values);

			result.erase(row_index->second);

			return result;
		}

		//<, >, <=, >=

		bool is_equal = condition_operation.length() == 2;

		deque<int> correct_rows;

		if (condition_operation[0] == '<')
		{
			for (auto node = this->indexes_array[index_index->second].begin(); node != this->indexes_array[column_index->second].end(); ++node)
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

		if (condition_operation[0] == '>')
		{
			for (auto node = this->indexes_array[index_index->second].rbegin(); node != this->indexes_array[column_index->second].rend(); ++node)
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

		Array<int> rows_array(rows_size);

		for (int i = 0; i < rows_size; i++)
		{
			rows_array[i] = correct_rows[i];
		}

		rows_array.sort();

		Table result(this->columns, this->indexes);

		for (int i = 0; i < rows_size; i++)
		{
			result.insert(this->values[rows_array[i]]);
		}

		return result;
	}

	if (condition_type == 2)//NAME ? NAME
	{
		string column_name1 = condition.get_left();
		string column_name2 = condition.get_right();

		auto column_index1 = this->columns_tree.find(column_name1);
		auto column_index2 = this->columns_tree.find(column_name2);

		if (column_index1 == this->columns_tree.end())
		{
			string ex = "unknown column " + column_name1;

			throw exception(ex.c_str());
		}

		if (column_index2 == this->columns_tree.end())
		{
			string ex = "unknown column " + column_name2;

			throw exception(ex.c_str());
		}

		Table result(this->columns, this->indexes);

		int values_size = this->values.size();

		for (int i = 0; i < values_size; i++)
		{
			Array<string> row = values[i];

			if (condition.get_value(row[column_index1->second], row[column_index2->second]))
			{
				result.insert(row);
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
		return Table(this->columns, this->indexes, this->values);
	}

	deque<int> columns_list;

	deque<int> indexes_list;

	for (int i = 0; i < columns_size; i++)
	{
		string column_name = columns[i];

		auto column_index = this->columns_tree.find(column_name);

		if (column_index == this->columns_tree.end())
		{
			string ex = "unknown column " + column_name;

			throw exception(ex.c_str());
		}

		columns_list.push_back(column_index->second);

		auto index_index = this->indexes_tree.find(column_name);

		if (index_index != this->indexes_tree.end())
		{
			indexes_list.push_back(index_index->second);
		}
	}

	int columns_list_size = columns_list.size();

	Array<int> columns_indexes(columns_list_size);

	for (int i = 0; i < columns_list_size; i++)
	{
		columns_indexes[i] = columns_list[i];
	}

	int indexes_list_size = indexes_list.size();

	Array<int> indexes_indexes(indexes_list_size);

	for (int i = 0; i < indexes_list_size; i++)
	{
		indexes_indexes[i] = indexes_list[i];
	}

	Array<string> new_indexes = this->indexes * indexes_indexes;

	deque<Array<string>> new_values;

	int values_size = this->values.size();

	for (int i = 0; i < values_size; i++)
	{
		new_values.push_back(this->values[i] * columns_indexes);
	}

	return Table(columns, new_indexes, new_values);
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

		string value = values[i];

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
		for (int j = 0; j < columns_size; j++)
		{
			int value_length = this->values[i][j].length();

			if (max_columns[j] < value_length)
			{
				max_columns[j] = value_length;
			}
		}
	}

	print_border(max_columns);

	print_row(max_columns, this->columns);

	print_border(max_columns);

	for (int i = 0; i < values_size; i++)
	{
		print_row(max_columns, this->values[i]);
	}

	print_border(max_columns);
}





void Database::create(string table_name, const Array<string>& columns, const Array<string>& indexes)
{
	if (this->tables_tree.find(table_name) != this->tables_tree.end())
	{
		string ex = "table " + table_name + " already exists";

		throw exception(ex.c_str());
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

	Table new_table(columns, indexes);

	this->tables.push_back(new_table);

	int table_index = this->tables.size() - 1;

	this->tables_tree.emplace(table_name, table_index);

	cout << "Table " << table_name << " has been created successfully" << endl;
}

void Database::insert(string table_name, const Array<string>& values)
{
	bool inserted_rows = this->operator[](table_name).insert(values);

	cout << inserted_rows << " rows was added to table " << table_name << endl;
}

void Database::erase(string table_name, const Condition& condition)
{
	int deleted_rows = this->operator[](table_name).erase(condition);

	cout << deleted_rows << " rows was removed from table " << table_name << endl;
}

void Database::select(const Array<string>& columns, string table_name_from, string table_name_join, const Condition& condition_join, const Condition& condition_where)
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

Table& Database::operator[](string table_name)
{
	auto table_index = this->tables_tree.find(table_name);
	
	if (table_index == this->tables_tree.end())
	{
		string ex = "unknown table " + table_name;

		throw exception(ex.c_str());
	}

	else
	{
		return this->tables[table_index->second];
	}
}