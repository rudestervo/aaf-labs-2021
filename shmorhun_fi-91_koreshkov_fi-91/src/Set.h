#pragma once
#include <vector>
#include <algorithm>
#include <iostream>

// Set

class Set {
public:
	static const size_t DEFAULT_SZ = 8;
	std::vector<int> data;
	Set(std::vector<int> _data) {
		std::sort(_data.begin(), _data.end());
		auto last = std::unique(_data.begin(), _data.end());
		data.insert(data.begin(), _data.begin(), last);
	}
	Set() {}

	size_t Size() const { return data.size(); }

	bool Contains(int x) const;
	bool Insert(int x);
	bool Delete(int x);

	Set Union(const Set& other) const;
	Set Intersection(const Set& other) const;
	Set Minus(const Set& other) const;

	bool IsSubsetOf(const Set& other) const;
	bool IsDisjointWith(const Set& other) const;

	friend std::ostream& operator<<(std::ostream&, const Set&);
	friend bool operator== (const Set& lhs, const Set& rhs) {
		return lhs.data == rhs.data;
	}
};

