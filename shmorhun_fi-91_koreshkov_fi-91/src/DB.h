#pragma once
#include "Collection.h"
#include "Request.h"
#include <string>
#include <map>

class DB {
public:
	struct Result {
		bool error;
		std::vector<Set> data;
		std::string msg;

		Result() : error(false) {}

		static Result Error(const std::string& msg) {
			Result res;
			res.error = true;
			res.msg = msg;
			return res;
		}
		static Result Success(const std::string& msg) {
			Result res;
			res.error = false;
			res.msg = msg;
			return res;
		}

	};

private:
	std::string db_name;
	std::map<const std::string, Collection> collections;

public:
	void PrintSets(std::vector<Set> sets_collection) {
		auto it = sets_collection.begin();
		while (it != sets_collection.end())
		{
			std::cout << *it << ' ';
			it++;
		}
		std::cout << std::endl;
	}

	Result Create(std::string collection_name) {
		const auto pair = collections.try_emplace(collection_name);

		const auto it = pair.first;
		const auto collectionCreated = pair.second;

		if (!collectionCreated) {
			std::string msg = "Collection '" + collection_name + "' already exists";
			return Result::Error(msg);
		}

		std::string msg = "Collection '" + collection_name + "' created successfully";
		return Result::Success(msg);
	}

	Result Insert(std::string collection_name, Set insert_set) {
		const auto it = collections.find(collection_name);

		if (it == collections.end()) {
			std::string msg = "Collection '" + collection_name + "' does not exist";
			return Result::Error(msg);
		}

		it->second.Insert(insert_set);

		return Result::Success("1 set inserted.");
	}

	Result InsertAll(std::string collection_name, std::vector<Set> insert_sets) {
		const auto it = collections.find(collection_name);

		if (it == collections.end()) {
			std::string msg = "Collection '" + collection_name + "' does not exist";
			return Result::Error(msg);
		}

		for (const Set& insert_set : insert_sets) {
			it->second.Insert(insert_set);
		}

		return Result::Success(std::to_string(insert_sets.size()) + " sets inserted.");
	}

	Result PrintTree(std::string collection_name, std::ostream& os) {
		const auto it = collections.find(collection_name);

		if (it == collections.end()) {
			std::string msg = "Collection '" + collection_name + "' does not exist";
			return Result::Error(msg);
		}

		it->second.Print(os);

		return Result::Success("");
	}

	Result Contains(std::string collection_name, Set check_set) {
		const auto it = collections.find(collection_name);

		if (it == collections.end()) {
			std::string msg = "Collection '" + collection_name + "' does not exist";
			return Result::Error(msg);
		}

		if (it->second.Contains(check_set) == true)
		{
			return Result::Success("True (Set exist in tree)");
		}
		else
		{
			return Result::Success("False (Set does not exist in tree)");
		}

	}

	Result Search(std::string collection_name) {

		const auto it = collections.find(collection_name);

		if (it == collections.end()) {
			std::string msg = "Collection '" + collection_name + "' does not exist";
			return Result::Error(msg);
		}
		std::vector<Set> res = it->second.Search();
		if (res.size() == 0)
		{
			return Result::Success("No sets it this database");
		}
		else
		{
			PrintSets(res);
			return Result::Success("Found sets");
		}

	}

	Result Intersects(std::string collection_name, Set intersec_set) {

		const auto it = collections.find(collection_name);

		if (it == collections.end()) {
			std::string msg = "Collection '" + collection_name + "' does not exist";
			return Result::Error(msg);
		}
		std::vector<Set> res = it->second.Intersects(intersec_set);
		if (res.size() == 0)
		{
			return Result::Success("No sets in this database");
		}
		else
		{
			PrintSets(res);
			return Result::Success("Found sets");
		}

	}

	Result Contains_Search(std::string collection_name, Set subset) {

		const auto it = collections.find(collection_name);

		if (it == collections.end()) {
			std::string msg = "Collection '" + collection_name + "' does not exist";
			return Result::Error(msg);
		}
		std::vector<Set> res = it->second.Contains_Search(subset);
		if (res.size() == 0)
		{
			return Result::Success("No sets in this database");
		}
		else
		{
			PrintSets(res);
			return Result::Success("Found sets");
		}

	}

	Result Contained_By(std::string collection_name, Set superset) {

		const auto it = collections.find(collection_name);

		if (it == collections.end()) {
			std::string msg = "Collection '" + collection_name + "' does not exist";
			return Result::Error(msg);
		}
		std::vector<Set> res = it->second.Contained_By(superset);
		if (res.size() == 0)
		{
			return Result::Success("No sets in this database");
		}
		else
		{
			PrintSets(res);
			return Result::Success("Found sets");
		}
	}




		const std::map<const std::string, Collection>& GetCollections() const { return collections; }
	};