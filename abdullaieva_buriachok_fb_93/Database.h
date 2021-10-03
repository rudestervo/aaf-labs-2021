#pragma once
#include "List.h"
#include "Array.h"
#include "Tree.h"
#include "Condition.h"

using namespace std;

class Table
{
private:
	Array<string> columns;
	Tree<string, int> columns_tree;

	Array<string> indexes;
	Tree<string, int> indexes_tree;
	Array<Tree<string, int>> indexes_array;

	List<Array<string>> values;

public:
	Table();

	Table(const Array<string>& columns);

	Table(const Array<string>& columns, const Array<string>& indexes);

	Table(const Array<string>& columns, const Array<string>& indexes, const List<Array<string>>& values);

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
	List<Table> tables;
	Tree<string, int> tables_tree;

public:
	void create(string table_name, const Array<string>& columns, const Array<string>& indexes);

	void insert(string table_name, const Array<string>& values);

	void erase(string table_name, const Condition& condition);

	void select(const Array<string>& columns, string table_name_from, string table_name_join, const Condition& condition_join, const Condition& condition_where) const;

	Table& operator[](string table_name) const;
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
		this->columns_tree.insert(this->columns[i], i);
	}
}

Table::Table(const Array<string>& columns, const Array<string>& indexes)
{
	this->columns = columns;

	int columns_size = this->columns.size();

	for (int i = 0; i < columns_size; i++)
	{
		this->columns_tree.insert(this->columns[i], i);
	}

	this->indexes = indexes;

	int indexes_size = this->indexes.size();

	for (int i = 0; i < indexes_size; i++)
	{
		this->indexes_tree.insert(this->indexes[i], i);
	}

	this->indexes_array = Array<Tree<string, int>>(indexes_size);
}

Table::Table(const Array<string>& columns, const Array<string>& indexes, const List<Array<string>>& values)
{
	this->columns = columns;

	int columns_size = this->columns.size();

	for (int i = 0; i < columns_size; i++)
	{
		this->columns_tree.insert(this->columns[i], i);
	}

	this->indexes = indexes;

	int indexes_size = this->indexes.size();

	this->indexes_array = Array<Tree<string, int>>(indexes_size);

	for (int i = 0; i < indexes_size; i++)
	{
		this->indexes_tree.insert(this->indexes[i], i);
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
		this->columns_tree.insert(this->columns[i], i);
	}

	this->indexes = table.indexes;

	int indexes_size = this->indexes.size();

	this->indexes_array = Array<Tree<string, int>>(indexes_size);

	for (int i = 0; i < indexes_size; i++)
	{
		this->indexes_tree.insert(this->indexes[i], i);
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
		cerr << "неправильное количество параметров";	throw;

		return false;
	}

	else
	{
		int indexes_size = this->indexes.size();

		for (int i = 0; i < indexes_size; i++)//проходим по всем индексам и проверяем на повторяющиеся значения
		{
			string column_name = this->indexes[i];
			
			int column_index = this->columns_tree.find(column_name);

			if (this->indexes_array[i].check(values[column_index]))
			{
				cerr << "такая запись уже есть";	throw;

				return false;
			}
		}
		
		this->values.push_back(values);//добавляем строку в список

		int row_index = this->values.size() - 1;//индекс новой строки

		for (int i = 0; i < indexes_size; i++)//проходим по всем индексам и добавляем новый узел дерева
		{
			string column_name = this->indexes[i];

			int column_index = this->columns_tree.find(column_name);

			this->indexes_array[i].insert(values[column_index], row_index);
		}

		return true;
	}
}

void Table::erase(const int row_index)
{
	if (row_index >= this->values.size() || row_index < 0)
	{
		cerr << "неизвестный номер строки";	throw;
	}

	else
	{
		int indexes_size = this->indexes.size();//удаляем индексы
		
		for (int i = 0; i < indexes_size; i++)
		{
			int column_index = this->indexes_tree.find(this->indexes[i]);

			string value = values[row_index][column_index];

			this->indexes_array[i].erase(value);
		}

		this->values.erase(row_index);//удаляем строку
	}
}

