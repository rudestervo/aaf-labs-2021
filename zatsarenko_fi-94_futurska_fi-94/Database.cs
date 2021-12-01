using System;
using System.Collections.Generic;
using System.Text;

namespace P1
{
    class Database
    {
        List<string> name;
        List<RTree> address;

        public Database()
        {
            name = new List<string>();
            address = new List<RTree>();
        }

        public void Add(string str, RTree link)
        {
            name.Add(str);
            address.Add(link);
        }

        public int Contains(string str)
        {
            if (name.Contains(str)) return 1;
            return 0;
        }

        public RTree Link(string str)
        {
            int index = name.IndexOf(str);
            return address[index];
        }
    }
}
