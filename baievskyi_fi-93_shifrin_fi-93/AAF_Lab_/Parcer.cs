using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;

namespace AAF_Lab_
{
    internal class Parcer: DATABASE
    {
        string str;

        public Parcer(string STRING)
        {
            str = STRING;
        }
        public void TryParceString(DATABASE DataBase)
        {
            int t = 0; // Отвечает за индекс скобочной структуры в строке после разбиения 
            int g = 0; // Отвечает за количество слов в строке со скобочной структурой
            int d = 0; // Отвечает за индекс скобочной структуры в строке после разбиения
            int l = 0; // Last word in string han number ... 

            if (!str.Contains(";"))
            {
                Console.WriteLine("\nВведена неизвестная команда.");
            }
            else
            {
                str = str.Split(';')[0];
                str = Regex.Replace(str, @"\s+", " ", RegexOptions.Multiline);

                if ((str.Split(" ")[0].ToUpper() == "CREATE") || (str.Split(" ")[0].ToUpper() == "INSERT"))
                {
                    if (str.Split(" ")[0].ToUpper() == "CREATE")
                    {
                        str = Regex.Replace(str, "CREATE", "CREATE", RegexOptions.IgnoreCase);
                        str = Regex.Replace(str, "INDEXED", "INDEXED", RegexOptions.IgnoreCase);
                    }
                    else
                    {
                        str = Regex.Replace(str, "INSERT", "INSERT", RegexOptions.IgnoreCase);
                        str = Regex.Replace(str, "INTO", "INTO", RegexOptions.IgnoreCase);
                    }

                    CI(str, ref t, ref g, ref d, ref l, DataBase);
                }
                else if ((str.Split(" ")[0].ToUpper() == "SELECT") || (str.Split(" ")[0].ToUpper() == "DELETE"))
                {
                    if (str.Split(" ")[0].ToUpper() == "SELECT")
                    {
                        str = Regex.Replace(str, "SELECT", "SELECT", RegexOptions.IgnoreCase);
                        str = Regex.Replace(str, "FROM", "FROM", RegexOptions.IgnoreCase);
                        str = Regex.Replace(str, "ORDER_BY", "ORDER_BY", RegexOptions.IgnoreCase);
                        str = Regex.Replace(str, "WHERE", "WHERE", RegexOptions.IgnoreCase);
                        str = Regex.Replace(str, "ASC", "ASC", RegexOptions.IgnoreCase);
                        str = Regex.Replace(str, "DESC", "DESC", RegexOptions.IgnoreCase);
                    }
                    else
                    {
                        str = Regex.Replace(str, "DELETE", "DELETE", RegexOptions.IgnoreCase);
                        str = Regex.Replace(str, "FROM", "FROM", RegexOptions.IgnoreCase);
                        str = Regex.Replace(str, "WHERE", "WHERE", RegexOptions.IgnoreCase);
                    }

                    _SD(DataBase, str, ref t, ref g, ref d, ref l);
                }
                else if (str.Split(" ")[0].ToUpper() == "PRINT" && (str.Split(" ")[1].ToUpper() == "TABLE"))
                {
                    str = Regex.Replace(str, "PRINT", "PRINT", RegexOptions.IgnoreCase);
                    str = Regex.Replace(str, "TABLE", "TABLE", RegexOptions.IgnoreCase);
                    PrintTree(DataBase, str.Split(" ")[2]);
                }
                else
                {
                    Console.WriteLine("\nВведена неизвестная команда.");
                }
            }
        }
        public static void A(string[] arr)
        {
            int l = 0;

            for (int q = 0; q < arr.Length; q++)
            {
                if (arr[q + 1] == null)
                {
                    l = q;
                    q = arr.Length;
                }

            }

            for (int q = 1; q < arr.Length; q++)
            {
                try
                {
                    if (arr[q] != null)
                    {
                        if (arr[q].Contains(","))
                        {
                            string[] _arr = arr[q].Split(",");
                            for (int r = l; r != q; r--)
                            {
                                arr[r + _arr.Length - 1] = arr[r];
                                l++;
                            }
                            int h = q;
                            foreach (string n in _arr)
                            {
                                arr[h] = n.Trim();
                                h++;
                            }
                        }
                    }
                }
                catch
                {
                    Console.WriteLine("Неизвестная команда.");
                }
            }
        }

