#pragma once
#include <iostream>
#include "List.h"

using namespace std;

template <typename T, typename U>
class Tree_Node
{
private:
	T key;
	U value;
	Tree_Node* pleft, * pright, * pparent;

	template <typename T, typename U> friend class Tree;

	void inorder_print();//ARB

	void inorder_asc(List<U>& values, const T& value, const bool is_equal);//ARB

	void inorder_desc(List<U>& values, const T& value, const bool is_equal);//BRA

	void preorder_travel(List<pair<T, U>>& values);//RAB

	Tree_Node* minimum();

	Tree_Node* maximum();

	Tree_Node* find(const T& key);

	void insert(T& key, U& value);

	void decrement(const U& value);

	U erase(const T& key);

public:
	Tree_Node(T& ket, U& value, Tree_Node* pparent);

	~Tree_Node();
};





template <typename T, typename U>
class Tree
{
private:
	Tree_Node<T, U>* root;

public:
	Tree();

	Tree(const Tree& tree);

	void operator=(const Tree& tree);

	~Tree();

	void inorder_print() const;

	List<U> inorder_asc(const T& key, const bool is_equal) const;

	List<U> inorder_desc(const T& key, const bool is_equal) const;

	bool check(const T& key) const;

	U find(const T& key) const;

	void insert(T& key, U& value);

	void erase(const T& key);
};







template<typename T, typename U>
inline Tree_Node<T, U>::Tree_Node(T& key, U& value, Tree_Node* pparent)
{
	this->key = key;
	this->value = value;
	this->pleft = this->pright = nullptr;
	this->pparent = pparent;
}

template<typename T, typename U>
inline Tree_Node<T, U>::~Tree_Node()
{
	delete this->pleft;
	delete this->pright;
}

template<typename T, typename U>
inline void Tree_Node<T, U>::inorder_print()
{
	if (this != nullptr)
	{
		this->pleft->inorder_print();
		cout << this->value << endl;
		this->pright->inorder_print();
	}
}

template<typename T, typename U>
inline void Tree_Node<T, U>::inorder_asc(List<U>& values, const T& key, const bool is_equal)
{
	if (this != nullptr)
	{
		this->pleft->inorder_asc(values, key, is_equal);

		if (!is_equal && this->key < key)
		{
			values.push_back(this->value);
		}

		if (is_equal && this->key <= key)
		{
			values.push_back(this->value);
		}

		if (this->key < key)
		{
			this->pright->inorder_asc(values, key, is_equal);
		}
	}
}

template<typename T, typename U>
inline void Tree_Node<T, U>::inorder_desc(List<U>& values, const T& key, const bool is_equal)
{
	if (this != nullptr)
	{
		this->pright->inorder_desc(values, key, is_equal);

		if (!is_equal && this->key > key)
		{
			values.push_back(this->value);
		}

		if (is_equal && this->key >= key)
		{
			values.push_back(this->value);
		}

		if (this->key > key)
		{
			this->pleft->inorder_desc(values, key, is_equal);
		}
	}
}

template<typename T, typename U>
inline void Tree_Node<T, U>::preorder_travel(List<pair<T, U>>& values)
{
	if (this != nullptr)
	{
		values.push_back(make_pair(this->key, this->value));
		this->pleft->preorder_travel(values);
		this->pright->preorder_travel(values);
	}
}

template<typename T, typename U>
inline Tree_Node<T, U>* Tree_Node<T, U>::minimum()
{
	Tree_Node* current = this;

	while (current != nullptr && current->pleft != nullptr)
	{
		current = current->pleft;
	}

	return current;
}

template<typename T, typename U>
inline Tree_Node<T, U>* Tree_Node<T, U>::maximum()
{
	Tree_Node* current = this;

	while (current != nullptr && current->pright != nullptr)
	{
		current = current->pright;
	}

	return current;
}

template<typename T, typename U>
inline Tree_Node<T, U>* Tree_Node<T, U>::find(const T& key)
{
	Tree_Node* current = this;

	while (current != nullptr && current->key != key)
	{
		if (key < current->key)
		{
			current = current->pleft;
		}

		else
		{
			current = current->pright;
		}
	}

	return current;
}

template<typename T, typename U>
inline void Tree_Node<T, U>::insert(T& key, U& value)
{
	if (this != nullptr)
	{
		Tree_Node* current = this, * parent = this->pparent;

		while (current != nullptr)
		{
			parent = current;

			if (key < current->key)
			{
				current = current->pleft;
			}

			else
			{
				current = current->pright;
			}
		}

		Tree_Node* new_node = new Tree_Node(key, value, parent);

		if (key < parent->key)
		{
			parent->pleft = new_node;
		}

		else
		{
			parent->pright = new_node;
		}
	}
}

