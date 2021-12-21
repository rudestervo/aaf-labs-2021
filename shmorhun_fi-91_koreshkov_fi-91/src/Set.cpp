#include "Set.h"


bool Set::Contains(int x) const
{
	return std::binary_search(data.begin(), data.end(), x);
}

bool Set::Insert(int x) {
	for (auto i = data.begin(); i != data.end(); i++) {
		if (x == *i) {
			// X is already in the set
			return 0;
		}
		if (x < *i) {
			// insert before.
			data.insert(i, x);
			return true;
		}
	}
	// if x > every elem of set, push it to the end
	data.push_back(x);
	return true;
}

bool Set::Delete(int x) {
	for (auto i = data.begin(); i != data.end(); i++) {
		if (*i > x) {
			// X is not in the set
			return 0;
		}
		if (*i == x) {
			data.erase(i);
			return 1;
		}
	}
	return 0;
}

Set Set::Union(const Set& other) const {
	Set u = Set();
	auto i = data.begin();
	auto j = other.data.begin();
	while (i != data.end() && j != other.data.end()) {
		if (*i == *j) {
			u.data.push_back(*i);
			i++;
			j++;
			continue;
		}
		if (*i < *j) {
			u.data.push_back(*i);
			i++;
			continue;
		}
		// otherwise *i > *j:
		u.data.push_back(*j);
		j++;
	}
	if (i == data.end()) {
		// this->data is exhausted. only other.data elements left. add them.
		u.data.insert(u.data.end(), j, other.data.end());
	}
	else {
		// other.data is exhausted. only this->data elements left. add them
		u.data.insert(u.data.end(), i, data.end());
	}
	return u;
}

Set Set::Intersection(const Set& other) const {
	Set cap = Set();
	auto i = data.begin();
	auto j = other.data.begin();
	while (i != data.end() && j != other.data.end()) {
		if (*i == *j) {
			// same element found. add it to the intersection
			cap.data.push_back(*i);
			i++;
			j++;
			continue;
		}
		if (*i > *j) {
			// continue moving j
			auto lb = std::lower_bound(j + 1, other.data.end(), *i);
			if (lb == other.data.end()) {
				// *i is > than every element of other.data[j:]
				return cap;
			}
			j = lb;
		}
		else {
			// otherwise *i < *j
			// continue moving i
			auto lb = std::lower_bound(i + 1, data.end(), *j);
			if (lb == data.end()) {
				// *j is > than every element of data[i:]
				return cap;
			}
			i = lb;
		}
	}
	return cap;
}

Set Set::Minus(const Set& other) const {
	Set r = Set();
	auto i = data.begin();
	auto j = other.data.begin();
	while (i != data.end() && j != other.data.end()) {
		if (*i == *j) {
			// same element found. remove it. everything ok.
			i++;
			j++;
			continue;
		}
		if (*i > *j) {
			// continue moving j
			auto lb = std::lower_bound(j + 1, other.data.end(), *i);
			j = lb;
		}
		else {
			// otherwise *i < *j
			// continue moving i adding all elements
			auto lb = std::lower_bound(i + 1, data.end(), *j);
			r.data.insert(r.data.end(), i, lb);
			i = lb;
		}
	}
	r.data.insert(r.data.end(), i, data.end());
	return r;
}

bool Set::IsSubsetOf(const Set& other) const {
	auto i = data.begin();
	auto j = other.data.begin();
	while (i != data.end() && j != other.data.end()) {
		if (*i == *j) {
			// same element found. add it to the intersection. everything ok.
			i++;
			j++;
			continue;
		}
		if (*i > *j) {
			// continue moving j
			auto lb = std::lower_bound(j + 1, other.data.end(), *i);
			j = lb;
		}
		else {
			// otherwise *i < *j
			return false;
		}
	}
	if (i == data.end() && j == other.data.end()) {
		// OK
		return true;
	}
	if (j == other.data.end()) {
		// superset exhausted while subset is not.
		return false;
	}
	// subset exhausted while superset is not
	return true;
}

bool Set::IsDisjointWith(const Set& other) const {
	auto i = data.begin();
	auto j = other.data.begin();
	while (i != data.end() && j != other.data.end()) {
		if (*i == *j) {
			// same element found. add it to the intersection
			return false;
		}
		if (*i > *j) {
			// continue moving j
			auto lb = std::lower_bound(j + 1, other.data.end(), *i);
			j = lb;
		}
		else {
			// otherwise *i < *j
			// continue moving i
			auto lb = std::lower_bound(i + 1, data.end(), *j);
			i = lb;
		}
	}
	return true;
}

std::ostream& operator<<(std::ostream& os, const Set& s)
{
	os << "{ ";
	bool first = true;
	for (int i : s.data) {
		if (!first) {
			os << ", ";
		}
		else {
			first = false;
		}
		os << i;
	}
	os << " }";
	return os;
}