        public static void CI(string str, ref int t, ref int g, ref int d, ref int l, DATABASE db)
        {
            string[] arr = new string[str.Split(" ").Length + 2];
            arr[0] = str.Trim();
            bool c = false;
            bool v = false;
            int j = 1; // Отвечает за подмассив слов, попавших в круглые скобки
            int k = 0; // Отвечает за счётчик в циклах

            {
                for (int i = 0; i < str.Length; i++)
                {
                    if ((str[i] == '\"') && (v == false) && (c == false))
                    {
                        v = true;
                    }
                    else if ((str[i] == '\"') && (v == true) && (c == false))
                    {
                        v = false;
                    }

                    if ((str[i] == '(') && c == false)
                    {
                        c = true;
                    }
                    else if ((str[i] == ')') && c == true)
                    {
                        c = false;
                        t = j;
                    }

                    if (((str[i] == ' ') && (c == false) && (v == false)) || i == str.Length - 1)
                    {
                        if (str.Substring(k, i - k) != " ")
                        {
                            arr[j] = str.Substring(k, i - k + 1).Trim();
                            if (i == str.Length)
                            {
                                arr[j] = str.Substring(k, i - k + 1);
                            }


                            if ((arr[j][0] == (char)34) && (arr[j][arr[j].Length - 1] == (char)34))
                            {
                                arr[j] = arr[j].Remove(0, 1);
                                arr[j] = arr[j].Remove(arr[j].Length - 1, 1);
                            }



                            if (arr[j][0] == '(')
                            {
                                d = j;
                                arr[j] = arr[j].Remove(0, 1);
                            }

                            if (arr[j][arr[j].Length - 1] == ')')
                            {
                                arr[j] = arr[j].Remove(arr[j].Length - 1, 1);
                            }

                            j++;
                            k = i;
                        }
                    }
                    else if (((str[i] == ' ') && (c == false) && (v == true)) || i == str.Length) { };

                    //Console.Write(str[i]);
                }
            }

            for (int q = 0; q < arr.Length - 1; q++)
            {
                if (arr[q + 1] == null)
                {
                    l = q;
                    q = arr.Length - 1;
                }
            }

            if (arr[t] != null)
            {
                //|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||\\

                c = false;
                v = false;
                j = 0;
                k = 0;

                for (int q = 0; q < arr[t].Length; q++)
                {
                    {
                        if ((arr[t][q] == '\"') && (v == false) && (c == false))
                        {
                            v = true;
                        }
                        else if ((arr[t][q] == '\"') && (v == true) && (c == false))
                        {
                            v = false;
                        }

                        if ((arr[t][q] == '(') && c == false)
                        {
                            c = true;
                        }
                        else if ((arr[t][q] == ')') && c == true)
                        {
                            c = false;
                            t = j;
                        }
                    }

                    if (((arr[t][q] == ',') && (c == false) && (v == false)) || (q == arr[t].Length - 1))
                    {
                        if (arr[t].Substring(k, q - k) != " ")
                        {
                            g++;
                            j++;
                            k = q;
                        }
                    }
                    else if (((arr[t][q] == ' ') && (c == false) && (v == true)) || q == arr[t].Length - 1) { };
                }


                //|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||\\

            }

            {
                c = false;
                v = false;
                j = 0;
                k = 0;
                
                string[] _arr = new string[g];
                for (int q = 0; q < arr[t].Length; q++)
                {
                    {
                        if ((arr[t][q] == '\"') && (v == false) && (c == false))
                        {
                            v = true;
                        }
                        else if ((arr[t][q] == '\"') && (v == true) && (c == false))
                        {
                            v = false;
                        }

                        if ((arr[t][q] == '(') && c == false)
                        {
                            c = true;
                        }
                        else if ((arr[t][q] == ')') && c == true)
                        {
                            c = false;
                            t = j;
                        }
                    }

                    if (((arr[t][q] == ',') && (c == false) && (v == false)) || (q == arr[t].Length - 1))
                    {
                        if (arr[t].Substring(k, q - k) != " ")
                        {
                            _arr[j] = arr[t].Substring(k, q - k).Trim();
                            if (q == arr[t].Length - 1)
                            {
                                _arr[j] = arr[t].Substring(k, q - k + 1);
                            }

                            if ((_arr[j][0] == ',') && (_arr[j][1] == ' '))
                            {
                                _arr[j] = _arr[j].Remove(0, 1);
                                _arr[j] = _arr[j].Remove(0, 1);
                            }

                            while ((_arr[j][0] == (char)34) || (_arr[j][_arr[j].Length - 1] == (char)34))
                            {
                                if ((_arr[j][0] == (char)34) && (_arr[j][_arr[j].Length - 1] == (char)34))
                                {
                                    _arr[j] = _arr[j].Remove(0, 1);
                                    _arr[j] = _arr[j].Remove(_arr[j].Length - 1, 1);
                                }

                                if ((_arr[j][0] == (char)34))
                                {
                                    _arr[j] = _arr[j].Remove(0, 1);
                                }
                            }

                            j++;
                            k = q;
                        }
                    }
                    else if (((arr[t][q] == ' ') && (c == false) && (v == true)) || q == arr[t].Length - 1) { };
                }


                if (arr[t] != null)
                {
                    string[] __arr = new string[new Regex("INDEXED").Matches(arr[t]).Count];
                    int m = 0;
                    for (int q = 0; q < _arr.Length; q++)
                    {
                        if (_arr[q] != null)
                        {
                            if (_arr[q].Contains(" INDEXED"))
                            {
                                _arr[q] = _arr[q].Replace(" INDEXED", "-");
                                _arr[q] = _arr[q].Replace(", ", "");
                                __arr[m] = _arr[q];
                                m++;
                            }

                            if (_arr[q].Contains("\""))
                            {
                                _arr[q] = _arr[q].Replace("\"", "");
                            }
                        }
                    }
                    for (int q = 0; q < _arr.Length; q++)
                    {
                        arr[arr.Length - _arr.Length + q] = _arr[q]; // Именно в этом месте рождается последняя повторяющася строка 
                    }
                }

            }

            C(arr, l, d, g, t, db);
        }

