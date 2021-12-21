#pragma once
#include "Collection.h"

/*
* cmd:
* - CREATE <target>;                    ::  create collection
*     - <target>  :: str, collection name
*     - (<payload> is empty)
*     - (<filter> is empty)
*
* - INSERT [INTO] <target> <payload>;   ::  insert set in colection
*     - <target>  :: str, collection where to insert
*     - <payload> :: vector<int>
*     - (<filter> is empty)
*
* - SEARCH <target>;                    :: show all from <target> collection
*     - <target>  :: str, collection where to search
*     - (<payload> is empty)
*     - (<filter> is empty)
*
* - SEARCH <target> where <filter> <payload>;                    :: show all from <target> collection
*     - <target>  :: str, collection where to search
*     - <payload> :: vector<int>
*     - <filter>  :: int
*
*/

class Request {
public:

	static const int CMD_UNPARSED = -1;
	static const int CMD_CREATE = 10;
	static const int CMD_INSERT = 20;
	static const int CMD_SEARCH = 30;
	static const int CMD_SEARCH_WHERE = 40;
	static const int CMD_CONTAINS = 50;
	static const int CMD_PRINT_TREE = 60;

	static const int FILTER_INTERSECTS = 100;
	static const int FILTER_SUBSET = 200;
	static const int FILTER_SUPERSET = 300;

	int command;
	std::string target;
	Set payload;
	int filter;

	friend std::ostream& operator<<(std::ostream& os, const Request& req);
};

std::ostream& operator<<(std::ostream& os, const Request& req) {
	if (!(req.command == Request::CMD_UNPARSED))
	{
	os << "Request {" << std::endl << "  command: ";
	if (req.command == Request::CMD_CREATE) {
		os << "CREATE";
	}
	else if (req.command == Request::CMD_INSERT) {
		os << "INSERT";
	}
	else if (req.command == Request::CMD_CONTAINS) {
		os << "CONTAINS";
	}
	else if (req.command == Request::CMD_SEARCH) {
		os << "SEARCH";
	}
	else if (req.command == Request::CMD_SEARCH_WHERE) {
		os << "SEARCH_WHERE";
	}
	else if (req.command == Request::CMD_PRINT_TREE) {
		os << "PRINT_TREE";
	}
	//else if (req.command == CMD_UNPARSED) {
	//	os << "unparsed";
	//}

		os << std::endl << "  target: '";
		os << req.target << "'" << std::endl << "  payload: " << req.payload << std::endl << "  filter: ";
		if (req.filter == Request::FILTER_INTERSECTS) {
			os << "(intersects)";
		}
		else if (req.filter == Request::FILTER_SUBSET) {
			os << "(subset)";
		}
		else if (req.filter == Request::FILTER_SUPERSET) {
			os << "(superset)";
			}
		os << std::endl << "}" << std::endl;
		return os;
		 
	}
	else
	{
		os << "command unparsed.";
		return os;
	}

}