int Table::erase(const Condition& condition)
{
	int condition_type = condition.get_type();

	if (condition_type == 0)//VALUE ? VALUE
	{
		if (condition.get_value())//удаляем все значения
		{
			int values_size = this->values.size();

			this->values = List<Array<string>>();//обнуляем значения

			this->indexes_array = Array<Tree<string, int>>(this->indexes.size());//убираем деревья индексов

			return values_size;
		}

		else//не удаляем ничего
		{
			return 0;
		}
	}

	else if (condition_type == 1)//NAME ? VALUE
	{
		string column_name = condition.get_left();

		if (!this->columns_tree.check(column_name))
		{
			cerr << "неизвестная колонка " << column_name;	throw;
		}

		else
		{
			if (this->indexes_tree.check(column_name))//у column_name есть индексы
			{
				int column_index = this->indexes_tree.find(column_name);//номер в индексах

				string condition_operation = condition.get_operation();
				string condition_value = condition.get_right();

				condition_value = condition_value.substr(1, condition_value.length() - 2);//убираем кавычки

				if (condition_operation == "=")
				{
					if (this->indexes_array[column_index].check(condition_value))//убрать только одну строку
					{
						int row_index = this->indexes_array[column_index].find(condition_value);
						
						this->erase(row_index);

						return 1;
					}

					else//не менять таблицу
					{
						return 0;
					}
				}

				else if (condition_operation == "!=")
				{
					int values_size = this->values.size();

					if (this->indexes_array[column_index].check(condition_value))//удалить все, кроме одной строки
					{
						int values_size = this->values.size();

						int row_index = this->indexes_array[column_index].find(condition_value);

						Array<string> row = this->values[row_index];//запомнили строку

						this->values = List<Array<string>>();//обнуляем значения

						this->indexes_array = Array<Tree<string, int>>(this->indexes.size());//убираем деревья индексов
						
						this->insert(row);//добавляэм эдинственную строку

						return values_size - 1;
					}

					else//удалить все значения
					{
						int values_size = this->values.size();

						this->values = List<Array<string>>();//обнуляем значения

						this->indexes_array = Array<Tree<string, int>>(this->indexes.size());//убираем деревья индексов

						return values_size;
					}
				}

				else//<, >, <=, >=
				{
					Array<int> rows_array;//строки, которые нужно убрать

					bool is_equal = condition_operation.length() == 2;//<=, >=

					if (condition_operation[0] == '<')//asc
					{
						rows_array = this->indexes_array[column_index].inorder_asc(condition_value, is_equal).to_array();
					}

					else//desc
					{
						rows_array = this->indexes_array[column_index].inorder_desc(condition_value, is_equal).to_array();
					}

					rows_array.sort();//сортируем по возростанию

					int rows_size = rows_array.size();

					int counter = 0;//змещение после удаления

					for (int i = 0; i < rows_size; i++)
					{
						this->erase(rows_array[i] - counter);
					}

					return counter;
				}
			}

			else//у column_name нет индексов
			{
				int counter = 0;//змещение после удаления

				int column_index = this->columns_tree.find(column_name);

				int values_size = this->values.size();

				//перебираем все строки и удаляем те, где условие выполняется

				for (int i = 0; i < values_size; i++)
				{
					string value = this->values[i - counter][column_index];

					if (condition.get_value(value))
					{
						this->erase(i - counter);
						counter++;
					}
				}

				return counter;
			}
		}
	}

	else//NAME ? NAME
	{
		string column_name1 = condition.get_left();
		string column_name2 = condition.get_right();

		if (!this->columns_tree.check(column_name1))
		{
			cerr << "неизвестная колонка " << column_name1;	throw;
		}

		else if (!this->columns_tree.check(column_name2))
		{
			cerr << "неизвестная колонка" << column_name2;	throw;
		}

		else
		{
			int counter = 0;//змещение после удаления

			int column_index1 = this->columns_tree.find(column_name1);
			int column_index2 = this->columns_tree.find(column_name2);
			
			int values_size = this->values.size();

			//перебираем все строки и удаляем те, где условие выполняется

			for (int i = 0; i < values_size; i++)
			{
				Array<string> row = this->values[i - counter];
				
				string value1 = row[column_index1];
				string value2 = row[column_index2];

				if (condition.get_value(value1, value2))
				{
					this->erase(i - counter);
					counter++;
				}
			}

			return counter;
		}
	}
}