        public static void C(string[] arr, int l, int d, int g, int t, DATABASE db)
        {
            if (arr[1] == "CREATE")
            {
                if ((t == 0) || (l != 3))
                {
                    Console.WriteLine("\nВведена неизвестная команда.");
                }
                else
                {
                    if ((l == 3) && (d == 3))
                    {
                        if (g != 0)
                        {
                            Console.Write("\n\nБудет создана таблица с названием {0} и колонками ", arr[2]);
                            int gg = g;

                            string[] ar = new string[g];
                            
                            for (int q = 0; q < g; q++)
                            {
                                if (q < g - 2)
                                {
                                    Console.Write(arr[arr.Length - g + q].Replace("-", " (индексируется)") + ", ");
                                    ar[q] = arr[arr.Length - g + q].Replace("-", string.Empty);
                                    if (arr[arr.Length - g + q].Contains("-"))
                                    {
                                        gg++;
                                    }
                                }
                                else if (q < g - 1)
                                {
                                    Console.Write(arr[arr.Length - g + q].Replace("-", " (индексируется)") + " и ");
                                    ar[q] = arr[arr.Length - g + q].Replace("-", string.Empty);
                                    if (arr[arr.Length - g + q].Contains("-"))
                                    {
                                        gg++;
                                    }
                                }
                                else
                                {
                                    Console.Write(arr[arr.Length - g + q].Replace("-", " (индексируется)") + ".");
                                    ar[q] = arr[arr.Length - g + q].Replace("-", string.Empty);
                                    if (arr[arr.Length - g + q].Contains("-"))
                                    {
                                        gg++;
                                    }
                                }

                            }

                            bool c = false;
                            foreach (var item in db.DaBa)
                            {
                                if (item.Keys.Contains(arr[2])) c = true;
                            }
                            if (!c)
                            {
                                Dictionary<string, BD> keyValuePairs = new Dictionary<string, BD>();
                                Dictionary<string, BD> dict = new Dictionary<string, BD>();
                                BD F = new BD(ar, l, d, g, t);
                                dict.Add(arr[2].Trim(), F);
                                db.DaBa.Add(dict);
                            }
                            else 
                            {
                                Console.WriteLine("\n\nНевозможно создать таблицу, ведь таблица с таким названием уже существует.");
                            }

                        }
                        else
                        {
                            Console.WriteLine("\nВведена неизвестная команда.");
                        }
                    }
                }

            }

            if (arr[1] == "INSERT")
            {
                if (t == 0)
                {
                    Console.WriteLine("\nВведена неизвестная команда.");
                }
                else
                {
                    if ((l != 3) && (l != 4))
                    {
                        Console.WriteLine("\nВведена неизвестная команда.");
                    }
                    else
                    {
                        if (l == 3)
                        {
                            if (d == 3)
                            {
                                if ((g != 0) && (arr[t].Split("\"").Count() == (2 * g + 1)) && (arr[t - 1] != "INTO"))
                                {
                                    Console.Write("\n\nВ таблицу с названием {0} будут добавлены следующие данные: (", arr[2]);

                                    string[] ar = new string[g];

                                    for (int q = 0; q < g; q++)
                                    {
                                        if (q < g - 1)
                                        {
                                            Console.Write(arr[arr.Length - g + q].Replace("-", " (индексируется)") + ", ");
                                            ar[q] = arr[arr.Length - g + q].Replace("-", string.Empty);
                                        }
                                        else
                                        {
                                            Console.Write(arr[arr.Length - g + q].Replace("-", " (индексируется)") + ")\n");
                                            ar[q] = arr[arr.Length - g + q].Replace("-", string.Empty);
                                        }

                                    }

                                    if (db.DaBa.Count > 0)
                                    {
                                        foreach (var item in db.DaBa)
                                        {
                                            if (item.ContainsKey(arr[2]) && (ar.Length == item[arr[2]]._colums.Count))
                                            {
                                                item[arr[2]].I(ar, l, d, g, t);
                                            }
                                            else
                                            {
                                                Console.WriteLine("\nВведена неизвестная команда.");
                                            }
                                        }
                                    }
                                    else
                                    {
                                        Console.WriteLine("\nВведена неизвестная команда.");
                                    }

                                }
                                else
                                {
                                    Console.WriteLine("\nВведена неизвестная команда.");
                                }
                            }
                            else
                            {
                                if ((g != 0) && (arr[t].Split("\"").Count() == (2 * g + 1)) && (arr[t + 1] != "INTO"))
                                {
                                    Console.Write("\n\nВ таблицу с названием {0} будут добавлены следующие данные: (", arr[3]);

                                    string[] ar = new string[g];

                                    for (int q = 0; q < g; q++)
                                    {
                                        if (q < g - 1)
                                        {
                                            Console.Write(arr[arr.Length - g + q].Replace("-", " (индексируется)") + ", ");
                                            ar[q] = arr[arr.Length - g + q].Replace("-", string.Empty);
                                        }
                                        else
                                        {
                                            Console.Write(arr[arr.Length - g + q].Replace("-", " (индексируется)") + ")\n");
                                            ar[q] = arr[arr.Length - g + q].Replace("-", string.Empty);
                                        }

                                    }

                                    if (db.DaBa.Count > 0)
                                    {
                                        foreach (var item in db.DaBa)
                                        {
                                            if (item.ContainsKey(arr[3]) && (ar.Length == item[arr[3]]._colums.Count))
                                            {
                                                item[arr[3]].I(ar, l, d, g, t);
                                            }
                                            else
                                            {
                                                Console.WriteLine("\nВведена неизвестная команда.");
                                            }
                                        }
                                    }
                                    else
                                    {
                                        Console.WriteLine("\nВведена неизвестная команда.");
                                    }
                                }
                                else
                                {
                                    Console.WriteLine("\nВведена неизвестная команда.");
                                }
                            }
                        }


                        if (l == 4)
                        {
                            if ((arr[2] == "INTO") || (arr[3] == "INTO"))
                            {
                                if ((d != 2) && (d != 4))
                                {
                                    Console.WriteLine("\nВведена неизвестная команда.");
                                }
                                else
                                {
                                    if (d == 2)
                                    {
                                        if ((g != 0) && (arr[t].Split("\"").Count() == (2 * g + 1)))
                                        {
                                            Console.Write("\n\nВ таблицу с названием {0} будут добавлены следующие данные: (", arr[4]);

                                            string[] ar = new string[g];

                                            for (int q = 0; q < g; q++)
                                            {
                                                if (q < g - 1)
                                                {
                                                    Console.Write(arr[arr.Length - g + q].Replace("-", " (индексируется)") + ", ");
                                                    ar[q] = arr[arr.Length - g + q].Replace("-", string.Empty);
                                                }
                                                else
                                                {
                                                    Console.Write(arr[arr.Length - g + q].Replace("-", " (индексируется)") + ")\n");
                                                    ar[q] = arr[arr.Length - g + q].Replace("-", string.Empty);
                                                }

                                            }

                                            if (db.DaBa.Count > 0)
                                            {
                                                foreach (var item in db.DaBa)
                                                {
                                                    if (item.ContainsKey(arr[4]) && (ar.Length == item[arr[4]]._colums.Count))
                                                    {
                                                        item[arr[4]].I(ar, l, d, g, t);
                                                    }
                                                    else
                                                    {
                                                        Console.WriteLine("\nВведена неизвестная команда.");
                                                    }
                                                }
                                            }
                                            else
                                            {
                                                Console.WriteLine("\nВведена неизвестная команда.");
                                            }
                                        }
                                        else
                                        {
                                            Console.WriteLine("\nВведена неизвестная команда.");
                                        }
                                    }

                                    if (d == 4)
                                    {
                                        if ((g != 0) && (arr[t].Split("\"").Count() == (2 * g + 1)))
                                        {
                                            Console.Write("\n\nВ таблицу с названием {0} будут добавлены следующие данные: (", arr[3]);

                                            string[] ar = new string[g];

                                            for (int q = 0; q < g; q++)
                                            {
                                                if (q < g - 1)
                                                {
                                                    Console.Write(arr[arr.Length - g + q].Replace("-", " (индексируется)") + ", ");
                                                    ar[q] = arr[arr.Length - g + q].Replace("-", string.Empty);
                                                }
                                                else
                                                {
                                                    Console.Write(arr[arr.Length - g + q].Replace("-", " (индексируется)") + ")\n");
                                                    ar[q] = arr[arr.Length - g + q].Replace("-", string.Empty);
                                                }
                                            }

                                            if (db.DaBa.Count > 0)
                                            {
                                                foreach (var item in db.DaBa)
                                                {
                                                    if (item.ContainsKey(arr[3]) && (ar.Length == item[arr[3]]._colums.Count))
                                                    {
                                                        item[arr[3]].I(ar, l, d, g, t);
                                                    }
                                                    else
                                                    {
                                                        Console.WriteLine("\nВведена неизвестная команда.");
                                                    }
                                                }
                                            }
                                            else
                                            {
                                                Console.WriteLine("\nВведена неизвестная команда.");
                                            }
                                        }
                                        else
                                        {
                                            Console.WriteLine("\nВведена неизвестная команда.");
                                        }
                                    }
                                }
                            }
                            else
                            {
                                Console.WriteLine("\nВведена неизвестная команда.");
                            }
                        }
                    }
                }

            }
        }
        public static void _SD(DATABASE DataBase, string str, ref int t, ref int g, ref int d, ref int l)
        {
            string[] arr = new string[str.Split(" ").Length + 4];
            arr[0] = str.Trim();
            string[] ummy = new string[arr[0].Split(" ").Length + 1];
            ummy[0] = arr[0];

            int sel = 0;
            int fr = 0;
            int whe = 0;
            int gro = 0;


            if ((str.Split(" ")[0] == "SELECT") && (str.Replace("SELECT", "").Trim() != ""))
            {
                if (str.Contains("FROM"))
                {
                    if ((new Regex("FROM").Matches(str).Count == 1) && (str.Replace("SELECT", "").Replace("FROM", "").Trim() != ""))
                    {
                        if (str.Contains("WHERE"))
                        {
                            if ((new Regex("WHERE").Matches(str).Count == 1) && (str.Replace("SELECT", "").Replace("FROM", "").Replace("WHERE", "").Trim() != ""))
                            {
                                if (str.Contains("ORDER_BY"))
                                {
                                    if ((new Regex("ORDER_BY").Matches(str).Count == 1) && (str.Replace("SELECT", "").Replace("FROM", "").Replace("WHERE", "").Replace("ORDER_BY", "").Trim() != ""))
                                    {
                                        ummy[1] = str.Split("SELECT")[1].Trim().Split("FROM")[0].Trim();
                                        ummy[2] = str.Split("FROM")[1].Trim().Split("WHERE")[0].Trim();
                                        ummy[3] = str.Split("WHERE")[1].Trim().Split("ORDER_BY")[0].Trim();
                                        ummy[4] = str.Split("ORDER_BY")[1].Trim();

                                        arr[1] = "SELECT";
                                        arr[2] = ummy[1];
                                        arr[3] = "FROM";
                                        arr[4] = ummy[2];
                                        arr[5] = "WHERE";
                                        arr[6] = ummy[3];
                                        arr[7] = "ORDER_BY";
                                        arr[8] = ummy[4];

                                        string table_name = "";
                                        List<string> lim = new List<string>();
                                        List<string> conditions = new List<string>();
                                        List<string> column_name = new List<string>();
                                        string ASC_or_DESC = "ASC";

                                        A(arr);
                                        {
                                            for (int q = 0; q < arr.Length; q++)
                                            {
                                                if (arr[q] == "SELECT") sel = q;
                                                if (arr[q] == "FROM") fr = q;
                                                if (arr[q] == "WHERE") whe = q;
                                                if (arr[q] == "ORDER_BY") gro = q;
                                            }

                                            if (arr[sel + 1].Contains("*"))
                                            {
                                                Console.Write("\n\nИз таблицы {0} будут выбраны все столбцы, ", arr[fr + 1]);
                                                table_name = arr[fr + 1];
                                            }
                                            else
                                            {
                                                Console.Write("\n\nИз таблицы {0} будут выбраны столбцы ", arr[fr + 1]);
                                                table_name = arr[fr + 1];

                                                for (int q = sel + 1; q < fr; q++)
                                                {
                                                    if ((sel - fr) == 1)
                                                    {
                                                        Console.Write(arr[q] + ".");
                                                        if (lim.Contains(arr[q]))
                                                        {
                                                            //lim.Add("ERROR");
                                                            lim.Add(arr[q]);
                                                        }
                                                        else
                                                        {
                                                            lim.Add(arr[q]);
                                                        }
                                                    }
                                                    else
                                                    {
                                                        if (q < fr - 2)
                                                        {
                                                            Console.Write(arr[q] + ", ");
                                                            if (lim.Contains(arr[q]))
                                                            {
                                                                //lim.Add("ERROR");
                                                                lim.Add(arr[q]);
                                                            }
                                                            else
                                                            {
                                                                lim.Add(arr[q]);
                                                            }
                                                        }
                                                        else if (q == fr - 2)
                                                        {
                                                            Console.Write(arr[q] + " и ");
                                                            if (lim.Contains(arr[q]))
                                                            {
                                                                lim.Add(arr[q]);
                                                                //lim.Add("ERROR");
                                                            }
                                                            else
                                                            {
                                                                lim.Add(arr[q]);
                                                            }
                                                        }
                                                        else
                                                        {
                                                            Console.Write(arr[q] + ", ");
                                                            if (lim.Contains(arr[q]))
                                                            {
                                                                //lim.Add("ERROR");
                                                                lim.Add(arr[q]);
                                                            }
                                                            else
                                                            {
                                                                lim.Add(arr[q]);
                                                            }
                                                        }

                                                    }
                                                }
                                            }

                                            Console.Write("удовлетворяющие условиям ");

                                            for (int q = whe + 1; q < gro; q++)
                                            {
                                                if ((gro - whe) == 1)
                                                {
                                                    Console.Write(arr[q] + ".");
                                                    conditions.Add(arr[q]);
                                                }
                                                else
                                                {
                                                    if (q < gro - 2)
                                                    {
                                                        Console.Write(arr[q] + ", ");
                                                        conditions.Add(arr[q]);
                                                    }
                                                    else if (q == gro - 2)
                                                    {
                                                        Console.Write(arr[q] + " и ");
                                                        conditions.Add(arr[q]);
                                                    }
                                                    else
                                                    {
                                                        Console.Write(arr[q] + ", ");
                                                        conditions.Add(arr[q]);
                                                    }

                                                }
                                            }
                                            Console.Write("упорядоченные в соответсвии с такими критериями: ");
                                            for (int q = gro + 1; q < arr.Length; q++)
                                            {
                                                if (arr[q] != null)
                                                {
                                                    if (q != gro + 1)
                                                    {
                                                        if (arr[q].Contains("ASC"))
                                                        {
                                                            Console.Write(", " + arr[q].Replace("ASC", "по возрастанию")); //ASCENDING
                                                            if (!column_name.Contains(arr[q].Replace("ASC", "").Replace("DESC", "").Trim()))
                                                            {
                                                                column_name.Add(arr[q]);
                                                            }
                                                            ASC_or_DESC = "ASC";
                                                        }

                                                        if (arr[q].Contains("DESC"))
                                                        {
                                                            Console.Write(", " + arr[q].Replace("DESC", "по убыванию")); //DESCENDING
                                                            if (!column_name.Contains(arr[q].Replace("ASC", "").Replace("DESC", "").Trim()))
                                                            {
                                                                column_name.Add(arr[q]);
                                                            }
                                                            ASC_or_DESC = "DESC";
                                                        }

                                                        if (!(arr[q].Contains("ASC")) && !(arr[q].Contains("DESC")))
                                                        {
                                                            Console.Write(", " + arr[q]);
                                                            if (!column_name.Contains(arr[q].Replace("ASC", "").Replace("DESC", "").Trim()))
                                                            {
                                                                column_name.Add(arr[q]);
                                                            }
                                                        }
                                                    }
                                                    if (q == gro + 1)
                                                    {
                                                        if (arr[q].Contains("ASC"))
                                                        {
                                                            Console.Write(arr[q].Replace("ASC", "по возрастанию")); //ASCENDING
                                                            if (!column_name.Contains(arr[q].Replace("ASC", "").Replace("DESC", "").Trim()))
                                                            {
                                                                column_name.Add(arr[q]);
                                                            }
                                                            ASC_or_DESC = "ASC";
                                                        }

                                                        if (arr[q].Contains("DESC"))
                                                        {
                                                            Console.Write(arr[q].Replace("DESC", "по убыванию")); //DESCENDING
                                                            if (!column_name.Contains(arr[q].Replace("ASC", "").Replace("DESC", "").Trim()))
                                                            {
                                                                column_name.Add(arr[q]);
                                                            }
                                                            column_name.Add(arr[q]);
                                                            ASC_or_DESC = "DESC";
                                                        }

                                                        if (!(arr[q].Contains("ASC")) && !(arr[q].Contains("DESC")))
                                                        {
                                                            Console.Write(arr[q]);
                                                            Console.Write(", " + arr[q]);
                                                            if (!column_name.Contains(arr[q].Replace("ASC", "").Replace("DESC", "").Trim()))
                                                            {
                                                                column_name.Add(arr[q]);
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                        Console.WriteLine();
                                        foreach (var item in DataBase.DaBa)
                                        {
                                            if (lim != null)
                                            {
                                                if ((lim.Count > item[table_name]._dictionary["0"].Length) || (column_name.Count > item[table_name]._dictionary["0"].Length))
                                                {
                                                    Console.WriteLine("\nВведена неизвестная команда.");
                                                }
                                                else
                                                {
                                                    int i = 0;

                                                    foreach (var name in lim)
                                                    {
                                                        if ((item[table_name]._dictionary["0"].Contains(name)) && !(lim.Contains("ERROR"))) i++;
                                                    }
                                                    if (i == lim.Count)
                                                    {
                                                        i = 0;

                                                        foreach (var name in column_name)
                                                        {
                                                            if (item[table_name]._dictionary["0"].Contains(name.Replace("ASC", "").Replace("DESC", "").Trim())) i++;
                                                        }

                                                        if (i == column_name.Count)
                                                        {
                                                            PrintTable(DataBase, table_name, lim.ToArray(), conditions.ToArray(), column_name.ToArray(), ASC_or_DESC);
                                                        }
                                                        else
                                                        {
                                                            Console.WriteLine("\nВведена неизвестная команда.");
                                                        }
                                                    }
                                                    else
                                                    {
                                                        Console.WriteLine("\nВведена неизвестная команда.");
                                                    }
                                                }

                                            }
                                            
                                        }
                                        

                                        // DONE
                                    }
                                    else
                                    {
                                        Console.WriteLine("\nВведена неизвестная команда.");
                                    }
                                }
                                else
                                {
                                    ummy[1] = str.Split("SELECT")[1].Trim().Split("FROM")[0].Trim();
                                    ummy[2] = str.Split("FROM")[1].Trim().Split("WHERE")[0].Trim();
                                    ummy[3] = str.Split("WHERE")[1].Trim();

                                    arr[1] = "SELECT";
                                    arr[2] = ummy[1];
                                    arr[3] = "FROM";
                                    arr[4] = ummy[2];
                                    arr[5] = "WHERE";
                                    arr[6] = ummy[3];

                                    string table_name = "";
                                    List<string> lim = new List<string>();
                                    List<string> conditions = new List<string>();
                                    List<string> column_name = new List<string>();
                                    string ASC_or_DESC = "ASC";

                                    A(arr);

                                    {
                                        for (int q = 0; q < arr.Length; q++)
                                        {
                                            if (arr[q] == "SELECT") sel = q;
                                            if (arr[q] == "FROM") fr = q;
                                            if (arr[q] == "WHERE") whe = q;
                                        }

                                        if (arr[sel + 1].Contains("*"))
                                        {
                                            Console.Write("\n\nИз таблицы {0} будут выбраны все столбцы, ", arr[fr + 1]);
                                            table_name = arr[fr + 1];
                                        }
                                        else
                                        {
                                            Console.Write("\n\nИз таблицы {0} будут выбраны столбцы ", arr[fr + 1]);
                                            table_name = arr[fr + 1];
                                            for (int q = sel + 1; q < fr; q++)
                                            {
                                                if ((sel - fr) == 1)
                                                {
                                                    Console.Write(arr[q] + ".");
                                                    if (lim.Contains(arr[q]))
                                                    {
                                                        lim.Add("ERROR");
                                                    }
                                                    else
                                                    {
                                                        lim.Add(arr[q]);
                                                    }
                                                }
                                                else
                                                {
                                                    if (q < fr - 2)
                                                    {
                                                        Console.Write(arr[q] + ", ");
                                                        if (lim.Contains(arr[q]))
                                                        {
                                                            //lim.Add("ERROR");
                                                            lim.Add(arr[q]);
                                                        }
                                                        else
                                                        {
                                                            lim.Add(arr[q]);
                                                        }
                                                    }
                                                    else if (q == fr - 2)
                                                    {
                                                        Console.Write(arr[q] + " и ");
                                                        if (lim.Contains(arr[q]))
                                                        {
                                                            //lim.Add("ERROR");
                                                            lim.Add(arr[q]);
                                                        }
                                                        else
                                                        {
                                                            lim.Add(arr[q]);
                                                        }
                                                    }
                                                    else
                                                    {
                                                        Console.Write(arr[q] + ", ");
                                                        if (lim.Contains(arr[q]))
                                                        {
                                                            //lim.Add("ERROR");
                                                            lim.Add(arr[q]);
                                                        }
                                                        else
                                                        {
                                                            lim.Add(arr[q]);
                                                        }
                                                    }

                                                }
                                            }
                                        }

                                        Console.Write("удовлетворяющие условиям ");

                                        for (int q = whe + 1; q < arr.Length; q++)
                                        {
                                            if (arr[q] != null)
                                            {
                                                if (q != whe + 1)
                                                {
                                                    Console.Write(", " + arr[q]);
                                                    conditions.Add(arr[q].Trim());
                                                }
                                                if (q == whe + 1)
                                                {
                                                    Console.Write(arr[q]);
                                                    conditions.Add(arr[q].Trim());
                                                }
                                            }
                                        }
                                        Console.Write(".");
                                    }

                                    Console.WriteLine();

                                    foreach (var item in DataBase.DaBa)
                                    {
                                        if (lim != null)
                                        {
                                            /*if ((lim.Count > item[table_name]._dictionary["0"].Length) || (column_name.Count > item[table_name]._dictionary["0"].Length))
                                            {
                                                Console.WriteLine("\nВведена неизвестная команда.");
                                            }
                                            else
                                            {*/
                                                int i = 0;

                                                foreach (var name in lim)
                                                {
                                                    if ((item[table_name]._dictionary["0"].Contains(name)) && !(lim.Contains("ERROR"))) i++;
                                                }
                                                if (i == lim.Count)
                                                {
                                                    i = 0;

                                                    foreach (var name in column_name)
                                                    {
                                                        if (item[table_name]._dictionary["0"].Contains(name.Replace("ASC", "").Replace("DESC", "").Trim())) i++;
                                                    }

                                                    if (i == column_name.Count)
                                                    {
                                                        PrintTable(DataBase, table_name, lim.ToArray(), conditions.ToArray(), column_name.ToArray(), "");
                                                    }
                                                    else
                                                    {
                                                        Console.WriteLine("\nВведена неизвестная команда.");
                                                    }
                                                }
                                                else
                                                {
                                                    Console.WriteLine("\nВведена неизвестная команда.");
                                                }
                                            //}
                                        }
                                    }
                                    
                                    //DONE
                                }
                            }
                            else
                            {
                                Console.WriteLine("\nВведена неизвестная команда.");
                            }
                        }
                        else
                        {
                            if (str.Contains("ORDER_BY"))
                            {
                                if ((new Regex("ORDER_BY").Matches(str).Count == 1) && (str.Replace("SELECT", "").Replace("FROM", "").Replace("ORDER_BY", "").Trim() != ""))
                                {
                                    ummy[1] = str.Split("SELECT")[1].Trim().Split("FROM")[0].Trim();
                                    ummy[2] = str.Split("FROM")[1].Trim().Split("ORDER_BY")[0].Trim();
                                    ummy[3] = str.Split("ORDER_BY")[1].Trim();

                                    arr[1] = "SELECT";
                                    arr[2] = ummy[1];
                                    arr[3] = "FROM";
                                    arr[4] = ummy[2];
                                    arr[5] = "ORDER_BY";
                                    arr[6] = ummy[3];

                                    string table_name = "";
                                    List<string> lim = new List<string>();
                                    List<string> conditions = new List<string>();
                                    List<string> column_name = new List<string>();
                                    string ASC_or_DESC = "ASC";

                                    A(arr);

                                    {
                                        for (int q = 0; q < arr.Length; q++)
                                        {
                                            if (arr[q] == "SELECT") sel = q;
                                            if (arr[q] == "FROM") fr = q;
                                            if (arr[q] == "ORDER_BY") gro = q;
                                        }

                                        if (arr[sel + 1].Contains("*"))
                                        {
                                            Console.Write("\n\nИз таблицы {0} будут выбраны все столбцы, ", arr[fr + 1]);
                                            table_name = arr[fr + 1];
                                        }
                                        else
                                        {
                                            Console.Write("\n\nИз таблицы {0} будут выбраны столбцы ", arr[fr + 1]);
                                            table_name = arr[fr + 1];

                                            for (int q = sel + 1; q < fr; q++)
                                            {
                                                if ((sel - fr) == 1)
                                                {
                                                    Console.Write(arr[q] + ".");
                                                    if (lim.Contains(arr[q]))
                                                    {
                                                        //lim.Add("ERROR");
                                                        lim.Add(arr[q]);
                                                    }
                                                    else
                                                    {
                                                        lim.Add(arr[q]);
                                                    }
                                                }
                                                else
                                                {
                                                    if (q != fr - 2)
                                                    {
                                                        Console.Write(arr[q] + ", ");
                                                        if (lim.Contains(arr[q]))
                                                        {
                                                            //lim.Add("ERROR");
                                                            lim.Add(arr[q]);
                                                        }
                                                        else
                                                        {
                                                            lim.Add(arr[q]);
                                                        }
                                                    }
                                                    else if (q != fr - 1)
                                                    {
                                                        Console.Write(arr[q] + " и ");
                                                        if (lim.Contains(arr[q]))
                                                        {
                                                            //lim.Add("ERROR");
                                                            lim.Add(arr[q]);
                                                        }
                                                        else
                                                        {
                                                            lim.Add(arr[q]);
                                                        }
                                                    }
                                                    else
                                                    {
                                                        Console.Write(arr[q] + ", ");
                                                        if (lim.Contains(arr[q]))
                                                        {
                                                            //lim.Add("ERROR");
                                                            lim.Add(arr[q]);
                                                        }
                                                        else
                                                        {
                                                            lim.Add(arr[q]);
                                                        }
                                                    }

                                                }
                                            }
                                        }

                                        Console.Write("упорядоченные в соответсвии с такими критериями: ");

                                        for (int q = gro + 1; q < arr.Length; q++)
                                        {
                                            if (arr[q] != null)
                                            {
                                                if (q != gro + 1)
                                                {
                                                    if (arr[q].Contains("ASC"))
                                                    {
                                                        Console.Write(", " + arr[q].Replace("ASC", "по возрастанию")); //ASCENDING
                                                        if (!column_name.Contains(arr[q].Replace("ASC", "").Replace("DESC", "").Trim()))
                                                        {
                                                            column_name.Add(arr[q]);
                                                        }

                                                        ASC_or_DESC = "ASC";
                                                    }

                                                    if (arr[q].Contains("DESC"))
                                                    {
                                                        Console.Write(", " + arr[q].Replace("DESC", "по убыванию")); //DESCENDING
                                                        if (!column_name.Contains(arr[q].Replace("ASC", "").Replace("DESC", "").Trim()))
                                                        {
                                                            column_name.Add(arr[q]);
                                                        }
                                                        ASC_or_DESC = "DESC";
                                                    }

                                                    if (!(arr[q].Contains("ASC")) && !(arr[q].Contains("DESC")))
                                                    {
                                                        Console.Write(", " + arr[q]);
                                                        if (!column_name.Contains(arr[q].Replace("ASC", "").Replace("DESC", "").Trim()))
                                                        {
                                                            column_name.Add(arr[q]);
                                                        }
                                                    }
                                                }
                                                if (q == gro + 1)
                                                {
                                                    if (arr[q].Contains("ASC"))
                                                    {
                                                        Console.Write(", " + arr[q].Replace("ASC", "по возрастанию")); //ASCENDING
                                                        if (!column_name.Contains(arr[q].Replace("ASC", "").Replace("DESC", "").Trim()))
                                                        {
                                                            column_name.Add(arr[q]);
                                                        }
                                                        ASC_or_DESC = "ASC";
                                                    }

                                                    if (arr[q].Contains("DESC"))
                                                    {
                                                        Console.Write(", " + arr[q].Replace("DESC", "по убыванию")); //DESCENDING
                                                        if (!column_name.Contains(arr[q].Replace("ASC", "").Replace("DESC", "").Trim()))
                                                        {
                                                            column_name.Add(arr[q]);
                                                        }
                                                        ASC_or_DESC = "DESC";
                                                    }

                                                    if (!(arr[q].Contains("ASC")) && !(arr[q].Contains("DESC")))
                                                    {
                                                        Console.Write(", " + arr[q]);
                                                        if (!column_name.Contains(arr[q].Replace("ASC", "").Replace("DESC", "").Trim()))
                                                        {
                                                            column_name.Add(arr[q]);
                                                        }
                                                    }

                                                }
                                            }
                                        }
                                        Console.Write(".");
                                    }

                                    Console.WriteLine();

                                    foreach (var item in DataBase.DaBa)
                                    {
                                        if (lim != null)
                                        {
                                            /*if ((lim.Count > item[table_name]._dictionary["0"].Length) || (column_name.Count > item[table_name]._dictionary["0"].Length))
                                            {
                                                Console.WriteLine("\nВведена неизвестная команда.");
                                            }
                                            else
                                            {*/
                                                int i = 0;

                                                foreach (var name in lim)
                                                {
                                                    if ((item[table_name]._dictionary["0"].Contains(name)) && !(lim.Contains("ERROR"))) i++;
                                                }
                                                if (i == lim.Count)
                                                {
                                                    i = 0;

                                                    foreach (var name in column_name)
                                                    {
                                                        if (item[table_name]._dictionary["0"].Contains(name.Replace("ASC", "").Replace("DESC", "").Trim())) i++;
                                                    }

                                                    if (i == column_name.Count)
                                                    {
                                                        PrintTable(DataBase, table_name, lim.ToArray(), conditions.ToArray(), column_name.ToArray(), ASC_or_DESC);
                                                    }
                                                    else
                                                    {
                                                        Console.WriteLine("\nВведена неизвестная команда.");
                                                    }
                                                }
                                                else
                                                {
                                                    Console.WriteLine("\nВведена неизвестная команда.");
                                                }
                                            //}
                                        }
                                        else
                                        {
                                            if (column_name.Count > item[table_name]._dictionary["0"].Length)
                                            {
                                                Console.WriteLine("\nВведена неизвестная команда.");
                                            }
                                            else
                                            {
                                                int i = 0;
                                                foreach (var name in column_name)
                                                {
                                                    if (item[table_name]._dictionary["0"].Contains(name.Replace("ASC", "").Replace("DESC", "").Trim())) i++;
                                                }

                                                if (i == column_name.Count)
                                                {
                                                    PrintTable(DataBase, table_name, lim.ToArray(), conditions.ToArray(), column_name.ToArray(), ASC_or_DESC);
                                                }
                                                else
                                                {
                                                    Console.WriteLine("\nВведена неизвестная команда.");
                                                }
                                            }

                                        }
                                    }
                                    //DONE
                                }
                                else
                                {
                                    Console.WriteLine("\nВведена неизвестная команда.");
                                }
                            }
                            else
                            {
                                ummy[1] = str.Split("SELECT")[1].Trim().Split("FROM")[0].Trim();
                                ummy[2] = str.Split("FROM")[1].Trim();

                                arr[1] = "SELECT";
                                arr[2] = ummy[1];
                                arr[3] = "FROM";
                                arr[4] = ummy[2];

                                string table_name = "";
                                List<string> lim = new List<string>();
                                List<string> conditions = new List<string>();
                                List<string> column_name = new List<string>();
                                string ASC_or_DESC = "ASC";


                                A(arr);

                                {
                                    for (int q = 0; q < arr.Length; q++)
                                    {
                                        if (arr[q] == "SELECT") sel = q;
                                        if (arr[q] == "FROM") fr = q;
                                    }

                                    if (arr[sel + 1].Contains("*"))
                                    {
                                        Console.Write("\n\nИз таблицы {0} будут выбраны все столбцы, ", arr[fr + 1]);
                                        table_name = arr[fr + 1];
                                    }
                                    else
                                    {
                                        Console.Write("\n\nИз таблицы {0} будут выбраны столбцы ", arr[fr + 1]);
                                        table_name = arr[fr + 1];

                                        for (int q = sel + 1; q < fr; q++)
                                        {
                                            if ((sel - fr) == 1)
                                            {
                                                Console.Write(arr[q] + ".");
                                                if (lim.Contains(arr[q]))
                                                {
                                                    lim.Add("ERROR");
                                                }
                                                else 
                                                {
                                                    lim.Add(arr[q]);
                                                }
                                            }
                                            else
                                            {
                                                if (q < fr - 2)
                                                {
                                                    Console.Write(arr[q] + ", ");
                                                    if (lim.Contains(arr[q]))
                                                    {
                                                        lim.Add(arr[q]);
                                                        //lim.Add("ERROR");
                                                    }
                                                    else
                                                    {
                                                        lim.Add(arr[q]);
                                                    }
                                                }
                                                else if (q == fr - 2)
                                                {
                                                    Console.Write(arr[q] + " и ");
                                                    if (lim.Contains(arr[q]))
                                                    {
                                                        //lim.Add("ERROR");
                                                        lim.Add(arr[q]);
                                                    }
                                                    else
                                                    {
                                                        lim.Add(arr[q]);
                                                    }
                                                }
                                                else
                                                {
                                                    Console.Write(arr[q] + ".");
                                                    if (lim.Contains(arr[q]))
                                                    {
                                                        //lim.Add("ERROR");
                                                        lim.Add(arr[q]);
                                                    }
                                                    else
                                                    {
                                                        lim.Add(arr[q]);
                                                    }
                                                }

                                            }
                                        }
                                    }


                                }

                                Console.WriteLine();
                                
                                foreach (var item in DataBase.DaBa)
                                {
                                    if (item.ContainsKey(arr[fr+1]))
                                    {
                                        if (lim != null)
                                        {
                                            /*if ((lim.Count > item[table_name]._dictionary["0"].Length) || (column_name.Count > item[table_name]._dictionary["0"].Length))
                                            {
                                                Console.WriteLine("\nВведена неизвестная команда.");
                                            }
                                            else
                                            {*/
                                                int i = 0;

                                                foreach (var name in lim)
                                                {
                                                    if ((item[table_name]._dictionary["0"].Contains(name)) && !(lim.Contains("ERROR"))) i++;
                                                }
                                                if (i == lim.Count)
                                                {
                                                    i = 0;

                                                    foreach (var name in column_name)
                                                    {
                                                        if (item[table_name]._dictionary["0"].Contains(name.Replace("ASC", "").Replace("DESC", "").Trim())) i++;
                                                    }

                                                    if (i == column_name.Count)
                                                    {
                                                        PrintTable(DataBase, table_name, lim.ToArray(), conditions.ToArray(), column_name.ToArray(), "");
                                                    }
                                                    else
                                                    {
                                                        Console.WriteLine("\nВведена неизвестная команда.");
                                                    }
                                                }
                                                else
                                                {
                                                    Console.WriteLine("\nВведена неизвестная команда.");
                                                }
                                            //}
                                        }
                                    }
                                    else
                                    {
                                        Console.WriteLine("Введена неизвестная команда.");
                                    }
                                }
                                //DONE
                            }
                        }
                    }
                    else
                    {
                        Console.WriteLine("\nВведена неизвестная команда.");
                    }
                }
                else
                {
                    Console.WriteLine("\nВведена неизвестная команда.");
                }
            }
            else if ((str.Split(" ")[0] == "DELETE") && (str.Replace("DELETE", "").Trim() != ""))
            {
                if (str.Contains("FROM"))
                {
                    if ((new Regex("FROM").Matches(str).Count == 1) && (str.Replace("DELETE", "").Replace("FROM", "").Trim() != ""))
                    {
                        if (str.Contains("WHERE"))
                        {
                            if ((new Regex("WHERE").Matches(str).Count == 1) && (str.Replace("DELETE", "").Replace("FROM", "").Replace("WHERE", "").Trim() != ""))
                            {
                                ummy[1] = str.Split("DELETE")[1].Trim().Split("FROM")[0].Trim();
                                ummy[2] = str.Split("FROM")[1].Trim().Split("WHERE")[0].Trim();
                                ummy[3] = str.Split("WHERE")[1].Trim();

                                arr[1] = "DELETE";
                                arr[2] = ummy[1];
                                arr[3] = "FROM";
                                arr[4] = ummy[2];
                                arr[5] = "WHERE";
                                arr[6] = ummy[3];

                                string table_name = "";
                                List<string> conditions = new List<string>();

                                A(arr);

                                {
                                    for (int q = 0; q < arr.Length; q++)
                                    {
                                        if (arr[q] == "DELETE") sel = q;
                                        if (arr[q] == "FROM") fr = q;
                                        if (arr[q] == "WHERE") whe = q;
                                    }

                                    if (arr[sel + 1].Contains("*"))
                                    {
                                        Console.Write("\n\nИз таблицы {0} будут удалены все столбцы,", arr[fr + 1]);
                                        table_name = arr[fr + 1];
                                        conditions.Add("*");
                                    }
                                    else
                                    {
                                        Console.Write("\n\nИз таблицы {0} будут удалены столбцы ", arr[fr + 1]);
                                        table_name = arr[fr + 1];

                                        for (int q = sel + 1; q < fr; q++)
                                        {
                                            if ((sel - fr) == 1)
                                            {
                                                Console.Write(arr[q] + ".");
                                            }
                                            else
                                            {
                                                if (q < fr - 2)
                                                {
                                                    Console.Write(arr[q] + ", ");
                                                }
                                                else if (q == fr - 2)
                                                {
                                                    Console.Write(arr[q] + " и ");
                                                }
                                                else
                                                {
                                                    Console.Write(arr[q] + ",");
                                                }

                                            }
                                        }
                                    }

                                    Console.Write(" удовлетворяющие условиям: ");

                                    for (int q = whe + 1; q < arr.Length; q++)
                                    {
                                        if (arr[q] != null)
                                        {
                                            if (q != whe + 1)
                                            {
                                                Console.Write(", " + arr[q]);
                                                conditions.Add(arr[q].Trim());
                                            }
                                            if (q == whe + 1)
                                            {
                                                Console.Write(arr[q]);
                                                conditions.Add(arr[q].Trim());
                                            }
                                        }
                                    }
                                    Console.Write(".");
                                }

                                DeleteSth(DataBase, table_name, conditions.ToArray());

                                //DONE
                            }
                            else
                            {
                                Console.WriteLine("\nВведена неизвестная команда.");
                            }
                        }
                        else
                        {
                            ummy[1] = str.Split("FROM")[1].Trim();

                            arr[1] = "DELETE";
                            arr[2] = "FROM";
                            arr[3] = ummy[1];

                            string table_name = "";
                            List<string> conditions = new List<string>();

                            A(arr);

                            {
                                for (int q = 0; q < arr.Length; q++)
                                {
                                    if (arr[q] == "DELETE") sel = q;
                                    if (arr[q] == "FROM") fr = q;
                                }

                                if (arr[sel + 1].Contains("*") || arr[sel + 1].Contains(""))
                                {
                                    Console.Write("\n\nИз таблицы {0} будут удалены все столбцы.", arr[fr + 1]);
                                    table_name = arr[fr + 1];
                                    conditions.Add("*");
                                }
                                else
                                {
                                    Console.Write("\n\nИз таблицы {0} будут удалены столбцы ", arr[fr + 1]);
                                    table_name = arr[fr + 1];

                                    for (int q = sel + 1; q < fr; q++)
                                    {
                                        if ((sel - fr) == 1)
                                        {
                                            Console.Write(arr[q] + ".");
                                        }
                                        else
                                        {
                                            if (q < fr - 2)
                                            {
                                                Console.Write(arr[q] + ", ");
                                            }
                                            else if (q == fr - 2)
                                            {
                                                Console.Write(arr[q] + " и ");
                                            }
                                            else
                                            {
                                                Console.Write(arr[q] + ".");
                                            }

                                        }
                                    }
                                }
                            }
                            DeleteSth(DataBase, table_name, conditions.ToArray());
                            //DONE
                        }
                    }
                    else
                    {
                        Console.WriteLine("\nВведена неизвестная команда.");
                    }
                }
                else
                {
                    if (str.Contains("WHERE"))
                    {
                        if ((new Regex("WHERE").Matches(str).Count == 1) && (str.Replace("DELETE", "").Replace("FROM", "").Replace("WHERE", "").Trim() != ""))
                        {
                            ummy[1] = str.Split("DELETE")[1].Trim().Split("WHERE")[0].Trim();
                            ummy[2] = str.Split("WHERE")[1].Trim();

                            arr[1] = "DELETE";
                            arr[2] = ummy[1];
                            arr[3] = "WHERE";
                            arr[4] = ummy[2];

                            string table_name = "";
                            List<string> conditions = new List<string>();

                            A(arr);

                            {
                                for (int q = 0; q < arr.Length; q++)
                                {
                                    if (arr[q] == "DELETE") sel = q;
                                    if (arr[q] == "WHERE") whe = q;
                                }


                                Console.Write("\n\nИз таблицы {0} будут удалены столбцы, удовлетворяющие условиям ", arr[sel + 1]);
                                table_name = arr[sel + 1];

                                for (int q = whe + 1; q < arr.Length; q++)
                                {
                                    if (arr[q] != null)
                                    {
                                        if (q != whe + 1)
                                        {
                                            Console.Write(", " + arr[q]);
                                            conditions.Add(arr[q].Trim());
                                        }
                                        if (q == whe + 1)
                                        {
                                            Console.Write(arr[q]);
                                            conditions.Add(arr[q].Trim());
                                        }
                                    }
                                }
                                Console.Write(".");

                                DeleteSth(DataBase, table_name, conditions.ToArray());
                                //DONE
                            }
                        }
                        else
                        {
                            Console.WriteLine("\nВведена неизвестная команда.");
                        }
                    }
                    else
                    {
                        ummy[1] = str.Split("DELETE")[1].Trim();
                        arr[1] = "DELETE";
                        arr[2] = ummy[1];

                        Console.Write("Таблица {0} будет удалена.", arr[2]);
                        DeleteSth(DataBase, arr[2], null);
                    }

                }
            }
            else
            {
                Console.WriteLine("\nВведена неизвестная команда.");
            }
        }

        public static void SD(string str, string[] arr, ref int t, ref int g, ref int d, ref int l)
        {
            bool c = false;
            bool v = false;
            int j = 1; // Отвечает за подмассив слов, попавших в круглые скобки
            int k = 0; // Отвечает за счётчик в циклах
            {
                //|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||\\

                c = false;
                v = false;
                j = 0;
                k = 0;

                for (int q = 0; q < arr[t].Length; q++)
                {
                    {
                        if ((arr[t][q] == '\"') && (v == false) && (c == false))
                        {
                            v = true;
                        }
                        else if ((arr[t][q] == '\"') && (v == true) && (c == false))
                        {
                            v = false;
                        }

                        if ((arr[t][q] == '(') && c == false)
                        {
                            c = true;
                        }
                        else if ((arr[t][q] == ')') && c == true)
                        {
                            c = false;
                            t = j;
                        }
                    }


                    if (((arr[t][q] == ',') && (c == false) && (v == false)) || (q == arr[t].Length - 1))
                    {
                        if (arr[t].Substring(k, q - k) != " ")
                        {
                            g++;
                            j++;
                            k = q;
                        }
                    }
                    else if (((arr[t][q] == ' ') && (c == false) && (v == true)) || q == arr[t].Length - 1) { };
                }
            }


            //|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||\\



            {
                c = false;
                v = false;
                j = 0;
                k = 0;
                string[] _arr = new string[g];
                for (int q = 0; q < arr[t].Length; q++)
                {
                    {
                        if ((arr[t][q] == '\"') && (v == false) && (c == false))
                        {
                            v = true;
                        }
                        else if ((arr[t][q] == '\"') && (v == true) && (c == false))
                        {
                            v = false;
                        }

                        if ((arr[t][q] == '(') && c == false)
                        {
                            c = true;
                        }
                        else if ((arr[t][q] == ')') && c == true)
                        {
                            c = false;
                            t = j;
                        }
                    }

                    if (((arr[t][q] == ',') && (c == false) && (v == false)) || (q == arr[t].Length - 1))
                    {
                        if (arr[t].Substring(k, q - k) != " ")
                        {
                            _arr[j] = arr[t].Substring(k, q - k).Trim();
                            if (q == arr[t].Length - 1)
                            {
                                _arr[j] = arr[t].Substring(k, q - k + 1);
                            }

                            if ((_arr[j][0] == ',') && (_arr[j][1] == ' '))
                            {
                                _arr[j] = _arr[j].Remove(0, 1);
                                _arr[j] = _arr[j].Remove(0, 1);
                            }

                            while ((_arr[j][0] == (char)34) || (_arr[j][_arr[j].Length - 1] == (char)34))
                            {
                                if ((_arr[j][0] == (char)34) && (_arr[j][_arr[j].Length - 1] == (char)34))
                                {
                                    _arr[j] = _arr[j].Remove(0, 1);
                                    _arr[j] = _arr[j].Remove(_arr[j].Length - 1, 1);
                                }

                                if ((_arr[j][0] == (char)34))
                                {
                                    _arr[j] = _arr[j].Remove(0, 1);
                                }
                            }

                            j++;
                            k = q;
                        }
                    }
                    else if (((arr[t][q] == ' ') && (c == false) && (v == true)) || q == arr[t].Length - 1) { };
                }

                string[] __arr = new string[new Regex("INDEXED").Matches(arr[t]).Count];
                int m = 0;
                for (int q = 0; q < _arr.Length; q++)
                {
                    if (_arr[q] != null)
                    {
                        if (_arr[q].Contains(" INDEXED"))
                        {
                            _arr[q] = _arr[q].Replace(" INDEXED", "");
                            _arr[q] = _arr[q].Replace(", ", "");
                            __arr[m] = _arr[q];
                            m++;
                        }

                        if (_arr[q].Contains("\""))
                        {
                            _arr[q] = _arr[q].Replace("\"", "");
                        }
                    }
                }
                for (int q = 0; q < _arr.Length; q++)
                {
                    arr[arr.Length - _arr.Length + q] = _arr[q];
                }

            }
        }

        
    }
}
