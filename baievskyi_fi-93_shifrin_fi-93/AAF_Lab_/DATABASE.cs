using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;

namespace AAF_Lab_
{
    internal class DATABASE
    {
        public List<Dictionary<string, BD>> DaBa = new List<Dictionary<string, BD>>();

       

        public static void PrintTree(DATABASE DATABASE, string Table_Name)
        {
            int i = 0;
            foreach (var item in DATABASE.DaBa)
            {
                if (item.Keys.Contains(Table_Name))
                {
                    BD n = item[Table_Name];
                    item[Table_Name]._P("");
                }
                else
                {
                    i++;
                }
            }
            if (i == DATABASE.DaBa.Count)
            {
                Console.WriteLine("Таблица не найдена. Возможно, она не существует.");
            }
        }

        public static void PrintTable(DATABASE DATABASE, string Table_Name, string[] lim, string[] conditions, string[] column_name, string ASC_or_DESC)
        {
            
            string[] operators = new string[] { "=", "!=", ">", "<", "<=", ">=" };

            int i = 0;
            int p = 0;

            foreach (var item in DATABASE.DaBa)
            {
                if (item.Keys.Contains(Table_Name))
                {
                    List<int> lims = new List<int>();
                    List<string[]> numbers = new List<string[]>();
                    bool check = false;

                    foreach (var num in lim)
                    {
                        if (item[Table_Name]._colums.Contains(num.Trim()))
                        {
                            lims.Add(item[Table_Name]._colums.IndexOf(num.Trim()));
                        }
                    }

                    if (lims.Count == 0)
                    {
                        for (int q = 0; q < item[Table_Name]._colums.Count; q++)
                        {
                            lims.Add(q);
                        }
                    }

                    foreach (var num in conditions)
                    {
                        string opera = "";
                        foreach (var oper in operators)
                        {
                            if (num.Contains(oper))
                            {
                                opera = oper;
                            }
                        }


                        if ((item[Table_Name]._colums.Contains(num.Split(opera)[0].Trim())) && (item[Table_Name]._colums.Contains(num.Split(opera)[1].Trim())))
                        {
                            string[] cond = new string[] { "-" + item[Table_Name]._colums.IndexOf(num.Split(opera)[0].Trim()).ToString(), opera, item[Table_Name]._colums.IndexOf(num.Split(opera)[1].Trim()).ToString() };
                            numbers.Add(cond);
                        }
                        else if ((item[Table_Name]._colums.Contains(num.Split(opera)[0].Trim())) && !(item[Table_Name]._colums.Contains(num.Split(opera)[1].Trim())) && (num.Split(opera)[1].Trim().Contains("\"")) && !(num.Split(opera)[0].Trim().Contains("\"")))
                        {
                            string[] cond = new string[] { "--" + item[Table_Name]._colums.IndexOf(num.Split(opera)[0].Trim()).ToString(), opera, num.Split(opera)[1].Trim().Replace("\"", "") };
                            numbers.Add(cond);
                        }
                        else if ((item[Table_Name]._colums.Contains(num.Split(opera)[1].Trim())) && !(num.Split(opera)[1].Trim().Contains("\"")) && !(item[Table_Name]._colums.Contains(num.Split(opera)[0].Trim())) && (num.Split(opera)[0].Trim().Contains("\"")))
                        {
                            string[] cond = new string[] { "---" + item[Table_Name]._colums.IndexOf(num.Split(opera)[1].Trim()).ToString(), opera, num.Split(opera)[0].Trim().Replace("\"", "") };
                            numbers.Add(cond);
                        }
                        else
                        {
                            check = true;

                        }
                    }
                    if (check != true)
                    {
                        if (column_name.Length == 1)
                        {
                            item[Table_Name].PCL(column_name[0], lims, numbers, ASC_or_DESC, item[Table_Name]._dictionary);
                        }
                        else if (column_name.Length == 0)
                        {
                            item[Table_Name].PCL("", lims, numbers, ASC_or_DESC, item[Table_Name]._dictionary);
                        }
                        else
                        {
                            item[Table_Name].PCL_ORDER(column_name, lims, numbers, ASC_or_DESC, item[Table_Name]._dictionary);
                        }
                        
                    }
                    else
                    {
                        Console.WriteLine("В одном из условий допущена ошибка.");
                    }

                }
                else
                {
                    i++;
                }
            }
            if (i == DATABASE.DaBa.Count)
            {
                Console.WriteLine("\nНе удалось удалить таблицу. Возможно, она не существует.\n");
            }
        }

