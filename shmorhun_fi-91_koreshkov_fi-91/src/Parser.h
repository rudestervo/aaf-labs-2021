// #include<iostream>
#pragma once
#include<vector>
#include<algorithm>
#include<cctype>
#include<cstdlib>
#include<string>
#include "Set.h"
#include "Request.h"

const std::vector<std::string> KEYWOARDS = { "CREATE", "INSERT", "SEARCH", "WHERE", "INTERSECTS", "CONTAINS", "CONTAINED_BY" };

class RequestParser {
	static size_t strffind(bool (*filter)(char), std::string str) {
		size_t l = str.length();
		for (size_t i = 0; i < l; i++) {
			if (filter(str[i])) return i;
		}
		return std::string::npos;
	}

	struct parse_set_result {
		Set set;
		bool parsed;
		std::vector<std::string>::iterator end;
		std::string ms;
		static parse_set_result error(const std::string& err_msg) {
			parse_set_result r;
		    r.ms = err_msg;
			r.parsed = false;
			return r;
		}
	};
	static parse_set_result parse_set(
		std::vector<std::string>::iterator begin,
		std::vector<std::string>::iterator end) {
		parse_set_result r{ Set(), true, end };


		auto i = begin;
		for (; i != end; i++) {
			if (*i == "{") break;
		}
		if (i == end) return parse_set_result::error("No set at all");

		i++;

		enum { VAL, COMMA_OR_SPACE, END} state = VAL;
		for (; i != end; i++) {
			
			if ((*i)[0] == '}') {
				state = END;
				break;
			}
			if (state == VAL && (*i)[0] != '\0') {
				int val = 0;
				if ((*i)[0] != '0') {
				    
					for (int j = 0;  j < (*i).size(); j++)
					{
						if (!isdigit((*i)[j]))
						{

							return parse_set_result::error("Invalid syntax (Invalid number). Return empty set");
						}
					}
					val = strtol((*i).c_str(), nullptr, 10);
					if (val == 0) {

						return parse_set_result::error("Invalid syntax (Invalid symbol instead of number). Return empty set");
					}
				}
				r.set.Insert(val);
				state = COMMA_OR_SPACE;
			}
			else {
				if ((*i)[0] != ',' && (*i)[0] != '\0') {
					return parse_set_result::error("Invalid syntax (Invalid symbols in the input). Return empty set");
				}
				state = VAL;
			}

		}
		if (state != END) {
			return parse_set_result::error("Invalid syntax (Other symbols after `}` symbol).Return empty set");
		}
		r.end = i;

		return r;
	}

	static bool is_in(char c, const char* str) {
		auto i = str;
		while (*i != '\0') {
			if (c == *i) return true;
			i++;
		}
		return false;
	}
	static std::string toupper(const std::string& str) {
		std::string upper;
		for (char c : str) {
			upper += std::toupper(c);
		}
		return upper;
	}

public:
	static bool is_keyword(std::string str) {
		str = toupper(str);
		for (const std::string& kw : KEYWOARDS) {
			if (str == kw) return true;
		}
		return false;
	}

	std::string parse_error;