Table Table::join(const Table& table, const Condition& condition) const
{
	if (condition.get_type() == 0)//JOIN
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

	else//JOIN ON
	{
		string column_name1 = condition.get_left(), column_name2 = condition.get_right();
		
		if (!this->columns_tree.check(column_name1))
		{
			cerr << "неизвестная колонка" << column_name1;	throw;
		}

		else if (!table.columns_tree.check(column_name2))
		{
			cerr << "неизвестная колонка" << column_name2;	throw;
		}

		else
		{
			int column_index1 = this->columns_tree.find(column_name1);
			int column_index2 = table.columns_tree.find(column_name2);
			
			Table result;

			result.columns = this->columns + table.columns;

			int values_size1 = this->values.size(), values_size2 = table.values.size();

			if (table.indexes_tree.check(column_name2))//у column_name2 есть индексов
			{
				column_index2 = table.indexes_tree.find(column_name2);//номер в массиве индексов
				
				for (int i = 0; i < values_size1; i++)
				{
					string value = this->values[i][column_index1];

					if (table.indexes_array[column_index2].check(value))//во второй таблице есть такое значение
					{
						int row = table.indexes_array[column_index2].find(value);

						result.values.push_back(this->values[i] + table.values[row]);
					}
				}
			}

			else//у column_name2 нет индексов
			{
				//перебираем все строки и "умножаем" их
				
				for (int i = 0; i < values_size1; i++)
				{
					for (int j = 0; j < values_size2; j++)
					{
						string value1 = this->values[i][column_index1];
						string value2 = this->values[i][column_index2];

						if (condition.get_value(value1, value2))
						{
							result.values.push_back(this->values[i] + table.values[j]);
						}
					}
				}
			}

			return result;
		}
	}
}

Table Table::where(const Condition& condition) const
{
	int condition_type = condition.get_type();

	if (condition_type == 0)//VALUE ? VALUE
	{
		if (condition.get_value())
		{
			return Table(this->columns, this->indexes, this->values);//this таблица
		}

		else
		{
			return Table(this->columns, this->indexes);//структура this таблицы, но без значений
		}
	}

	else if (condition_type == 1)//NAME ? VALUE
	{
		string column_name = condition.get_left();

		if (!this->columns_tree.check(column_name))
		{
			cerr << "неизвестная колонка " << column_name;	throw;
		}

		else
		{
			if (this->indexes_tree.check(column_name))//у column_name есть индексы
			{
				int column_index = this->indexes_tree.find(column_name);//номер в индексах

				string condition_operation = condition.get_operation();
				string condition_value = condition.get_right();

				condition_value = condition_value.substr(1, condition_value.length() - 2);//убираем кавычки

				if (condition_operation == "=")
				{
					if (this->indexes_array[column_index].check(condition_value))//вернуть только одну строку
					{
						int rows_index = this->indexes_array[column_index].find(condition_value);

						Table result(this->columns, this->indexes);

						result.insert(this->values[rows_index]);//добавляем найденную строчку

						return result;
					}

					else//вернуть пустую таблицу
					{
						return Table(this->columns, this->indexes);
					}
				}

				else if (condition_operation == "!=")
				{
					int values_size = this->values.size();

					if (this->indexes_array[column_index].check(condition_value))//вернуть все, кроме одной строки
					{
						int index_value = this->indexes_array[column_index].find(condition_value);

						Table result(this->columns, this->indexes, this->values);//копия таблицы

						result.erase(index_value);//удаляем одну строчку

						return result;
					}

					else//вернуть всю таблицу
					{
						return Table(this->columns, this->indexes, this->values);
					}
				}

				else//<, >, <=, >=
				{
					Array<int> rows_array;//строки, которые нужно взять

					bool mode = condition_operation.length() == 2;//<=, >=

					if (condition_operation[0] == '<')//asc
					{
						rows_array = this->indexes_array[column_index].inorder_asc(condition_value, mode).to_array();
					}

					else//desc
					{
						rows_array = this->indexes_array[column_index].inorder_desc(condition_value, mode).to_array();
					}

					Table result(this->columns, this->indexes);

					rows_array.sort();

					int rows_size = rows_array.size();

					for (int i = 0; i < rows_size; i++)
					{
						result.insert(this->values[rows_array[i]]);
					}

					return result;
				}
			}

			else//у column_name нет индексов
			{
				Table result(this->columns, this->indexes);

				int column_index = this->columns_tree.find(column_name);

				int values_size = this->values.size();

				//перебираем все строки и добавляем те, для которых выполняется условие
				
				for (int i = 0; i < values_size; i++)
				{
					Array<string> row = values[i];
					
					if (condition.get_value(row[column_index]))
					{
						result.insert(row);
					}
				}

				return result;
			}
		}
	}

	else//NAME ? NAME
	{
		string column_name1 = condition.get_left();
		string column_name2 = condition.get_right();

		if (!this->columns_tree.check(column_name1))
		{
			cerr << "неизвестная колонка " << column_name1;	throw;
		}

		else if (!this->columns_tree.check(column_name2))
		{
			cerr << "неизвестная колонка " << column_name2;	throw;
		}

		else
		{
			Table result(this->columns, this->indexes);
			
			int column_index1 = this->columns_tree.find(column_name1);
			int column_index2 = this->columns_tree.find(column_name2);

			int values_size = this->values.size();

			//перебираем все строки и добавляем те, для которых выполняется условие
			
			for (int i = 0; i < values_size; i++)
			{
				Array<string> row = values[i];
				
				if (condition.get_value(row[column_index1], row[column_index2]))
				{
					result.insert(row);
				}
			}

			return result;
		}
	}
}