template<typename T, typename U>
inline void Tree_Node<T, U>::decrement(const U& value)
{
	if (this != nullptr)
	{
		this->pleft->decrement(value);
		this->value--;
		this->pright->decrement(value);
	}
}

template<typename T, typename U>
inline U Tree_Node<T, U>::erase(const T& key)
{
	Tree_Node* to_delete = this->find(key);

	if (to_delete != nullptr)
	{
		U deleted_value = to_delete->value;

		Tree_Node* parent = to_delete->pparent;

		if (to_delete->pleft == nullptr && to_delete->pright == nullptr)
		{
			if (parent != nullptr)
			{
				if (parent->pleft == to_delete)
				{
					parent->pleft = nullptr;
				}

				else
				{
					parent->pright = nullptr;
				}
			}

			delete to_delete;
		}

		else if (to_delete->pleft == nullptr || to_delete->pright == nullptr)
		{
			if (to_delete->pleft == nullptr)
			{
				if (parent != nullptr)
				{
					if (parent->pleft == to_delete)
					{
						parent->pleft = to_delete->pright;
					}

					else
					{
						parent->pright = to_delete->pright;
					}
				}

				to_delete->pright->pparent = parent;
				to_delete->pright = nullptr;
			}

			else
			{
				if (parent != nullptr)
				{
					if (parent->pleft == to_delete)
					{
						parent->pleft = to_delete->pleft;
					}

					else
					{
						parent->pright = to_delete->pleft;
					}
				}

				to_delete->pleft->pparent = parent;
				to_delete->pleft = nullptr;
			}

			delete to_delete;
		}

		else
		{
			Tree_Node* next = to_delete->pright->minimum();

			to_delete->key = next->key;
			to_delete->value = next->value;

			if (next->pparent->pleft == next)
			{
				next->pparent->pleft = next->pright;

				if (next->pright != nullptr)
				{
					next->pright->pparent = next->pparent;
				}
			}

			else
			{
				next->pparent->pright = next->pright;

				if (next->pright != nullptr)
				{
					next->pright->pparent = next->pparent;
				}
			}

			delete next;
		}

		return deleted_value;
	}
}





template<typename T, typename U>
inline Tree<T, U>::Tree()
{
	this->root = nullptr;
}

template<typename T, typename U>
inline Tree<T, U>::Tree(const Tree& tree)
{
	this->root = nullptr;
	
	List<pair<T, U>> values;

	tree.root->preorder_travel(values);

	for (int i = 0; i < values.size(); i++)
	{
		this->insert(values[i].first, values[i].second);
	}
}

template<typename T, typename U>
inline void Tree<T, U>::operator=(const Tree& tree)
{
	if (this->root != nullptr)
	{
		this->~Tree();
	}

	List<pair<T, U>> values;

	tree.root->preorder_travel(values);

	for (int i = 0; i < values.size(); i++)
	{
		this->insert(values[i].first, values[i].second);
	}
}

template<typename T, typename U>
inline Tree<T, U>::~Tree()
{
	delete this->root;
}

template<typename T, typename U>
inline void Tree<T, U>::inorder_print() const
{
	this->root->inorder_print();
}

template<typename T, typename U>
inline List<U> Tree<T, U>::inorder_asc(const T& key, const bool is_equal) const
{
	List<U> result;

	this->root->inorder_asc(result, key, is_equal);

	return result;
}

template<typename T, typename U>
inline List<U> Tree<T, U>::inorder_desc(const T& key, const bool is_equal) const
{
	List<U> result;

	this->root->inorder_desc(result, key, is_equal);

	return result;
}

template<typename T, typename U>
inline bool Tree<T, U>::check(const T& key) const
{
	return this->root->find(key) == nullptr ? false : true;
}

template<typename T, typename U>
inline U Tree<T, U>::find(const T& key) const
{
	Tree_Node<T, U>* result = this->root->find(key);
	
	if (result != nullptr)
	{
		return result->value;
	}

	else
	{
		return U();
	}
}

template<typename T, typename U>
inline void Tree<T, U>::insert(T& key, U& value)
{
	if (this->root == nullptr)
	{
		this->root = new Tree_Node<T, U>(key, value, nullptr);
	}

	else if (this->root->find(key) == nullptr)
	{
		this->root->insert(key, value);
	}
}

template<typename T, typename U>
inline void Tree<T, U>::erase(const T& key)
{
	Tree_Node<T, U>* new_root = this->root;
	
	if (this->root->key == key)//удаляем корень
	{
		if (this->root->pleft == nullptr && this->root->pright == nullptr)//нет дочерних
		{
			new_root = nullptr;
		}

		else if (this->root->pleft == nullptr || this->root->pright == nullptr)//один дочерний
		{
			new_root = this->root->pleft == nullptr ? this->root->pright : this->root->pleft;
		}
	}
	
	U value = this->root->erase(key);

	this->root = new_root;
	
	this->root->decrement(value);
}