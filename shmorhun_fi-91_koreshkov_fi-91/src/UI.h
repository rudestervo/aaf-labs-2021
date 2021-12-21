#pragma once
#include "DB.h"
#include <string>
#include <iostream>
#include "Collection.h"
#include "Parser.h"

class UI {
	DB database;
	const std::map<const std::string, Collection>& collections;

	RequestParser sql_parser;

	bool exit;
	std::string last_input;
	size_t offset;

	const char* WHITESPACE = " \n\r\t\v\f";
	const std::string EXIT_CMD = "exit";
	const std::string SHOW_CMD = "show";

	enum CMD_CODE {
		CODE_INVALID = -1,
		CODE_EXIT = 0,
		CODE_SHOW,

		CODE_DB_ERR,
		CODE_DB_OK,
		CODE_SQL_ERROR
	};

	std::string prefix;
	std::string suffix;

	void Output(std::string str) {
		std::cout << prefix << " > " << suffix;
		for (char& c : str) {
			if (c == '\n') {
				std::cout << prefix << " > " << suffix;
			}
			std::cout << c;
		}
		std::cout << std::endl;
	}

	int ParseCommand() {
		if (last_input.substr(offset, EXIT_CMD.length()) == EXIT_CMD) {
			return CODE_EXIT;
		}
		if (last_input.substr(offset, SHOW_CMD.length()) == SHOW_CMD) {
			return CODE_SHOW;
		}
		return CODE_INVALID;
	}

	int Input() {
		offset = 0;
		std::getline(std::cin, last_input, ';');
		// Strip whitespace in front of the command
		last_input = last_input.substr(last_input.find_first_not_of(WHITESPACE));

		if (last_input[0] == ':') {
			// Command, not sql request
			offset = 1;
			size_t code = ParseCommand();
			if (code == CODE_INVALID) {
				Output("Invalid command");
			}
			else if (code == CODE_SHOW) {
				Output("Collections:");
				suffix = "  - ";
				for (auto c : collections) {
					Output(c.first);
				}
				suffix = "";
			}
			return code;
		}

		Request sql_req = sql_parser.parse(last_input);
		if (sql_parser.parse_error.empty()) {
			// Success
			Output("SQL request parsed:");
			std::cout << sql_req;

			DB::Result db_res;

			if (sql_req.command == Request::CMD_CREATE) {
				db_res = database.Create(sql_req.target);
				if (db_res.error) {
					Output("Database error:");
					Output("  " + db_res.msg);
					return CODE_DB_ERR;
				}

				Output("Request successful:");
				suffix = "  ";
				Output(db_res.msg);
				suffix = "";
				if (!db_res.data.empty()) {
					Output("Data:");
					for (Set& s : db_res.data) {
						std::cout << prefix << " > " << s;
					}
				}
				return CODE_DB_OK;
			}

			if (sql_req.command == Request::CMD_INSERT) {
				db_res = database.Insert(sql_req.target, sql_req.payload);
				if (db_res.error) {
					Output("Database error:");
					Output("  " + db_res.msg);
					return CODE_DB_ERR;
				}

				Output("Request successful:");
				suffix = "  ";
				Output(db_res.msg);
				suffix = "";
				return CODE_DB_OK;
			}

			if (sql_req.command == Request::CMD_PRINT_TREE) {
				db_res = database.PrintTree(sql_req.target, std::cout);

				if (db_res.error) {
					Output("Database error:");
					Output("  " + db_res.msg);
					return CODE_DB_ERR;
				}

				Output("Request successful:");
				suffix = "  ";
				Output(db_res.msg);
				suffix = "";
				return CODE_DB_OK;
			}

			if (sql_req.command == Request::CMD_CONTAINS) {
				db_res = database.Contains(sql_req.target, sql_req.payload);

				if (db_res.error) {
					Output("Database error:");
					Output("  " + db_res.msg);
					return CODE_DB_ERR;
				}

				Output("Request successful:");
				suffix = "  ";
				Output(db_res.msg);
				suffix = "";
				return CODE_DB_OK;
			}
			
			if (sql_req.command == Request::CMD_SEARCH) {
				
				db_res = database.Search(sql_req.target);

				if (db_res.error) {
					Output("Database error:");
					Output("  " + db_res.msg);
					return CODE_DB_ERR;
				}

				Output("Request successful:");
				suffix = "  ";
				Output(db_res.msg);
				suffix = "";
				return CODE_DB_OK;
			}

			if (sql_req.filter == Request::FILTER_INTERSECTS) {

				db_res = database.Intersects(sql_req.target, sql_req.payload);

				if (db_res.error) {
					Output("Database error:");
					Output("  " + db_res.msg);
					return CODE_DB_ERR;
				}

				Output("Request successful:");
				suffix = "  ";
				Output(db_res.msg);
				suffix = "";
				return CODE_DB_OK;
			}

			if (sql_req.filter == Request::FILTER_SUPERSET) {

				db_res = database.Contains_Search(sql_req.target, sql_req.payload);

				if (db_res.error) {
					Output("Database error:");
					Output("  " + db_res.msg);
					return CODE_DB_ERR;
				}

				Output("Request successful:");
				suffix = "  ";
				Output(db_res.msg);
				suffix = "";
				return CODE_DB_OK;
			}

			if (sql_req.filter == Request::FILTER_SUBSET) {

				db_res = database.Contained_By(sql_req.target, sql_req.payload);
				if (db_res.error) {
					Output("Database error:");
					Output("  " + db_res.msg);
					return CODE_DB_ERR;
				}

				Output("Request successful:");
				suffix = "  ";
				Output(db_res.msg);
				suffix = "";
				return CODE_DB_OK;
			}



			Output("Unknown/unimplemented command");
			return CODE_SQL_ERROR;
		}
		else {
			Output("Invalid SQL request:");
			Output("  \"" + sql_parser.parse_error + "\"");
			return CODE_SQL_ERROR;
		}
	}


public:
	UI() : exit(false), database(), collections(database.GetCollections()) {

	}

	int REPL() {
		std::cout << "--- This is REPL.V1 ---" << std::endl;
		std::cout << "(special commands are :exit, :show)" << std::endl;
		std::cout << "(every command and sql request must end with a semicolon ';')" << std::endl;

		while (!exit) {
			std::cout << std::endl << "$ ";
			auto code = Input();
			if (code == CODE_EXIT) {
				exit = true;
			}
		}
		std::cout << "Bye!";
		return 0;
	}
};