        public static void DeleteSth(DATABASE DATABASE, string Table_Name, string[] conditions)
        {
            string[] operators = new string[] { "=", "!=", ">", "<", "<=", ">=" };

            int i = 0;
            int p = 0;

            foreach (var item in DATABASE.DaBa)
            {
                if (!item.Keys.Contains(Table_Name)) i++;
            }
            if (i == DATABASE.DaBa.Count)
            {
                Console.WriteLine("\nНе удалось удалить таблицу. Возможно, она не существует.\n");
                return;
            }

            for (int r = 0; r < DATABASE.DaBa.Count; r++)
            {
                if (DATABASE.DaBa[r].Keys.Contains(Table_Name))
                {
                    if (conditions != null)
                    {
                        List<string[]> numbers = new List<string[]>();
                        bool check = false;

                        foreach (var num in conditions)
                        {
                            string opera = "";
                            foreach (var oper in operators)
                            {
                                if (num.Contains(oper))
                                {
                                    opera = oper;
                                }

                                if (num.Contains("*"))
                                {
                                    opera = "*";
                                }
                            }

                            if (opera == "*")
                            {
                                foreach (var item in DATABASE.DaBa[r][Table_Name]._colums)
                                {
                                    string[] cond = new string[] { "--" + DATABASE.DaBa[r][Table_Name]._colums.IndexOf(item), "!=", DATABASE.DaBa[r][Table_Name]._colums.IndexOf(item).ToString() };
                                    numbers.Add(cond);
                                }
                            }
                            else
                            {
                                if ((DATABASE.DaBa[r][Table_Name]._colums.Contains(num.Split(opera)[0].Trim())) && (DATABASE.DaBa[r][Table_Name]._colums.Contains(num.Split(opera)[1].Trim())))
                                {
                                    string[] cond = new string[] { "-" + DATABASE.DaBa[r][Table_Name]._colums.IndexOf(num.Split(opera)[0].Trim()).ToString(), opera, DATABASE.DaBa[r][Table_Name]._colums.IndexOf(num.Split(opera)[1].Trim()).ToString() };
                                    numbers.Add(cond);
                                }
                                else if ((DATABASE.DaBa[r][Table_Name]._colums.Contains(num.Split(opera)[0].Trim())) && !(DATABASE.DaBa[r][Table_Name]._colums.Contains(num.Split(opera)[1].Trim())) && (num.Split(opera)[1].Trim().Contains("\"")) && !(num.Split(opera)[0].Trim().Contains("\"")))
                                {
                                    string[] cond = new string[] { "--" + DATABASE.DaBa[r][Table_Name]._colums.IndexOf(num.Split(opera)[0].Trim()).ToString(), opera, num.Split(opera)[1].Trim().Replace("\"", "") };
                                    numbers.Add(cond);
                                }
                                else if ((DATABASE.DaBa[r][Table_Name]._colums.Contains(num.Split(opera)[1].Trim())) && !(num.Split(opera)[1].Trim().Contains("\"")) && !(DATABASE.DaBa[r][Table_Name]._colums.Contains(num.Split(opera)[0].Trim())) && (num.Split(opera)[0].Trim().Contains("\"")))
                                {
                                    string[] cond = new string[] { "---" + DATABASE.DaBa[r][Table_Name]._colums.IndexOf(num.Split(opera)[1].Trim()).ToString(), opera, num.Split(opera)[0].Trim().Replace("\"", "") };
                                    numbers.Add(cond);
                                }
                                else
                                {
                                    check = true;
                                }
                            }


                        }
                        if (check != true)
                        {
                            int g = 0;
                            foreach (var table in DATABASE.DaBa[r][Table_Name]._able)
                            {
                                List<string> For_Del = new List<string>();
                                table.InorderDel(table.Head, For_Del, numbers, DATABASE.DaBa[r][Table_Name]._dictionary);
                                g = For_Del.Count;
                                foreach (var element in For_Del)
                                {
                                    table.Remove(element);
                                }
                            }
                            Console.WriteLine("\nИз таблицы {0} будет удалено {1} строк.", Table_Name, g);
                        }
                        else
                        {
                            Console.WriteLine("В одном из условий допущена ошибка.");
                        }
                    }
                    else
                    {
                        DATABASE.DaBa.Remove(DATABASE.DaBa[r]);
                        Console.WriteLine("\nТаблица {0} удалена.", Table_Name);
                    }

                }
                else
                {
                    i++;
                }


            }
        }
    }
}
