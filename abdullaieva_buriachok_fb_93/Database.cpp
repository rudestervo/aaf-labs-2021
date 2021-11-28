#include "Database.h"
#include <iostream>

Table::Table()
{
	this->table_rows = 0;
}

Table::Table(const Array<std::string>& columns) : Table()
{
	this->columns = columns;

	int columns_size = this->columns.size();

	for (int i = 0; i < columns_size; i++)
	{
		this->columns_map.emplace(this->columns[i], i);
	}
}

Table::Table(const Array<std::string>& columns, const Array<std::string>& indexes) : Table(columns)
{
	int indexes_size = indexes.size();

	for (int i = 0; i < indexes_size; i++)
	{
		const std::string& column_name = indexes[i];

		if (this->columns_map.find(column_name) == this->columns_map.end())
		{
			throw std::exception(("unknown column " + column_name).c_str());
		}

		this->indexes.emplace(column_name, std::map<std::string, std::set<int>>());
	}
}

Table::Table(const Array<std::string>& columns, const std::map<std::string, std::map<std::string, int>>& indexes) : Table(columns)
{
	for (auto index = indexes.begin(); index != indexes.end(); ++index)
	{
		const std::string& column_name = index->first;

		if (this->columns_map.find(column_name) == this->columns_map.end())
		{
			throw std::exception(("unknown column " + column_name).c_str());
		}

		this->indexes.emplace(column_name, std::map<std::string, std::set<int>>());
	}
}

Table::Table(const Array<std::string>& columns, const std::map<std::string, std::map<std::string, int>>& indexes, const std::deque<Array<std::string>>& values) : Table(columns, indexes)
{
	for (auto value_row = values.begin(); value_row != values.end(); ++value_row)
	{
		this->insert(*value_row);
	}
}

Table::Table(const Table& table)
{
	this->columns = table.columns;
	this->columns_map = table.columns_map;
	this->indexes = table.indexes;
	this->values = table.values;
	this->table_rows = table.table_rows;
}

void Table::insert(const Array<std::string>& values)
{
	if (this->columns.size() != values.size())
	{
		throw std::exception("wrong number of parameters");
	}

	this->values.push_back(values);
	this->table_rows++;

	int row_index = this->values.size() - 1;

	for (auto index = this->indexes.begin(); index != this->indexes.end(); ++index)
	{
		const std::string& column_name = index->first;

		int column_index = this->columns_map.find(column_name)->second;

		const std::string& value = values[column_index];

		auto index_node = index->second.find(value);

		if (index_node != index->second.end())
		{
			index_node->second.emplace(row_index);
		}

		else
		{
			std::set<int> index_set;
			index_set.emplace(row_index);

			index->second.emplace(value, index_set);
		}
	}
}

void Table::erase(const int row_index)
{
	if (row_index >= this->values.size() || row_index < 0)
	{
		throw std::exception(("unknown row index " + std::to_string(row_index)).c_str());
	}

	for (auto index = this->indexes.begin(); index != this->indexes.end(); ++index)
	{
		const std::string& column_name = index->first;

		int column_index = this->columns_map.find(column_name)->second;

		const std::string& value = this->values[row_index][column_index];

		std::set<int>& index_set = index->second.find(value)->second;

		if (index_set.size() == 1)
		{
			index->second.erase(value);
		}

		else
		{
			index_set.erase(row_index);
		}
	}

	this->values[row_index].clear();
	this->table_rows--;
}

