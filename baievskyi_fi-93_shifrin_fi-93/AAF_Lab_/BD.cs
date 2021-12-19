using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace AAF_Lab_
{
    internal class BD
    {
        public Dictionary<string, string[]> _dictionary = new Dictionary<string, string[]>();

        public List<int> _spaces = new List<int>();
        public List<string> _colums = new List<string>();
        public List<AVLTree<string>> _able = new List<AVLTree<string>>();
        public int _l, _d, _g, _t;

        public BD(string[] arr, int l, int d, int g, int t)
        {
            _dictionary.Add("0", arr);

            foreach (string s in arr)
            {
                _colums.Add(s);
                _spaces.Add(s.Length);
            }
            foreach (var column in _colums)
            {
                AVLTree<string> Oak = new AVLTree<string>();

                Oak.Add(column, _colums.ToArray(), "0");
                _able.Add(Oak);
            }

            _l = l;
            _d = d;
            _g = g;
            _t = t;

        }
        public void I(string[] arr, int l, int d, int g, int t)
        {
            int q = 0;
            _dictionary.Add(_dictionary.Count.ToString(), arr);
            foreach (var tree in _able)
            {
                tree.Add(arr[q], arr, (_dictionary.Count - 1).ToString());
                if (arr[q].Length > _spaces[q]) _spaces[q] = arr[q].Length;
                q++;
            }
        }
        public void P(string word)
        {
            int j = 0;

            if (word == "")
            {
                int space = 0;

                foreach (var item in _spaces)
                {
                    space += item;
                }

                Console.WriteLine(String.Concat(Enumerable.Repeat("-", space + 5 * _colums.Count - 1)));

                for (int r = 0; r < _dictionary["0"].Length; r++)
                {
                    if (_dictionary["0"][r] == _dictionary["0"].Last())
                    {
                        Console.Write("| {0}{1} | \n", String.Concat(Enumerable.Repeat(" ", _spaces[r] - _dictionary["0"][r].Length)), _dictionary["0"][r]);
                    }
                    else
                    {
                        Console.Write("| {0}{1} | ", String.Concat(Enumerable.Repeat(" ", _spaces[r] - _dictionary["0"][r].Length)), _dictionary["0"][r]);
                    }
                }

                Console.WriteLine(String.Concat(Enumerable.Repeat("-", space + 5 * _colums.Count - 1)));

                _able[0].INorder(_able[0].Head, _spaces, _dictionary);

                Console.WriteLine(String.Concat(Enumerable.Repeat("-", space + 5 * _colums.Count - 1)));
            }
            else
            {
                int i = 0;

                int space = 0;

                foreach (var item in _spaces)
                {
                    space += item;
                }
                Console.WriteLine(String.Concat(Enumerable.Repeat("-", space + 5 * _colums.Count - 1)));

                while (word.Replace("ASC", "").Replace("DESC", "").Trim() != _colums[i])
                {
                    i++;
                    if (_colums[i] == null) break;
                }

                for (int r = 0; r < _dictionary["0"].Length; r++)
                {
                    if (_dictionary["0"][r] == _dictionary["0"].Last())
                    {
                        Console.Write("| {0}{1} | \n", String.Concat(Enumerable.Repeat(" ", _spaces[r] - _dictionary["0"][r].Length)), _dictionary["0"][r]);
                    }
                    else
                    {
                        Console.Write("| {0}{1} | ", String.Concat(Enumerable.Repeat(" ", _spaces[r] - _dictionary["0"][r].Length)), _dictionary["0"][r]);
                    }
                }

                Console.WriteLine(String.Concat(Enumerable.Repeat("-", space + 5 * _colums.Count - 1)));

                _able[i].INorder(_able[i].Head, _spaces, _dictionary);

                Console.WriteLine(String.Concat(Enumerable.Repeat("-", space + 5 * _colums.Count - 1)));
            }
        }

        public void _P(string word)
        {
            int j = 0;

            if (word == "")
            {
                int space = 0;

                foreach (var item in _spaces)
                {
                    space += item;
                }

                Console.WriteLine(String.Concat(Enumerable.Repeat("-", space + 5 * _colums.Count - 1)));

                for (int r = 0; r < _dictionary["0"].Length; r++)
                {
                    if (_dictionary["0"][r] == _dictionary["0"].Last())
                    {
                        Console.Write("| {0}{1} | \n", String.Concat(Enumerable.Repeat(" ", _spaces[r] - _dictionary["0"][r].Length)), _dictionary["0"][r]);
                    }
                    else
                    {
                        Console.Write("| {0}{1} | ", String.Concat(Enumerable.Repeat(" ", _spaces[r] - _dictionary["0"][r].Length)), _dictionary["0"][r]);
                    }
                }

                Console.WriteLine(String.Concat(Enumerable.Repeat("-", space + 5 * _colums.Count - 1)));

                PrintTableWithoutAnyConditions(_spaces);

                Console.WriteLine(String.Concat(Enumerable.Repeat("-", space + 5 * _colums.Count - 1)));
            }
            else
            {
                int i = 0;

                int space = 0;

                foreach (var item in _spaces)
                {
                    space += item;
                }
                Console.WriteLine(String.Concat(Enumerable.Repeat("-", space + 5 * _colums.Count - 1)));

                while (word != _colums[i])
                {
                    i++;
                    if (_colums[i] == null) break;
                }

                for (int r = 0; r < _dictionary["0"].Length; r++)
                {
                    if (_dictionary["0"][r] == _dictionary["0"].Last())
                    {
                        Console.Write("| {0}{1} | \n", String.Concat(Enumerable.Repeat(" ", _spaces[r] - _dictionary["0"][r].Length)), _dictionary["0"][r]);
                    }
                    else
                    {
                        Console.Write("| {0}{1} | ", String.Concat(Enumerable.Repeat(" ", _spaces[r] - _dictionary["0"][r].Length)), _dictionary["0"][r]);
                    }
                }

                Console.WriteLine(String.Concat(Enumerable.Repeat("-", space + 5 * _colums.Count - 1)));

                _able[i].INorder(_able[i].Head, _spaces, _dictionary);

                Console.WriteLine(String.Concat(Enumerable.Repeat("-", space + 5 * _colums.Count - 1)));
            }
        }
        public void PrintTableWithoutAnyConditions(List<int> _spaces)
        {
            foreach (var row in _dictionary)
            {
                if (row.Value[0] != _dictionary.First().Value[0])
                {
                    for (int q = 0; q < row.Value.Length; q++)
                    {
                        if (q == row.Value.Length - 1)
                        {
                            Console.Write("| {0}{1} | \n", String.Concat(Enumerable.Repeat(" ", _spaces[q] - row.Value[q].Length)), row.Value[q]);
                        }
                        else
                        {
                            Console.Write("| {0}{1} | ", String.Concat(Enumerable.Repeat(" ", _spaces[q] - row.Value[q].Length)), row.Value[q]);
                        }
                    }

                }
            }
        }
        public void PCL(string column_name, List<int> lims, List<string[]> conditions, string ASC_or_DESC, Dictionary<string, string[]> _dictionary)
        {
            int j = 0;

            if (column_name == "")
            {
                int space = 0;

                foreach (var item in lims)
                {
                        space += _spaces[item];   
                }
                Console.WriteLine(String.Concat(Enumerable.Repeat("-", space + 5 * lims.Count - 1)));

                for (int q = 0; q < lims.Count; q++)
                {
                    if (q == (lims.Count - 1))
                    {
                        Console.Write("| {0}{1} | \n", String.Concat(Enumerable.Repeat(" ", _spaces[lims[q]] - _dictionary["0"][lims[q]].Length)), _dictionary["0"][lims[q]]);
                    }
                    else
                    {
                        Console.Write("| {0}{1} | ", String.Concat(Enumerable.Repeat(" ", _spaces[lims[q]] - _dictionary["0"][lims[q]].Length)), _dictionary["0"][lims[q]]);
                    }
                }

                Console.WriteLine(String.Concat(Enumerable.Repeat("-", space + 5 * lims.Count - 1)));

                if (ASC_or_DESC.ToUpper() == "ASC")
                {
                    _able[0].INorderCL(_able[0].Head, lims, conditions, _spaces, _dictionary);
                }
                else if (ASC_or_DESC.ToUpper() == "DESC")
                {
                    _able[0].POSTorderCL(_able[0].Head, lims, conditions, _spaces, _dictionary);
                }
                else
                {
                    _able[0].INorderCL(_able[0].Head, lims, conditions, _spaces, _dictionary);
                }

                Console.WriteLine(String.Concat(Enumerable.Repeat("-", space + 5 * lims.Count - 1)));
            }
            else
            {
                int i = 0;
                while (column_name.Replace("ASC", "").Replace("DESC", "").Trim() != _colums[i])
                {
                    i++;
                    if (_colums[i] == null) break;
                }

                int space = 0;

                foreach (var item in lims)
                {
                    space += _spaces[item];
                }
                Console.WriteLine(String.Concat(Enumerable.Repeat("-", space + 5 * lims.Count - 1)));

                for (int q = 0; q < lims.Count; q++)
                {
                    if (q == (lims.Count - 1))
                    {
                        Console.Write("| {0}{1} | \n", String.Concat(Enumerable.Repeat(" ", _spaces[q] - _dictionary["0"][lims[q]].Length)), _dictionary["0"][lims[q]]);
                    }
                    else
                    {
                        Console.Write("| {0}{1} | ", String.Concat(Enumerable.Repeat(" ", _spaces[q] - _dictionary["0"][lims[q]].Length)), _dictionary["0"][lims[q]]);
                    }
                }

                Console.WriteLine(String.Concat(Enumerable.Repeat("-", space + 5 * lims.Count - 1)));

                if (ASC_or_DESC.ToUpper() == "ASC")
                {
                    _able[0].INorderCL(_able[i].Head, lims, conditions, _spaces, _dictionary);
                }
                else if (ASC_or_DESC.ToUpper() == "DESC")
                {
                    _able[0].POSTorderCL(_able[i].Head, lims, conditions, _spaces, _dictionary);
                }
                else
                {
                    _able[0].INorderCL(_able[i].Head, lims, conditions, _spaces, _dictionary);
                }

                Console.WriteLine(String.Concat(Enumerable.Repeat("-", space + 5 * lims.Count - 1)));
            }
        }

        public void PCL_ORDER(string[] column_name, List<int> lims, List<string[]> conditions, string ASC_or_DESC, Dictionary<string, string[]> _dictionary)
        {
            bool check = true;
            List<string> _order = new List<string>();
            List<string> _final = new List<string>();
            List<List<string>> _order_list = new List<List<string>>();
            Dictionary<string, List<string>> _same = new Dictionary<string, List<string>>();
            string ___final = "";
            List<string> _basta = new List<string>();
            Dictionary<string, string> _swap = new Dictionary<string, string>();

            foreach (var colum in column_name)
            {
                int i = 0;
                foreach (var elem in _order)
                {
                    if (elem.Replace("ASC", "").Replace("DESC", "").Trim() != colum.Replace("ASC", "").Replace("DESC", "").Trim())
                    {
                        i++;
                    }
                }

                if (i == _order.Count)
                {
                    _order.Add(colum);
                }
                else
                {
                    check = false;
                }
            }

            if (check == true)
            {
                foreach (var colum in _order)
                {
                    if (colum.Contains("DESC"))
                    {
                        List<string> _v = new List<string>();


                        _able[_colums.IndexOf(colum.Replace("DESC", "").Trim())].POSTorder_ORDER(_able[_colums.IndexOf(colum.Replace("DESC", "").Trim())].Head, _v);
                        _order_list.Add(_v);

                    }
                    else if ((colum.Contains("ASC")) || !(colum.Contains("DESC")))
                    {
                        List<string> _v = new List<string>();

                        _able[_colums.IndexOf(colum.Replace("ASC", "").Trim())].INorder_ORDER(_able[_colums.IndexOf(colum.Replace("ASC", "").Trim())].Head, _v);
                        _order_list.Add(_v);

                    }
                }
            }

            for (int s = 0; s < _order.Count; s++)
            {
                if (_order[s].Contains("DESC"))
                {
                    _able[_colums.IndexOf(_order[s].Replace("DESC", "").Trim())].POSTorder_I(_able[_colums.IndexOf(_order[s].Replace("DESC", "").Trim())].Head, _same, ref ___final, _basta);
                }
                else
                {
                    _able[_colums.IndexOf(_order[s].Replace("ASC", "").Trim())].INorder_I(_able[_colums.IndexOf(_order[s].Replace("ASC", "").Trim())].Head, _same, ref ___final, _basta);
                }

                if (_order[0].Contains("DESC"))
                {
                    if (s == 0)
                    {
                        foreach (var item in ___final.Reverse())
                        {
                            _swap.Add(item.ToString(), (___final.IndexOf(item) + 1).ToString());
                        }

                    }
                    else
                    {
                        Dictionary<string, string> _temp = new Dictionary<string, string>();
                        
                        foreach (var item in _swap)
                        {
                            _temp.Add(item.Key, item.Value);
                        }
                        
                        List<string> _check = new List<string>();

                        for (int i = 0; i < ___final.Length; i++)
                        {
                            foreach (var u in _swap)
                            {
                                if (u.Key.ToString() == ___final[i].ToString())
                                {
                                    _check.Add(u.Value);
                                    break;
                                }
                            }
                        }

                        if (!_order[s].Contains("DESC"))
                        {
                            foreach (var item in ___final)
                            {
                                string min = _temp.Count.ToString();

                                foreach (var v in _check)
                                {
                                    if (min.CompareTo(v) > 0)
                                    {
                                        min = v;
                                    }
                                }

                                _check.RemoveAt(_check.IndexOf(min));
                                _temp[item.ToString()] = min;

                            }
                        }
                        else 
                        {
                            foreach (var item in ___final.Reverse())
                            {
                                string max = "";

                                foreach (var v in _check)
                                {
                                    if (max.CompareTo(v) < 0)
                                    {
                                        max = v;
                                    }
                                }

                                _check.RemoveAt(_check.IndexOf(max));
                                _temp[item.ToString()] = max;

                            }
                        }

                        foreach (var item in _swap)
                        {
                            _swap[item.Key] = _temp[item.Key];
                        }

                    }
                }
                else
                {
                    if (s == 0)
                    {
                        foreach (var item in ___final)
                        {
                            _swap.Add(item.ToString(), (___final.IndexOf(item) + 1).ToString());
                        }

                    }
                    else
                    {
                        Dictionary<string, string> _temp = new Dictionary<string, string>();
                        foreach (var item in _swap)
                        {
                            _temp.Add(item.Key, item.Value);
                        }
                        List<string> _check = new List<string>();

                        for (int i = 0; i < ___final.Length; i++)
                        {
                            foreach (var u in _swap)
                            {
                                if (u.Key.ToString() == ___final[i].ToString())
                                {
                                    _check.Add(u.Value);
                                    break;
                                }
                            }
                        }

                        if (!_order[s].Contains("DESC"))
                        {
                            foreach (var item in ___final)
                            {
                                string min = _temp.Count.ToString();

                                foreach (var v in _check)
                                {
                                    if (min.CompareTo(v) > 0)
                                    {
                                        min = v;
                                    }
                                }

                                _check.RemoveAt(_check.IndexOf(min));
                                _temp[item.ToString()] = min;

                            }
                        }
                        else
                        {
                            foreach (var item in ___final.Reverse())
                            {
                                string max = "";

                                foreach (var v in _check)
                                {
                                    if (max.CompareTo(v) < 0)
                                    {
                                        max = v;
                                    }
                                }

                                _check.RemoveAt(_check.IndexOf(max));
                                _temp[item.ToString()] = max;

                            }
                        }


                        foreach (var item in _swap)
                        {
                            _swap[item.Key] = _temp[item.Key];
                        }


                        Console.WriteLine();
                    }
                }
                ___final = "";

                foreach (var item in _same)
                {
                    if (item.Value.Count == 1)
                    {
                        _basta.Add(item.Value[0]);
                    }
                }
                _same.Clear();
            }

            for (int i = 1; i <= _swap.Count(); i++)
            {
                foreach (var f in _swap)
                {
                    if ((f.Value).CompareTo(i.ToString()) == 0)
                    {
                        _final.Add(f.Key);
                    }
                }
            }

            int space = 0;

            foreach (var item in lims)
            {
                space += _spaces[item];
            }
            Console.WriteLine(String.Concat(Enumerable.Repeat("-", space + 5 * lims.Count - 1)));

            for (int q = 0; q < lims.Count; q++)
            {
                if (q == (lims.Count - 1))
                {
                    Console.Write("| {0}{1} | \n", String.Concat(Enumerable.Repeat(" ", _spaces[q] - _dictionary["0"][lims[q]].Length)), _dictionary["0"][lims[q]]);
                }
                else
                {
                    Console.Write("| {0}{1} | ", String.Concat(Enumerable.Repeat(" ", _spaces[q] - _dictionary["0"][lims[q]].Length)), _dictionary["0"][lims[q]]);
                }
            }

            Console.WriteLine(String.Concat(Enumerable.Repeat("-", space + 5 * lims.Count - 1)));
            for (int u = 0; u < _final.Count; u++)
            {
                int counter = 0;
                for (int w = 0; w < conditions.Count; w++)
                {
                    if (conditions[w][0].Contains("---"))
                    {
                        if (conditions[w][1] == "=")
                        {
                            if (_dictionary[_final[u]][conditions[w][0].Replace("---", "").Split(" ")[0].ToCharArray()[0] - '0'] == conditions[w].Last())
                            {
                                counter++;
                            }
                        }

                        if (conditions[w][1] == "!=")
                        {
                            if (_dictionary[_final[u]][conditions[w][0].Replace("---", "").Split(" ")[0].ToCharArray()[0] - '0'] != conditions[w].Last())
                            {
                                counter++;
                            }
                        }

                        if (conditions[w][1] == ">")
                        {
                            if (conditions[w].Last().CompareTo(_dictionary[_final[u]][conditions[w][0].Replace("---", "").Split(" ")[0].ToCharArray()[0] - '0']) > 0)
                            {
                                counter++;
                            }
                        }

                        if (conditions[w][1] == "<")
                        {
                            if (conditions[w].Last().CompareTo(_dictionary[_final[u]][conditions[w][0].Replace("---", "").Split(" ")[0].ToCharArray()[0] - '0']) < 0)
                            {
                                counter++;
                            }
                        }

                        if (conditions[w][1] == ">=")
                        {
                            if (conditions[w].Last().CompareTo(_dictionary[_final[u]][conditions[w][0].Replace("---", "").Split(" ")[0].ToCharArray()[0] - '0']) >= 0)
                            {
                                counter++;
                            }
                        }

                        if (conditions[w][1] == "<=")
                        {
                            if (conditions[w].Last().CompareTo(_dictionary[_final[u]][conditions[w][0].Replace("---", "").Split(" ")[0].ToCharArray()[0] - '0']) <= 0)
                            {
                                counter++;
                            }
                        }
                    }
                    else if (conditions[w][0].Contains("--"))
                    {
                        if (conditions[w][1] == "=")
                        {
                            if (_dictionary[_final[u]][conditions[w][0].Replace("--", "").Split(" ")[0].ToCharArray()[0] - '0'] == conditions[w].Last())
                            {
                                counter++;
                            }
                        }

                        if (conditions[w][1] == "!=")
                        {
                            if (_dictionary[_final[u]][conditions[w][0].Replace("--", "").Split(" ")[0].ToCharArray()[0] - '0'] != conditions[w].Last())
                            {
                                counter++;
                            }
                        }

                        if (conditions[w][1] == ">")
                        {
                            if (_dictionary[_final[u]][conditions[w][0].Replace("--", "").Split(" ")[0].ToCharArray()[0] - '0'].CompareTo(conditions[w].Last()) > 0)
                            {
                                counter++;
                            }
                        }

                        if (conditions[w][1] == "<")
                        {
                            if (_dictionary[_final[u]][conditions[w][0].Replace("--", "").Split(" ")[0].ToCharArray()[0] - '0'].CompareTo(conditions[w].Last()) < 0)
                            {
                                counter++;
                            }
                        }

                        if (conditions[w][1] == ">=")
                        {
                            if (_dictionary[_final[u]][conditions[w][0].Replace("--", "").Split(" ")[0].ToCharArray()[0] - '0'].CompareTo(conditions[w].Last()) >= 0)
                            {
                                counter++;
                            }
                        }

                        if (conditions[w][1] == "<=")
                        {
                            if (_dictionary[_final[u]][conditions[w][0].Replace("--", "").Split(" ")[0].ToCharArray()[0] - '0'].CompareTo(conditions[w].Last()) <= 0)
                            {
                                counter++;
                            }
                        }
                    }
                    else if (conditions[w][0].IndexOf("-") == 0)
                    {
                        if (conditions[w][1] == "=")
                        {
                            if (_dictionary[_final[u]][conditions[w][0].Replace("-", "").Split(" ")[0].ToCharArray()[0] - '0'] == _dictionary[_final[u]][conditions[w].Last().ToCharArray()[0] - '0'])
                            {
                                counter++;
                            }
                        }

                        if (conditions[w][1] == "!=")
                        {
                            if (_dictionary[_final[u]][conditions[w][0].Replace("-", "").Split(" ")[0].ToCharArray()[0] - '0'] != _dictionary[_final[u]][conditions[w].Last().ToCharArray()[0] - '0'])
                            {
                                counter++;
                            }
                        }

                        if (conditions[w][1] == ">")
                        {
                            if (_dictionary[_final[u]][conditions[w][0].Replace("-", "").Split(" ")[0].ToCharArray()[0] - '0'].CompareTo(_dictionary[_final[u]][conditions[w].Last().ToCharArray()[0] - '0']) > 0)
                            {
                                counter++;
                            }
                        }

                        if (conditions[w][1] == "<")
                        {
                            if (_dictionary[_final[u]][conditions[w][0].Replace("-", "").Split(" ")[0].ToCharArray()[0] - '0'].CompareTo(_dictionary[_final[u]][conditions[w].Last().ToCharArray()[0] - '0']) < 0)
                            {
                                counter++;
                            }
                        }

                        if (conditions[w][1] == ">=")
                        {

                            if (_dictionary[_final[u]][conditions[w][0].Replace("-", "").Split(" ")[0].ToCharArray()[0] - '0'].CompareTo(_dictionary[_final[u]][conditions[w].Last().ToCharArray()[0] - '0']) >= 0)
                            {
                                counter++;
                            }
                        }

                        if (conditions[w][1] == "<=")
                        {
                            if (_dictionary[_final[u]][conditions[w][0].Replace("-", "").Split(" ")[0].ToCharArray()[0] - '0'].CompareTo(_dictionary[_final[u]][conditions[w].Last().ToCharArray()[0] - '0']) <= 0)
                            {
                                counter++;
                            }
                        }
                    }

                }

                if (counter == conditions.Count)
                {
                    int q = 0;

                    /*
                                        foreach (var i in _dictionary[_final[u]])
                                        {*/
                    for (int t = 0; t < lims.Count; t++)
                    {
                        Console.Write("| {0}{1} | ", String.Concat(Enumerable.Repeat(" ", _spaces[q] - _dictionary[_final[u]][lims[t]].Length)), _dictionary[_final[u]][lims[t]]);
                        q++;
                    }
                        
                    //}
                    
                    Console.WriteLine();
                    
                }
            }
            Console.WriteLine(String.Concat(Enumerable.Repeat("-", space + 5 * lims.Count - 1)));
        }
    }
}

