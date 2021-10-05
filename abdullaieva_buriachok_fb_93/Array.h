#pragma once

using namespace std;

template <typename T>
class Array
{
private:
	T* parray;
	int array_size;

public:
	Array();

	Array(const int array_size);

	Array(const Array& array);

	void operator=(const Array& array);

	~Array();

	int size() const;

	T& operator[](const int position) const;

	Array operator+(const Array& array) const;

	Array operator*(const Array<int>& array) const;

	void sort();
};







template<typename T>
inline Array<T>::Array()
{
	this->parray = nullptr;
	this->array_size = 0;
}

template<typename T>
inline Array<T>::Array(const int array_size)
{
	this->array_size = array_size;
	this->parray = new T[this->array_size];
}

template<typename T>
inline Array<T>::Array(const Array& array)
{
	this->array_size = array.array_size;
	this->parray = new T[this->array_size];

	for (int i = 0; i < this->array_size; i++)
	{
		this->parray[i] = array.parray[i];
	}
}

template<typename T>
inline void Array<T>::operator=(const Array& array)
{
	if (this->parray != nullptr)
	{
		this->~Array();
	}
	
	this->array_size = array.array_size;
	this->parray = new T[this->array_size];

	for (int i = 0; i < this->array_size; i++)
	{
		this->parray[i] = array.parray[i];
	}
}

template<typename T>
inline Array<T>::~Array()
{
	delete[] parray;
}

template<typename T>
inline int Array<T>::size() const
{
	return this->array_size;
}

template<typename T>
inline T& Array<T>::operator[](const int position) const
{
	if (position >= 0 && position < this->array_size)
	{
		return this->parray[position];
	}
}

template<typename T>
inline Array<T> Array<T>::operator+(const Array& array) const
{
	Array result(this->array_size + array.array_size);

	for (int i = 0; i < this->array_size; i++)
	{
		result.parray[i] = this->parray[i];
	}

	for (int i = 0; i < array.array_size; i++)
	{
		result.parray[this->array_size + i] = array.parray[i];
	}
	
	return result;
}

template<typename T>
inline Array<T> Array<T>::operator*(const Array<int>& array) const
{
	int size = array.size();
	
	Array result(size);

	for (int i = 0; i < size; i++)
	{
		result.parray[i] = this->parray[array[i]];
	}

	return result;
}

template<typename T>
inline void Array<T>::sort()
{
	int distance = this->array_size / 2;

	while (distance > 0)
	{
		for (int i = 0; i < this->array_size; i += distance)
		{
			int key = this->parray[i];

			int j = i - distance;

			while (j >= 0 && this->parray[j] > key)
			{
				this->parray[j + distance] = this->parray[j];

				j -= distance;
			}

			this->parray[j + distance] = key;
		}

		distance /= 2;
	}
}