int Table::erase(const Condition& condition)
{
	if (condition.type == Condition::Type::VALUE_VALUE)
	{
		if (!condition.compare())
		{
			return 0;
		}

		for (auto index = this->indexes.begin(); index != this->indexes.end(); ++index)
		{
			index->second.clear();
		}

		int deleted_rows = this->table_rows;

		this->values.clear();
		this->table_rows = 0;

		return deleted_rows;
	}

	if (condition.type == Condition::Type::NAME_VALUE)
	{
		const std::string& column_name = condition.left;

		auto column_index = this->columns_map.find(column_name);

		if (column_index == this->columns_map.end())
		{
			throw std::exception(("unknown column " + column_name).c_str());
		}

		auto index = this->indexes.find(column_name);

		if (index == this->indexes.end())
		{
			int deleted_rows = this->table_rows;

			int counter = 0;
			
			for (auto value_row = this->values.begin(); value_row != this->values.end(); ++value_row)
			{
				if ((*value_row).size() > 0)
				{
					const std::string& value = (*value_row)[column_index->second];

					if (condition.compare(value))
					{
						this->erase(counter);
					}
				}

				counter++;
			}

			return deleted_rows - this->table_rows;
		}

		const std::string& condition_value = condition.right;

		if (condition.operation == Condition::Operation::EQUAL)
		{
			auto index_node = index->second.find(condition_value);

			if (index_node == index->second.end())
			{
				return 0;
			}

			std::set<int> index_set = index_node->second;

			int set_size = index_set.size();

			for (auto row_index = index_set.begin(); row_index != index_set.end(); ++row_index)
			{
				this->erase(*row_index);
			}

			return set_size;
		}

		if (condition.operation == Condition::Operation::NOT_EQUAL)
		{
			int deleted_rows = this->table_rows;

			*this = this->where(condition.reverse());

			return deleted_rows - this->table_rows;
		}

		//<, >, <=, >=

		bool is_equal = condition.operation == Condition::Operation::LESS_EQUAL || condition.operation == Condition::Operation::GREATER_EQUAL;

		std::set<int> rows_set;

		if (condition.operation == Condition::Operation::LESS || condition.operation == Condition::Operation::LESS_EQUAL)
		{
			for (auto index_node = index->second.begin(); index_node != index->second.end(); ++index_node)
			{
				if (is_equal && index_node->first == condition_value)
				{
					const std::set<int>& index_set = index_node->second;

					for (auto row_index = index_set.begin(); row_index != index_set.end(); ++row_index)
					{
						rows_set.emplace(*row_index);
					}
				}

				if (index_node->first < condition_value)
				{
					const std::set<int>& index_set = index_node->second;

					for (auto row_index = index_set.begin(); row_index != index_set.end(); ++row_index)
					{
						rows_set.emplace(*row_index);
					}
				}

				else
				{
					break;
				}
			}
		}

		if (condition.operation == Condition::Operation::GREATER || condition.operation == Condition::Operation::GREATER_EQUAL)
		{
			for (auto index_node = index->second.rbegin(); index_node != index->second.rend(); ++index_node)
			{
				if (is_equal && index_node->first == condition_value)
				{
					const std::set<int>& index_set = index_node->second;

					for (auto row_index = index_set.begin(); row_index != index_set.end(); ++row_index)
					{
						rows_set.emplace(*row_index);
					}
				}

				if (index_node->first > condition_value)
				{
					const std::set<int>& index_set = index_node->second;

					for (auto row_index = index_set.begin(); row_index != index_set.end(); ++row_index)
					{
						rows_set.emplace(*row_index);
					}
				}

				else
				{
					break;
				}
			}
		}

		int rows_size = rows_set.size();

		for (auto row = rows_set.begin(); row != rows_set.end(); ++row)
		{
			this->erase(*row);
		}

		return rows_size;
	}

	if (condition.type == Condition::Type::NAME_NAME)
	{
		const std::string& column_name1 = condition.left;
		const std::string& column_name2 = condition.right;

		auto column_index1 = this->columns_map.find(column_name1);
		auto column_index2 = this->columns_map.find(column_name2);

		if (column_index1 == this->columns_map.end())
		{
			throw std::exception(("unknown column " + column_name1).c_str());
		}

		if (column_index2 == this->columns_map.end())
		{
			throw std::exception(("unknown column " + column_name2).c_str());
		}

		int deleted_rows = this->table_rows;

		int counter = 0;
		
		for (auto value_row = this->values.begin(); value_row != this->values.end(); ++value_row)
		{
			if ((*value_row).size() > 0)
			{
				const Array<std::string>& row = *value_row;

				const std::string& value1 = row[column_index1->second];
				const std::string& value2 = row[column_index2->second];

				if (condition.compare(value1, value2))
				{
					this->erase(counter);
				}
			}

			counter++;
		}

		return deleted_rows - this->table_rows;
	}
}