Table Table::select(const Array<string>& columns) const
{
	int columns_size = columns.size();

	if (columns_size == 0)//все колонки таблицы
	{
		return Table(this->columns, this->indexes, this->values);//таблица this
	}

	else
	{
		List<int> columns_list;//номера колонок, которые нужно выбрать

		List<int> indexes_list;//номера индексов, которые нужно выбрать

		for (int i = 0; i < columns_size; i++)
		{
			if (!this->columns_tree.check(columns[i]))
			{
				cerr << "неизвестная колонка";	throw;
			}

			else
			{
				int column_index = this->columns_tree.find(columns[i]);
				
				columns_list.push_back(column_index);
			}

			if (this->indexes_tree.check(columns[i]))
			{
				int index_index = this->indexes_tree.find(columns[i]);
				
				indexes_list.push_back(index_index);
			}
		}

		Array<int> columns_indexes = columns_list.to_array();

		Array<int> indexes_indexes = indexes_list.to_array();

		int indexes_size = indexes_indexes.size();

		Array<string> new_indexes = this->indexes * indexes_indexes;//выбираем нужные индексы

		List<Array<string>> new_values;

		int values_size = this->values.size();

		for (int i = 0; i < values_size; i++)
		{
			new_values.push_back(this->values[i] * columns_indexes);//выбираем нужные колонки строк
		}

		return Table(columns, new_indexes, new_values);
	}
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

	print_border(max_columns);//+---+---+---+

	print_row(max_columns, this->columns);

	print_border(max_columns);//+---+---+---+

	for (int i = 0; i < values_size; i++)
	{
		print_row(max_columns, this->values[i]);
	}

	print_border(max_columns);//+---+---+---+
}





void Database::create(string table_name, const Array<string>& columns, const Array<string>& indexes)
{
	if (this->tables_tree.check(table_name))
	{
		cerr << "таблица table_name уже есть";	throw;
	}

	else
	{
		int columns_size = columns.size();
		
		for (int i = 0; i < columns_size; i++)
		{
			for (int j = 0; j < columns_size; j++)
			{
				if (i != j && columns[i] == columns[j])
				{
					cerr << "несколько колонок имеют одинаковые названия";	throw;
				}
			}
		}

		Table new_table(columns, indexes);
		
		this->tables.push_back(new_table);//добавляем таблицу в список

		int table_index = this->tables.size() - 1;

		this->tables_tree.insert(table_name, table_index);//добавляет запись в дерево

		cout << "Таблица " << table_name << " успешно создана" << endl;
	}
}

void Database::insert(string table_name, const Array<string>& values)
{
	bool inserted_rows = this->operator[](table_name).insert(values);

	cout << "В таблицу " << table_name << " была добавлена " << inserted_rows << " строк(а)" << endl;
}

void Database::erase(string table_name, const Condition& condition)
{
	int deleted_rows = this->operator[](table_name).erase(condition);

	cout << "Из таблицы " << table_name << " было удалено " << deleted_rows << " строк(а/и)" << endl;
}

void Database::select(const Array<string>& columns, string table_name_from, string table_name_join, const Condition& condition_join, const Condition& condition_where) const
{
	if (table_name_join != "")//JOIN
	{
		this->operator[](table_name_from).join(this->operator[](table_name_join), condition_join).where(condition_where).select(columns).print();
	}

	else
	{
		this->operator[](table_name_from).where(condition_where).select(columns).print();
	}
}

Table& Database::operator[](string table_name) const
{
	if (!this->tables_tree.check(table_name))
	{
		cerr << "таблица table_name не найдена";	throw;
	}

	else
	{
		int table_index = this->tables_tree.find(table_name);
		
		return this->tables[table_index];
	}
}