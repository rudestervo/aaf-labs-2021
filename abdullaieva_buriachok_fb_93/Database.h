#pragma once
#include <string>
#include <deque>
#include <map>
#include <set>
#include "Array.h"
#include "Condition.h"
#include "Join.h"

class Table
{
private:
	Array<std::string> columns;
	std::map<std::string, int> columns_map;

	std::map<std::string, std::map<std::string, std::set<int>>> indexes;

	std::deque<Array<std::string>> values;
	int table_rows;

public:
	Table();

	Table(const Array<std::string>& columns);

	Table(const Array<std::string>& columns, const Array<std::string>& indexes);

	Table(const Array<std::string>& columns, const std::map<std::string, std::map<std::string, int>>& indexes);

	Table(const Array<std::string>& columns, const std::map<std::string, std::map<std::string, int>>& indexes, const std::deque<Array<std::string>>& values);

	Table(const Table& table);

	void insert(const Array<std::string>& values);

	void erase(const int row_index);

	int erase(const Condition& condition);

	Table join(const Table& table, const Join& join) const;

	Table where(const Condition& condition) const;

	Table select(const Array<std::string>& columns) const;

	void print() const;
};



class Database
{
private:
	std::map<std::string, Table> tables;

public:
	void create(const std::string& table_name, const Array<std::string>& columns, const Array<std::string>& indexes);

	void insert(const std::string& table_name, const Array<std::string>& values);

	void erase(const std::string& table_name, const Condition& condition);

	void select(const Array<std::string>& columns, const std::string& table_name_from, const std::string& table_name_join, const Join& join, const Condition& condition);

	Table& operator[](const std::string& table_name);
};