Table Table::join(const Table& table, const Join& join) const
{
	if (join.type == Join::Type::JOIN)
	{
		Table result(this->columns + table.columns);

		for (auto value_row1 = this->values.begin(); value_row1 != this->values.end(); ++value_row1)
		{
			for (auto value_row2 = table.values.begin(); value_row2 != table.values.end(); ++value_row2)
			{
				if ((*value_row1).size() > 0 && (*value_row2).size() > 0)
				{
					result.values.push_back((*value_row1) + (*value_row2));
				}
			}
		}

		result.table_rows = this->table_rows * table.table_rows;

		return result;
	}

	const std::string& column_name1 = join.left;
	const std::string& column_name2 = join.right;

	auto column_index1 = this->columns_map.find(column_name1);
	auto column_index2 = table.columns_map.find(column_name2);

	if (column_index1 == this->columns_map.end())
	{
		throw std::exception(("unknown column " + column_name1).c_str());
	}

	if (column_index2 == table.columns_map.end())
	{
		throw std::exception(("unknown column " + column_name2).c_str());
	}

	Table result(this->columns + table.columns);

	auto index1 = this->indexes.find(column_name1);
	auto index2 = table.indexes.find(column_name2);

	if (index2 != table.indexes.end())
	{
		for (auto value_row1 = this->values.begin(); value_row1 != this->values.end(); ++value_row1)
		{
			if ((*value_row1).size() > 0)
			{
				const std::string& value = (*value_row1)[column_index1->second];

				auto index_node = index2->second.find(value);

				if (index_node != index2->second.end())
				{
					const std::set<int>& index_set = index_node->second;

					for (auto row_index = index_set.begin(); row_index != index_set.end(); ++row_index)
					{
						result.values.push_back((*value_row1) + table.values[*row_index]);
						result.table_rows++;
					}
				}
			}
		}

		return result;
	}

	if (index1 != this->indexes.end())
	{
		for (auto value_row2 = table.values.begin(); value_row2 != table.values.end(); ++value_row2)
		{
			if ((*value_row2).size() > 0)
			{
				const std::string& value = (*value_row2)[column_index2->second];

				auto index_node = index1->second.find(value);

				if (index_node != index1->second.end())
				{
					const std::set<int>& index_set = index_node->second;

					for (auto row_index = index_set.begin(); row_index != index_set.end(); ++row_index)
					{
						result.values.push_back(this->values[*row_index] + (*value_row2));
						result.table_rows++;
					}
				}
			}
		}

		return result;
	}

	for (auto value_row1 = this->values.begin(); value_row1 != this->values.end(); ++value_row1)
	{
		for (auto value_row2 = table.values.begin(); value_row2 != table.values.end(); ++value_row2)
		{
			if ((*value_row1).size() > 0 && (*value_row2).size() > 0)
			{
				const std::string& value1 = (*value_row1)[column_index1->second];
				const std::string& value2 = (*value_row2)[column_index2->second];

				if (value1 == value2)
				{
					result.values.push_back((*value_row1) + (*value_row2));
					result.table_rows++;
				}
			}
		}
	}

	return result;
}

Table Table::where(const Condition& condition) const
{
	if (condition.type == Condition::Type::VALUE_VALUE)
	{
		if (!condition.compare())
		{
			return Table(this->columns);
		}

		return *this;
	}

	if (condition.type == Condition::Type::NAME_VALUE)
	{
		const std::string& column_name = condition.left;

		auto column_index = this->columns_map.find(column_name);

		if (column_index == this->columns_map.end())
		{
			throw std::exception(("unknown column " + column_name).c_str());
		}

		auto index = this->indexes.find(column_name);

		if (index == this->indexes.end())
		{
			Table result(this->columns);

			for (auto value_row = this->values.begin(); value_row != this->values.end(); ++value_row)
			{
				if ((*value_row).size() > 0)
				{
					if (condition.compare((*value_row)[column_index->second]))
					{
						result.values.push_back(*value_row);
						result.table_rows++;
					}
				}
			}

			return result;
		}

		const std::string& condition_value = condition.right;

		if (condition.operation == Condition::Operation::EQUAL)
		{
			auto index_node = index->second.find(condition_value);

			if (index_node == index->second.end())
			{
				return Table(this->columns);
			}

			Table result(this->columns);

			const std::set<int>& index_set = index_node->second;

			for (auto row_index = index_set.begin(); row_index != index_set.end(); ++row_index)
			{
				result.values.push_back(this->values[*row_index]);
			}

			result.table_rows += index_set.size();

			return result;
		}

		if (condition.operation == Condition::Operation::NOT_EQUAL)
		{
			auto index_node = index->second.find(condition_value);

			if (index_node == index->second.end())
			{
				return *this;
			}

			Table result = *this;

			const std::set<int>& index_set = index_node->second;

			for (auto row_index = index_set.begin(); row_index != index_set.end(); ++row_index)
			{
				result.erase(*row_index);
			}

			return result;
		}

		//<, >, <=, >=

		Table result = *this;

		result.erase(condition.reverse());

		return result;
	}

	if (condition.type == Condition::Type::NAME_NAME)
	{
		const std::string& column_name1 = condition.left;
		const std::string& column_name2 = condition.right;

		auto column_index1 = this->columns_map.find(column_name1);
		auto column_index2 = this->columns_map.find(column_name2);

		if (column_index1 == this->columns_map.end())
		{
			throw std::exception(("unknown column " + column_name1).c_str());
		}

		if (column_index2 == this->columns_map.end())
		{
			throw std::exception(("unknown column " + column_name2).c_str());
		}

		Table result(this->columns);

		for (auto value_row = this->values.begin(); value_row != this->values.end(); ++value_row)
		{
			if ((*value_row).size() > 0)
			{
				const Array<std::string>& row = *value_row;

				if (condition.compare(row[column_index1->second], row[column_index2->second]))
				{
					result.values.push_back(row);
					result.table_rows++;
				}
			}
		}

		return result;
	}
}