	Request parse(std::string str) {
		parse_error = "";
		Request req;
		const char* ws = " \n\r\t\v\f";
		const char* delims = "{,}";
		
		size_t start = str.find_first_not_of(ws);
		size_t end = str.length();

		std::vector<std::string> tokens;
		size_t pos = start;
		size_t token_start = start;
		while (pos < end) {
			bool on_start = token_start == pos;
			if (str[pos] == ';') {
				if (!on_start) {
					tokens.push_back(str.substr(token_start, pos - token_start));
				}
				break;
			}
			
			if (is_in(str[pos], delims)) {
				if (!on_start) {
					if (str[pos] == '{') {
						parse_error = "invalid syntax: unexpected '{'";
						return req;
					}
					tokens.push_back(str.substr(token_start, pos - token_start));
				}
				tokens.push_back(str.substr(pos, 1));
				token_start = pos = pos+1;
			}
			if (is_in(str[pos], ws)) {
				if (!on_start) {
					tokens.push_back(str.substr(token_start, pos - token_start));
				}
				token_start = pos = str.find_first_not_of(ws, pos);
			}
			else {
				pos++;
			}
		}

		auto it = tokens.begin();

		while (it != tokens.end())
		{
			if ((*it) == "")
			{
				it = tokens.erase(it);
			}
			if (it != tokens.end())
			{
				it++;
			}
		}


		if (token_start != pos && token_start < end) {
			tokens.push_back(str.substr(token_start, pos - token_start));
		}
		
		if (tokens.size() < 2) {
			req.command = Request::CMD_UNPARSED;
			parse_error = "too few tokens; parse aborted.";
			return req;
		}

		// token[0] is a command.
		// make cmd uppercase
		auto i_tok = tokens.begin();
		std::string cmd = toupper(*i_tok);


		if (cmd == "PRINT_TREE") {
			req.command = Request::CMD_PRINT_TREE;
			i_tok++;
			req.target = *i_tok;
		}
		else if (cmd == "CREATE") {
			req.command = Request::CMD_CREATE;
			i_tok++;
			req.target = *i_tok;
		}
		else if (cmd == "INSERT") {
			req.command = Request::CMD_INSERT;
			i_tok++;
			req.target = *i_tok;
			i_tok++;
			auto ps = parse_set(i_tok, tokens.end());
			if (!ps.parsed) {
				req.command = Request::CMD_UNPARSED;
				parse_error = "invalid syntax: cannot parse Set " + ps.ms;
				return req;
			}
			req.payload = ps.set;
			i_tok = ps.end;
		}
		else if (cmd == "CONTAINS") {
			req.command = Request::CMD_CONTAINS;
			i_tok++;
			req.target = *i_tok;
			i_tok++;
			auto ps = parse_set(i_tok, tokens.end());
			if (!ps.parsed) {
				parse_error = "invalid syntax: cannot parse Set " + ps.ms;
				req.command = Request::CMD_UNPARSED;
				return req;
			}
			req.payload = ps.set;
			i_tok = ps.end;
		}
		else if (cmd == "SEARCH") {
			i_tok++;
			req.target = *i_tok;
			i_tok++;
			if (i_tok == tokens.end()) {
				// select whole collection
				req.command = Request::CMD_SEARCH;
				return req;
			}
			// Skip validation of "WHERE" because i do not care
			i_tok++;
			if (i_tok == tokens.end()) {
				req.command = Request::CMD_UNPARSED;
				parse_error = "invalid syntax: SEARCH WHERE command has no filter.";
				return req;
			}

			std::string filter = toupper(*i_tok);
			if (filter == "INTERSECTS") {
				req.filter = Request::FILTER_INTERSECTS;
			} 
			else if (filter == "CONTAINS") {
				req.filter = Request::FILTER_SUPERSET;
			}
			else if (filter == "CONTAINED_BY") {
				req.filter = Request::FILTER_SUBSET;
			}
			else {
				req.command = Request::CMD_UNPARSED;
				parse_error = "invalid syntax: SEARCH WHERE command has invalid filter.";
				return req;
			}
			req.command = Request::CMD_SEARCH_WHERE;

			i_tok++;

			auto ps = parse_set(i_tok, tokens.end());
			if (!ps.parsed) {
				req.command = Request::CMD_UNPARSED;
				parse_error = "invalid syntax: cannot parse Set " + ps.ms;
				return req;
			}
			req.payload = ps.set;
			i_tok = ps.end;
		}
		else {
			req.command = Request::CMD_UNPARSED;
			parse_error = "unknown command";
			return req;
		}
		i_tok++;
		if (i_tok != tokens.end()) {
			req.command = Request::CMD_UNPARSED;
			parse_error = "invalid syntax: extra tokens after the end of command";
			return req;
		}
		if (is_keyword(req.target)) {
			req.command = Request::CMD_UNPARSED;
			parse_error = "invalid target: target cannot be a keyword";
			return req;
		}
		return req;
	}
};
