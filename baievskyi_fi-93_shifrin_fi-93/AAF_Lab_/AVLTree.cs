using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace AAF_Lab_
{
    internal class AVLTree<T> : DATABASE, IEnumerable<T> where T : IComparable
    {
        // Свойство для корня дерева
        public List<string> str = new List<string>();
        public AVLTreeNode<T> Head
        {
            get;
            internal set;
        }

        #region Метод Clear

        public void Clear()
        {
            Head = null; // удаление дерева
            Count = 0;
        }

        #endregion

        #region Метод Remove

        public bool Remove(T value)
        {
            AVLTreeNode<T> current;
            current = Find(value); // поиск удаляемого узла по значению

            if (current == null) // узел не найден
            {
                return false;
            }

            AVLTreeNode<T> treeToBalance = current.Parent; // проверка баланса дарева
            Count--;                                       // уменьшение колиества узлов

            // Вариант 1: Если удаляемый узел не имеет правого потомка

            if (current.Right == null) // если нет правого потомка
            {
                if (current.Parent == null) // удалямый узел является корнем
                {
                    Head = current.Left;    // на место корня перемещаем левого потомка

                    if (Head != null)
                    {
                        Head.Parent = null; // для нового корня удаляем ссылку на родителя  
                    }
                }
                else // удаляемый узел не является корнем
                {
                    int result = current.Parent.CompareTo(current.Value);

                    if (result > 0)
                    {
                        // Если значение родительского узла больше удаляемого, 
                        // сделать левого потомка текущего элемента, левым потомком родителя.  

                        current.Parent.Left = current.Left;
                    }
                    else if (result < 0)
                    {

                        // Если родительский узел меньше чем удаляемый,                 
                        // сделать левого потомка удаляемого узла - правым потомком родителя.                 

                        current.Parent.Right = current.Left;
                    }
                }
            }

            // Вариант 2: Если правый потомок удаляемого узла, не имеет левого потомка. 

            else if (current.Right.Left == null) // если у правого потомка нет левого потомка
            {
                current.Right.Left = current.Left;

                if (current.Parent == null) // текущий элемент является корнет
                {
                    Head = current.Right;

                    if (Head != null)
                    {
                        Head.Parent = null;
                    }
                }
                else
                {
                    int result = current.Parent.CompareTo(current.Value);
                    if (result > 0)
                    {

                        // Если значение родительского узла больше удаляемого, 
                        // сделать левого потомка текущего элемента, левым потомком родителя.  

                        current.Parent.Left = current.Right;
                    }

                    else if (result < 0)
                    {

                        // Если родительский узел меньше чем удаляемый,                 
                        // сделать левого потомка удаляемого узла - правым потомком родителя.                 

                        current.Parent.Right = current.Right;
                    }
                }
            }

            // Вариант 3: Если правый потомок удаляемого узла имеет левого потомка, 
            // то требуется поместить на место удаляемого узла, крайним левый потомок его правого потомка.     

            else
            {
                // Нахождение крайнего левого узла для правого потомка текущего элемента.       

                AVLTreeNode<T> leftmost = current.Right.Left;

                while (leftmost.Left != null)
                {
                    leftmost = leftmost.Left;
                }

                // Родительское левое поддерево становится родительским крайним правым поддеревом.         
                leftmost.Parent.Left = leftmost.Right;

                // Присвоить крайний левый и крайний правый потомок удаляемого узла, его правому и левому потомку соответственно.         

                leftmost.Left = current.Left;
                leftmost.Right = current.Right;

                if (current.Parent == null)
                {
                    Head = leftmost;

                    if (Head != null)
                    {
                        Head.Parent = null;
                    }
                }
                else
                {
                    int result = current.Parent.CompareTo(current.Value);

                    if (result > 0)
                    {

                        // Если значение родительского узла больше удаляемого, 
                        // сделать левого потомка текущего элемента, левым потомком родителя.  

                        current.Parent.Left = leftmost;
                    }
                    else if (result < 0)
                    {

                        // Если родительский узел меньше чем удаляемый,                 
                        // сделать левого потомка удаляемого узла - правым потомком родителя.                 

                        current.Parent.Right = leftmost;
                    }
                }
            }

            if (treeToBalance != null)
            {
                // treeToBalance.Balance();
            }

            else
            {
                if (Head != null)
                {
                    // Head.Balance();
                }
            }

            return true;

        }

        #endregion

        #region Метод Contains

        public bool Contains(T value)
        {
            return Find(value) != null;
        }

        /// <summary> 
        /// Находит и возвращает первый узел который содержит искомое значение.
        /// Если значение не найдено, возвращает null. 
        /// Так же возвращает родительский узел.
        /// </summary> /// 
        /// <param name="value">Значение поиска</param> 
        /// <param name="parent">Родительский элемент для найденного значения/// </param> 
        /// <returns> Найденный узел (или ноль) /// </returns> 

        private AVLTreeNode<T> Find(T value)
        {

            AVLTreeNode<T> current = Head; // помещаем текущий элемент в корень дерева

            // Пока текщий узел на пустой 
            while (current != null)
            {
                int result = current.CompareTo(value); // сравнение значения текущего элемента с искомым значением

                if (result > 0)
                {
                    // Если значение меньшне текущего - переход влево 
                    current = current.Left;
                }
                else if (result < 0)
                {
                    // Если значение больше текщего - переход вправо             
                    current = current.Right;
                }
                else
                {
                    // Элемент найден      
                    break;
                }
            }
            return current;
        }


        #endregion

        #region Количество узлов дерева
        public int Count
        {
            get;
            private set;
        }
        #endregion

        #region Метод Add

        // Метод добавлет новый узел

        public void Add(T value, string[] arr, string _index)
        {
            // Вариант 1:  Дерево пустое - создание корня дерева      
            if (Head == null)
            {
                Head = new AVLTreeNode<T>(value, null, this, arr, _index);
            }

            // Вариант 2: Дерево не пустое - найти место для добавление нового узла.

            else
            {
                AddTo(Head, value, arr, _index);
            }

            Count++;
        }

        // Алгоритм рекурсивного добавления нового узла в дерево.

        private void AddTo(AVLTreeNode<T> node, T value, string[] arr, string _index)
        {
            // Вариант 1: Добавление нового значения в дерево. Значение добавлемого узла меньше чем значение текущего узла.      

            if (value.CompareTo(node.Value) < 0)
            {
                //Создание левого узла, если его нет.

                if (node.Left == null)
                {
                    node.Left = new AVLTreeNode<T>(value, node, this, arr, _index);
                }

                else
                {
                    // Переходим к следующему левому узлу
                    AddTo(node.Left, value, arr, _index);
                }
            }
            // Вариант 2: Добавлемое значение больше или равно текущему значению.

            else
            {
                //Создание правого узла, если его нет.         
                if (node.Right == null)
                {
                    node.Right = new AVLTreeNode<T>(value, node, this, arr, _index);
                }
                else
                {
                    // Переход к следующему правому узлу.             
                    AddTo(node.Right, value, arr, _index);
                }
            }
            //node.Balance();
        }

        #endregion

        #region Итераторы

        public IEnumerator<T> InOrderTraversal()
        {

            // рекурсивное перемищение по дереву

            if (Head != null) // существует ли корень дерева
            {

                Stack<AVLTreeNode<T>> stack = new Stack<AVLTreeNode<T>>();
                AVLTreeNode<T> current = Head;

                // при рекурсивном перемещении по дереву, нужно указывать какой потомок будет слудеющим (правый или левый)

                bool goLeftNext = true;

                // Начинаем с помещения корня в стек
                stack.Push(current);

                while (stack.Count > 0)
                {
                    // Если перемещаемся влево ... 
                    if (goLeftNext)
                    {
                        // Перемещение всех левых потомков в стек.

                        while (current.Left != null)
                        {
                            stack.Push(current);
                            current = current.Left;
                        }
                    }

                    yield return current.Value;

                    // Если перемещаемся вправо 

                    if (current.Right != null)
                    {
                        current = current.Right;

                        // Идинажды перемещаемся вправо, после чего опять идем влево. 

                        goLeftNext = true;
                    }
                    else
                    {
                        // Если перейти вправо нельзя - извлекаем родительский узел. 

                        current = stack.Pop();
                        goLeftNext = false;
                    }
                }
            }
        }

        public IEnumerator<T> GetEnumerator()
        {
            return InOrderTraversal();
        }

        System.Collections.IEnumerator System.Collections.IEnumerable.GetEnumerator()
        {

            return GetEnumerator();

        }

        #endregion

        public void INorder(AVLTreeNode<T> node, List<int> _spaces, Dictionary<string, string[]> _dictionary)
        {
            if (node == null)
                return;

            if (node.Left != null) INorder(node.Left, _spaces, _dictionary);

            if (_dictionary["0"][0] != _dictionary.First().Value[0])
            {
                for (int q = 0; q < _dictionary[node._index.ToString()].Length; q++)
                {
                    if (q == _dictionary[node._index.ToString()].Length - 1)
                    {
                        Console.Write("| {0}{1} | \n", String.Concat(Enumerable.Repeat(" ", _spaces[q] - _dictionary[node._index.ToString()][q].Length)), _dictionary[node._index.ToString()][q]);
                    }
                    else
                    {
                        Console.Write("| {0}{1} | ", String.Concat(Enumerable.Repeat(" ", _spaces[q] - _dictionary[node._index.ToString()][q].Length)), _dictionary[node._index.ToString()][q]);
                    }
                }

            }

            if (node.Right != null) INorder(node.Right, _spaces, _dictionary);

        }

        public void INorderCL(AVLTreeNode<T> node, List<int> lims, List<string[]> conditions, List<int> _spaces, Dictionary<string, string[]> _dictionary)
        {
            if (node == null)
                return;

            if (node.Left != null) INorderCL(node.Left, lims, conditions, _spaces, _dictionary);

            if ((node.Parent != null))
            {
                int counter = 0;

                for (int w = 0; w < conditions.Count; w++)
                {
                    if (conditions[w][0].Contains("---"))
                    {
                        if (conditions[w][1] == "=")
                        {
                            if (_dictionary[node._index][conditions[w][0].Replace("---", "").Split(" ")[0].ToCharArray()[0] - '0'] == conditions[w].Last())
                            {
                                counter++;
                            }
                        }

                        if (conditions[w][1] == "!=")
                        {
                            if (_dictionary[node._index][conditions[w][0].Replace("---", "").Split(" ")[0].ToCharArray()[0] - '0'] != conditions[w].Last())
                            {
                                counter++;
                            }
                        }

                        if (conditions[w][1] == ">")
                        {
                            if (conditions[w].Last().CompareTo(_dictionary[node._index][conditions[w][0].Replace("---", "").Split(" ")[0].ToCharArray()[0] - '0']) > 0)
                            {
                                counter++;
                            }
                        }

                        if (conditions[w][1] == "<")
                        {
                            if (conditions[w].Last().CompareTo(_dictionary[node._index][conditions[w][0].Replace("---", "").Split(" ")[0].ToCharArray()[0] - '0']) < 0)
                            {
                                counter++;
                            }
                        }

                        if (conditions[w][1] == ">=")
                        {
                            if (conditions[w].Last().CompareTo(_dictionary[node._index][conditions[w][0].Replace("---", "").Split(" ")[0].ToCharArray()[0] - '0']) >= 0)
                            {
                                counter++;
                            }
                        }

                        if (conditions[w][1] == "<=")
                        {
                            if (conditions[w].Last().CompareTo(_dictionary[node._index][conditions[w][0].Replace("---", "").Split(" ")[0].ToCharArray()[0] - '0']) <= 0)
                            {
                                counter++;
                            }
                        }
                    }
                    else if (conditions[w][0].Contains("--"))
                    {
                        if (conditions[w][1] == "=")
                        {
                            if (_dictionary[node._index][conditions[w][0].Replace("--", "").Split(" ")[0].ToCharArray()[0] - '0'] == conditions[w].Last())
                            {
                                counter++;
                            }
                        }

                        if (conditions[w][1] == "!=")
                        {
                            if (_dictionary[node._index][conditions[w][0].Replace("--", "").Split(" ")[0].ToCharArray()[0] - '0'] != conditions[w].Last())
                            {
                                counter++;
                            }
                        }

                        if (conditions[w][1] == ">")
                        {
                            if (_dictionary[node._index][conditions[w][0].Replace("--", "").Split(" ")[0].ToCharArray()[0] - '0'].CompareTo(conditions[w].Last()) > 0)
                            {
                                counter++;
                            }
                        }

                        if (conditions[w][1] == "<")
                        {
                            if (_dictionary[node._index][conditions[w][0].Replace("--", "").Split(" ")[0].ToCharArray()[0] - '0'].CompareTo(conditions[w].Last()) < 0)
                            {
                                counter++;
                            }
                        }

                        if (conditions[w][1] == ">=")
                        {
                            if (_dictionary[node._index][conditions[w][0].Replace("--", "").Split(" ")[0].ToCharArray()[0] - '0'].CompareTo(conditions[w].Last()) >= 0)
                            {
                                counter++;
                            }
                        }

                        if (conditions[w][1] == "<=")
                        {
                            if (_dictionary[node._index][conditions[w][0].Replace("--", "").Split(" ")[0].ToCharArray()[0] - '0'].CompareTo(conditions[w].Last()) <= 0)
                            {
                                counter++;
                            }
                        }
                    }
                    else if (conditions[w][0].IndexOf("-") == 0)
                    {
                        if (conditions[w][1] == "=")
                        {
                            if (_dictionary[node._index][conditions[w][0].Replace("-", "").Split(" ")[0].ToCharArray()[0] - '0'] == _dictionary[node._index][conditions[w].Last().ToCharArray()[0] - '0'])
                            {
                                counter++;
                            }
                        }

                        if (conditions[w][1] == "!=")
                        {
                            if (_dictionary[node._index][conditions[w][0].Replace("-", "").Split(" ")[0].ToCharArray()[0] - '0'] != _dictionary[node._index][conditions[w].Last().ToCharArray()[0] - '0'])
                            {
                                counter++;
                            }
                        }

                        if (conditions[w][1] == ">")
                        {
                            if (_dictionary[node._index][conditions[w][0].Replace("-", "").Split(" ")[0].ToCharArray()[0] - '0'].CompareTo(_dictionary[node._index][conditions[w].Last().ToCharArray()[0] - '0']) > 0)
                            {
                                counter++;
                            }
                        }

                        if (conditions[w][1] == "<")
                        {
                            if (_dictionary[node._index][conditions[w][0].Replace("-", "").Split(" ")[0].ToCharArray()[0] - '0'].CompareTo(_dictionary[node._index][conditions[w].Last().ToCharArray()[0] - '0']) < 0)
                            {
                                counter++;
                            }
                        }

                        if (conditions[w][1] == ">=")
                        {
                            if (_dictionary[node._index][conditions[w][0].Replace("-", "").Split(" ")[0].ToCharArray()[0] - '0'].CompareTo(_dictionary[node._index][conditions[w].Last().ToCharArray()[0] - '0']) >= 0)
                            {
                                counter++;
                            }
                        }

                        if (conditions[w][1] == "<=")
                        {
                            if (_dictionary[node._index][conditions[w][0].Replace("-", "").Split(" ")[0].ToCharArray()[0] - '0'].CompareTo(_dictionary[node._index][conditions[w].Last().ToCharArray()[0] - '0']) <= 0)
                            {
                                counter++;
                            }
                        }
                    }

                }

                if (counter == conditions.Count)
                {
                    for (int q = 0; q < lims.Count; q++)
                    {
                        if (q == (lims.Count - 1))
                        {
                            Console.Write("| {0}{1} | \n", String.Concat(Enumerable.Repeat(" ", _spaces[lims[q]] - _dictionary[node._index][lims[q]].Length)), _dictionary[node._index][lims[q]]);
                        }
                        else
                        {
                            Console.Write("| {0}{1} | ", String.Concat(Enumerable.Repeat(" ", _spaces[lims[q]] - _dictionary[node._index][lims[q]].Length)), _dictionary[node._index][lims[q]]);
                        }
                    }
                }
            }

            if (node.Right != null) INorderCL(node.Right, lims, conditions, _spaces, _dictionary);
        }

        public void POSTorderCL(AVLTreeNode<T> node, List<int> lims, List<string[]> conditions, List<int> _spaces, Dictionary<string, string[]> _dictionary)
        {
            if (node == null)
                return;

            if (node.Right != null) POSTorderCL(node.Right, lims, conditions, _spaces, _dictionary);

            if (node.Parent != null)
            {
                int counter = 0;

                for (int w = 0; w < conditions.Count; w++)
                {
                    if (conditions[w][0].Contains("---"))
                    {
                        if (conditions[w][1] == "=")
                        {
                            if (_dictionary[node._index][conditions[w][0].Replace("---", "").Split(" ")[0].ToCharArray()[0] - '0'] == conditions[w].Last())
                            {
                                counter++;
                            }
                        }

                        if (conditions[w][1] == "!=")
                        {
                            if (_dictionary[node._index][conditions[w][0].Replace("---", "").Split(" ")[0].ToCharArray()[0] - '0'] != conditions[w].Last())
                            {
                                counter++;
                            }
                        }

                        if (conditions[w][1] == ">")
                        {
                            if (conditions[w].Last().CompareTo(_dictionary[node._index][conditions[w][0].Replace("---", "").Split(" ")[0].ToCharArray()[0] - '0']) > 0)
                            {
                                counter++;
                            }
                        }

                        if (conditions[w][1] == "<")
                        {
                            if (conditions[w].Last().CompareTo(_dictionary[node._index][conditions[w][0].Replace("---", "").Split(" ")[0].ToCharArray()[0] - '0']) < 0)
                            {
                                counter++;
                            }
                        }

                        if (conditions[w][1] == ">=")
                        {
                            if (conditions[w].Last().CompareTo(_dictionary[node._index][conditions[w][0].Replace("---", "").Split(" ")[0].ToCharArray()[0] - '0']) >= 0)
                            {
                                counter++;
                            }
                        }

                        if (conditions[w][1] == "<=")
                        {
                            if (conditions[w].Last().CompareTo(_dictionary[node._index][conditions[w][0].Replace("---", "").Split(" ")[0].ToCharArray()[0] - '0']) <= 0)
                            {
                                counter++;
                            }
                        }
                    }
                    else if (conditions[w][0].Contains("--"))
                    {
                        if (conditions[w][1] == "=")
                        {
                            if (_dictionary[node._index][conditions[w][0].Replace("--", "").Split(" ")[0].ToCharArray()[0] - '0'] == conditions[w].Last())
                            {
                                counter++;
                            }
                        }

                        if (conditions[w][1] == "!=")
                        {
                            if (_dictionary[node._index][conditions[w][0].Replace("--", "").Split(" ")[0].ToCharArray()[0] - '0'] != conditions[w].Last())
                            {
                                counter++;
                            }
                        }

                        if (conditions[w][1] == ">")
                        {
                            if (_dictionary[node._index][conditions[w][0].Replace("--", "").Split(" ")[0].ToCharArray()[0] - '0'].CompareTo(conditions[w].Last()) > 0)
                            {
                                counter++;
                            }
                        }

                        if (conditions[w][1] == "<")
                        {
                            if (_dictionary[node._index][conditions[w][0].Replace("--", "").Split(" ")[0].ToCharArray()[0] - '0'].CompareTo(conditions[w].Last()) < 0)
                            {
                                counter++;
                            }
                        }

                        if (conditions[w][1] == ">=")
                        {
                            if (_dictionary[node._index][conditions[w][0].Replace("--", "").Split(" ")[0].ToCharArray()[0] - '0'].CompareTo(conditions[w].Last()) >= 0)
                            {
                                counter++;
                            }
                        }

                        if (conditions[w][1] == "<=")
                        {
                            if (_dictionary[node._index][conditions[w][0].Replace("--", "").Split(" ")[0].ToCharArray()[0] - '0'].CompareTo(conditions[w].Last()) <= 0)
                            {
                                counter++;
                            }
                        }
                    }
                    else if (conditions[w][0].IndexOf("-") == 0)
                    {
                        if (conditions[w][1] == "=")
                        {
                            if (_dictionary[node._index][conditions[w][0].Replace("-", "").Split(" ")[0].ToCharArray()[0] - '0'] == _dictionary[node._index][conditions[w].Last().ToCharArray()[0] - '0'])
                            {
                                counter++;
                            }
                        }

                        if (conditions[w][1] == "!=")
                        {
                            if (_dictionary[node._index][conditions[w][0].Replace("-", "").Split(" ")[0].ToCharArray()[0] - '0'] != _dictionary[node._index][conditions[w].Last().ToCharArray()[0] - '0'])
                            {
                                counter++;
                            }
                        }

                        if (conditions[w][1] == ">")
                        {
                            if (_dictionary[node._index][conditions[w][0].Replace("-", "").Split(" ")[0].ToCharArray()[0] - '0'].CompareTo(_dictionary[node._index][conditions[w].Last().ToCharArray()[0] - '0']) > 0)
                            {
                                counter++;
                            }
                        }

                        if (conditions[w][1] == "<")
                        {
                            if (_dictionary[node._index][conditions[w][0].Replace("-", "").Split(" ")[0].ToCharArray()[0] - '0'].CompareTo(_dictionary[node._index][conditions[w].Last().ToCharArray()[0] - '0']) < 0)
                            {
                                counter++;
                            }
                        }

                        if (conditions[w][1] == ">=")
                        {
                            if (_dictionary[node._index][conditions[w][0].Replace("-", "").Split(" ")[0].ToCharArray()[0] - '0'].CompareTo(_dictionary[node._index][conditions[w].Last().ToCharArray()[0] - '0']) >= 0)
                            {
                                counter++;
                            }
                        }

                        if (conditions[w][1] == "<=")
                        {
                            if (_dictionary[node._index][conditions[w][0].Replace("-", "").Split(" ")[0].ToCharArray()[0] - '0'].CompareTo(_dictionary[node._index][conditions[w].Last().ToCharArray()[0] - '0']) <= 0)
                            {
                                counter++;
                            }
                        }
                    }
                }

                if (counter == conditions.Count)
                {
                    for (int q = 0; q < lims.Count; q++)
                    {
                        if (q == lims.Count - 1)
                        {
                            Console.Write("| {0}{1} | \n", String.Concat(Enumerable.Repeat(" ", _spaces[lims[q]] - _dictionary[node._index][lims[q]].Length)), _dictionary[node._index][lims[q]]);
                        }
                        else
                        {
                            Console.Write("| {0}{1} | ", String.Concat(Enumerable.Repeat(" ", _spaces[lims[q]] - _dictionary[node._index][lims[q]].Length)), _dictionary[node._index][lims[q]]);
                        }
                    }
                }
            }

            if (node.Left != null) POSTorderCL(node.Left, lims, conditions, _spaces, _dictionary);

        }

        public void InorderDel(AVLTreeNode<T> node, List<string> For_Del, List<string[]> conditions, Dictionary<string, string[]> _dictionary)
        {
            if (node == null)
                return;

            if (node.Left != null) InorderDel(node.Left, For_Del, conditions, _dictionary);

            if ((node.Parent != null))
            {
                int counter = 0;

                for (int w = 0; w < conditions.Count; w++)
                {
                    if (conditions[w][0].Contains("---"))
                    {
                        if (conditions[w][1] == "=")
                        {
                            if (_dictionary[node._index][conditions[w][0].Replace("---", "").Split(" ")[0].ToCharArray()[0] - '0'] == conditions[w].Last())
                            {
                                counter++;
                            }
                        }

                        if (conditions[w][1] == "!=")
                        {
                            if (_dictionary[node._index][conditions[w][0].Replace("---", "").Split(" ")[0].ToCharArray()[0] - '0'] != conditions[w].Last())
                            {
                                counter++;
                            }
                        }

                        if (conditions[w][1] == ">")
                        {
                            if (conditions[w].Last().CompareTo(_dictionary[node._index][conditions[w][0].Replace("---", "").Split(" ")[0].ToCharArray()[0] - '0']) > 0)
                            {
                                counter++;
                            }
                        }

                        if (conditions[w][1] == "<")
                        {
                            if (conditions[w].Last().CompareTo(_dictionary[node._index][conditions[w][0].Replace("---", "").Split(" ")[0].ToCharArray()[0] - '0']) < 0)
                            {
                                counter++;
                            }
                        }

                        if (conditions[w][1] == ">=")
                        {
                            if (conditions[w].Last().CompareTo(_dictionary[node._index][conditions[w][0].Replace("---", "").Split(" ")[0].ToCharArray()[0] - '0']) >= 0)
                            {
                                counter++;
                            }
                        }

                        if (conditions[w][1] == "<=")
                        {
                            if (conditions[w].Last().CompareTo(_dictionary[node._index][conditions[w][0].Replace("---", "").Split(" ")[0].ToCharArray()[0] - '0']) <= 0)
                            {
                                counter++;
                            }
                        }
                    }
                    else if (conditions[w][0].Contains("--"))
                    {
                        if (conditions[w][1] == "=")
                        {
                            if (_dictionary[node._index][conditions[w][0].Replace("--", "").Split(" ")[0].ToCharArray()[0] - '0'] == conditions[w].Last())
                            {
                                counter++;
                            }
                        }

                        if (conditions[w][1] == "!=")
                        {
                            if (_dictionary[node._index][conditions[w][0].Replace("--", "").Split(" ")[0].ToCharArray()[0] - '0'] != conditions[w].Last())
                            {
                                counter++;
                            }
                        }

                        if (conditions[w][1] == ">")
                        {
                            if (_dictionary[node._index][conditions[w][0].Replace("--", "").Split(" ")[0].ToCharArray()[0] - '0'].CompareTo(conditions[w].Last()) > 0)
                            {
                                counter++;
                            }
                        }

                        if (conditions[w][1] == "<")
                        {
                            if (_dictionary[node._index][conditions[w][0].Replace("--", "").Split(" ")[0].ToCharArray()[0] - '0'].CompareTo(conditions[w].Last()) < 0)
                            {
                                counter++;
                            }
                        }

                        if (conditions[w][1] == ">=")
                        {
                            if (_dictionary[node._index][conditions[w][0].Replace("--", "").Split(" ")[0].ToCharArray()[0] - '0'].CompareTo(conditions[w].Last()) >= 0)
                            {
                                counter++;
                            }
                        }

                        if (conditions[w][1] == "<=")
                        {
                            if (_dictionary[node._index][conditions[w][0].Replace("--", "").Split(" ")[0].ToCharArray()[0] - '0'].CompareTo(conditions[w].Last()) <= 0)
                            {
                                counter++;
                            }
                        }
                    }
                    else if (conditions[w][0].IndexOf("-") == 0)
                    {
                        if (conditions[w][1] == "=")
                        {
                            if (_dictionary[node._index][conditions[w][0].Replace("-", "").Split(" ")[0].ToCharArray()[0] - '0'] == _dictionary[node._index][conditions[w].Last().ToCharArray()[0] - '0'])
                            {
                                counter++;
                            }
                        }

                        if (conditions[w][1] == "!=")
                        {
                            if (_dictionary[node._index][conditions[w][0].Replace("-", "").Split(" ")[0].ToCharArray()[0] - '0'] != _dictionary[node._index][conditions[w].Last().ToCharArray()[0] - '0'])
                            {
                                counter++;
                            }
                        }

                        if (conditions[w][1] == ">")
                        {
                            if (_dictionary[node._index][conditions[w][0].Replace("-", "").Split(" ")[0].ToCharArray()[0] - '0'].CompareTo(_dictionary[node._index][conditions[w].Last().ToCharArray()[0] - '0']) > 0)
                            {
                                counter++;
                            }
                        }

                        if (conditions[w][1] == "<")
                        {
                            if (_dictionary[node._index][conditions[w][0].Replace("-", "").Split(" ")[0].ToCharArray()[0] - '0'].CompareTo(_dictionary[node._index][conditions[w].Last().ToCharArray()[0] - '0']) < 0)
                            {
                                counter++;
                            }
                        }

                        if (conditions[w][1] == ">=")
                        {
                            if (_dictionary[node._index][conditions[w][0].Replace("-", "").Split(" ")[0].ToCharArray()[0] - '0'].CompareTo(_dictionary[node._index][conditions[w].Last().ToCharArray()[0] - '0']) >= 0)
                            {
                                counter++;
                            }
                        }

                        if (conditions[w][1] == "<=")
                        {
                            if (_dictionary[node._index][conditions[w][0].Replace("-", "").Split(" ")[0].ToCharArray()[0] - '0'].CompareTo(_dictionary[node._index][conditions[w].Last().ToCharArray()[0] - '0']) <= 0)
                            {
                                counter++;
                            }
                        }
                    }

                }

                if (counter == conditions.Count)
                {
                    For_Del.Add(node.Value.ToString());
                }
            }

            if (node.Right != null) InorderDel(node.Right, For_Del, conditions, _dictionary);
        }

        public void INorder_ORDER(AVLTreeNode<T> node, List<string> _order)
        {
            if (node == null)
                return;

            if (node.Left != null) INorder_ORDER(node.Left, _order);

            if (node != Head)
            {
                _order.Add(node._index);
                
            }

            if (node.Right != null) INorder_ORDER(node.Right, _order);

        }

        public void INorder_I(AVLTreeNode<T> node, Dictionary<string, List<string>> _same, ref string ___final, List<string> _basta)
        {
            if (node == null)
                return;

            if (node.Left != null) INorder_I(node.Left, _same, ref ___final, _basta);

            if (node != Head)
            {
                if (!_basta.Contains(node._index))
                {
                    if (!_same.ContainsKey(node.Value.ToString()))
                    {
                        List<string> vs = new List<string>();
                        vs.Add(node._index);
                        _same.Add(node.Value.ToString(), vs);
                    }
                    else
                    {
                        _same[node.Value.ToString()].Add(node._index);
                    }
                    ___final += node._index;
                }
            }

            if (node.Right != null) INorder_I(node.Right, _same, ref ___final, _basta);

        }
        public void POSTorder_I(AVLTreeNode<T> node, Dictionary<string, List<string>> _same, ref string ___final, List<string> _basta)
        {
            if (node == null)
                return;

            if (node.Right != null) POSTorder_I(node.Right, _same, ref ___final, _basta);

            if (node != Head)
            {
                if (!_basta.Contains(node._index))
                {
                    if (!_same.ContainsKey(node.Value.ToString()))
                    {
                        List<string> vs = new List<string>();
                        vs.Add(node._index);
                        _same.Add(node.Value.ToString(), vs);
                    }
                    else
                    {
                        _same[node.Value.ToString()].Add(node._index);
                    }
                    ___final += node._index;
                }
            }

            if (node.Left != null) POSTorder_I(node.Left, _same, ref ___final, _basta);

        }

        public void POSTorder_ORDER(AVLTreeNode<T> node, List<string> _order)
        {
            if (node == null)
                return;

            if (node.Right != null) POSTorder_ORDER(node.Right, _order);
            
            if (node != Head)
            {
                _order.Add(node._index);
               
            }

            if (node.Left != null) POSTorder_ORDER(node.Left, _order);
            

        }
    }
}