Table Table::select(const Array<std::string>& columns) const
{
	int columns_size = columns.size();

	if (columns_size == 0)
	{
		return *this;
	}

	Array<int> columns_indexes(columns_size);

	for (int i = 0; i < columns_size; i++)
	{
		const std::string& column_name = columns[i];

		auto column_index = this->columns_map.find(column_name);

		if (column_index == this->columns_map.end())
		{
			throw std::exception(("unknown column " + column_name).c_str());
		}

		columns_indexes[i] = column_index->second;
	}

	Table result(columns);

	for (auto value_row = this->values.begin(); value_row != this->values.end(); ++value_row)
	{
		if ((*value_row).size() > 0)
		{
			result.values.push_back((*value_row) * columns_indexes);
			result.table_rows++;
		}
	}

	return result;
}

void print_border(const Array<int>& max_columns)
{
	std::cout << '+';

	int size = max_columns.size();

	for (int i = 0; i < size; i++)
	{
		for (int j = 0; j < max_columns[i] + 2; j++)
		{
			std::cout << '-';
		}

		std::cout << '+';
	}

	std::cout << std::endl;
}

void print_row(const Array<int>& max_columns, const Array<std::string>& values)
{
	std::cout << '|';

	int size = max_columns.size();

	for (int i = 0; i < size; i++)
	{
		std::cout << ' ';

		const std::string& value = values[i];

		std::cout << value;

		for (int j = 0; j < max_columns[i] - value.length() + 1; j++)
		{
			std::cout << ' ';
		}

		std::cout << '|';
	}

	std::cout << std::endl;
}

void Table::print() const
{
	int columns_size = this->columns.size();

	Array<int> max_columns(columns_size);

	for (int i = 0; i < columns_size; i++)
	{
		max_columns[i] = int(this->columns[i].length());
	}

	for (auto value_row = this->values.begin(); value_row != this->values.end(); ++value_row)
	{
		if ((*value_row).size() > 0)
		{
			for (int j = 0; j < columns_size; j++)
			{
				int value_length = (*value_row)[j].length();

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

	for (auto value_row = this->values.begin(); value_row != this->values.end(); ++value_row)
	{
		if ((*value_row).size() > 0)
		{
			print_row(max_columns, *value_row);
		}
	}

	print_border(max_columns);

	std::cout << "rows printed: " << this->table_rows << std::endl;
}



void Database::create(const std::string& table_name, const Array<std::string>& columns, const Array<std::string>& indexes)
{
	if (this->tables.find(table_name) != this->tables.end())
	{
		throw std::exception(("table " + table_name + " already exists").c_str());
	}

	int columns_size = columns.size();

	for (int i = 0; i < columns_size; i++)
	{
		for (int j = 0; j < columns_size; j++)
		{
			if (i != j && columns[i] == columns[j])
			{
				throw std::exception("few columns have the same name");
			}
		}
	}

	this->tables.emplace(table_name, Table(columns, indexes));

	std::cout << "Table " << table_name << " has been created successfully" << std::endl;
}

void Database::insert(const std::string& table_name, const Array<std::string>& values)
{
	this->operator[](table_name).insert(values);

	std::cout << "1 row was added to table " << table_name << std::endl;
}

void Database::erase(const std::string& table_name, const Condition& condition)
{
	int deleted_rows = this->operator[](table_name).erase(condition);

	std::cout << deleted_rows << " rows were removed from table " << table_name << std::endl;
}

void Database::select(const Array<std::string>& columns, const std::string& table_name_from, const std::string& table_name_join, const Join& join, const Condition& condition)
{
	if (table_name_join != "")
	{
		this->operator[](table_name_from).join(this->operator[](table_name_join), join).where(condition).select(columns).print();
	}

	else
	{
		this->operator[](table_name_from).where(condition).select(columns).print();
	}
}

Table& Database::operator[](const std::string& table_name)
{
	auto table = this->tables.find(table_name);

	if (table == this->tables.end())
	{
		throw std::exception(("unknown table " + table_name).c_str());
	}

	else
	{
		return table->second;
	}
}