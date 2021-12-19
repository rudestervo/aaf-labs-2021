using AAF_Lab_;
using System;
using System.Text.RegularExpressions;

namespace Lab1
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.OutputEncoding = System.Text.Encoding.UTF8;
            bool exit = true;
            string temp = "";
            DATABASE DataBase = new DATABASE();

            Console.WriteLine("Команды, поддержуемые данной программой перечислены ниже:");
            Console.WriteLine("    1. CREATE table_name ( column_1 [INDEXED], column_2 [INDEXED], ...);");
            Console.WriteLine("    2. INSERT [INTO] table_name ( \"value_1\", \"value_2\", ...);");
            Console.WriteLine("    3. SELECT [* || column_1, column_2, ...] FROM table_name WHERE [condition_1, ...] [ORDER_BY column_1 || column_2 || ... [ASC || DESC]];");
            Console.WriteLine("    4. DELETE [FROM] table_name WHERE [condition_1, ...];");
            Console.WriteLine("Примечания: ");
            Console.WriteLine("    1. Допускается ввод сразу нескольких команд через точку с запятой.");
            Console.WriteLine("    2. Условия указываются в формате — {column_1 || \"value\"} operator {column_1 || \"value\"}.");
            Console.WriteLine("    3. Оператор модет иметь вид — { = || != || < || > || <= || >= }.");
            Console.WriteLine("    4. ASC - в прямом лексикографическом порядке, DESC - в обратном.");
            Console.WriteLine("    5. Для вывода любой таблицы существует команда - [PRINT TABLE table_name;].");
            Console.WriteLine("    6. Для выхода из программы нужно ввести команду - [EXIT;].");

            while (exit)
            {
                string str = "";
                Console.WriteLine("\n\n\nВведите Вашу команду:");
                if (temp != "")
                {
                    str = temp.Trim() + " " + Console.ReadLine();
                }
                else
                {
                    str = Console.ReadLine();
                }
                
                str = Regex.Replace(str, "EXIT", "EXIT", RegexOptions.IgnoreCase);

                if (str.Contains(";"))
                {
                    string[] comands = str.Split(";");

                    for (int q = 0; q < comands.Length - 1; q++)
                    {
                        if (comands[q] != "EXIT")
                        {
                            Parcer parcer = new Parcer(comands[q].Trim() + ";");
                            parcer.TryParceString(DataBase);
                        }
                        else
                        {
                            q = comands.Length;
                            exit = false;
                        }
                    }
                    temp = "";
                }
                else 
                {
                    temp = str;
                }
            }
        }
    }
}