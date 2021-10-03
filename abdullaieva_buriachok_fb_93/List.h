#pragma once
#include "Array.h"

using namespace std;

template <typename T>
class List_Node
{
private:
	T value;
	List_Node* pnext;

	template <typename T> friend class List;

public:
	List_Node(const T& value, List_Node* pnext);
};





template <typename T>
class List
{
private:
	List_Node<T>* head;
	int list_size;

public:
	List();

	List(const List& list);

	void operator=(const List& list);

	~List();

	int size() const;

	void push_back(const T& value);

	void erase(const int position);

	T& operator[](const int position) const;

	Array<T> to_array() const;
};







template<typename T>
inline List_Node<T>::List_Node(const T& value, List_Node* pnext)
{
	this->value = value;
	this->pnext = pnext;
}





template<typename T>
inline List<T>::List()
{
	this->head = nullptr;
	this->list_size = 0;
}

template<typename T>
inline List<T>::List(const List& list)
{
	this->head = nullptr;
	this->list_size = 0;

	List_Node<T>* current = list.head;

	while (current != nullptr)
	{
		this->push_back(current->value);

		current = current->pnext;
	}
}

template<typename T>
inline void List<T>::operator=(const List& list)
{
	if (this->head != nullptr)
	{
		this->~List();
	}

	List_Node<T>* current = list.head;

	while (current != nullptr)
	{
		this->push_back(current->value);

		current = current->pnext;
	}
}

template<typename T>
inline List<T>::~List()
{
	while (this->head != nullptr)
	{
		List_Node<T>* to_delete = this->head;

		this->head = this->head->pnext;

		delete to_delete;

		this->list_size--;
	}
}

template<typename T>
inline int List<T>::size() const
{
	return this->list_size;
}

template<typename T>
inline void List<T>::push_back(const T& value)
{
	if (this->head == nullptr)
	{
		this->head = new List_Node<T>(value, nullptr);
	}

	else
	{
		List_Node<T>* last = this->head;

		while (last->pnext != nullptr)
		{
			last = last->pnext;
		}

		last->pnext = new List_Node<T>(value, nullptr);
	}

	this->list_size++;
}

template<typename T>
inline void List<T>::erase(const int position)
{
	if (position == 0)
	{
		List_Node<T>* to_delete = this->head;

		this->head = this->head->pnext;

		delete to_delete;

		this->list_size--;
	}

	else if (position > 0 && position < this->list_size)
	{
		List_Node<T>* previous = this->head;

		for (int i = 0; i < position - 1; i++)
		{
			previous = previous->pnext;
		}

		List_Node<T>* to_delete = previous->pnext;

		previous->pnext = to_delete->pnext;

		delete to_delete;

		this->list_size--;
	}
}

template<typename T>
inline T& List<T>::operator[](const int position) const
{
	if (position >= 0 && position < this->list_size)
	{
		List_Node<T>* current = this->head;

		for (int i = 0; i < position; i++)
		{
			current = current->pnext;
		}

		return current->value;
	}
}

template<typename T>
inline Array<T> List<T>::to_array() const
{
	Array<T> result(this->list_size);

	int counter = 0;

	List_Node<T>* current = this->head;

	while (current != nullptr)
	{
		result[counter] = current->value;

		counter++;
		current = current->pnext;
	}

	return result;
}