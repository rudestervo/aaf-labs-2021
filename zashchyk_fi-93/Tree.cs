using System;
using System.Collections.Generic;
using System.Text;

namespace NewLab
{
    class Tree
    {
        private TreeNode Root;
        private Dictionary<int, List<Segment>> Dict;
        public int Depth { get; set; }

        public Tree(TreeNode root)
        {
            Root = root;
            Dict = new Dictionary<int, List<Segment>>();
            Depth = 0;
        }
        public Tree()
        {
            Root = null;
            Dict = new Dictionary<int, List<Segment>>();
            Depth = 0;
        }

        public void Insert(Segment data)
        {
            if (Root != null)
            {
                Root = Root.Insert(data);                
            }
            else
                Root = new TreeNode(data);
            Height();
        }

        private void FillDictionary()
        {
            if (Root != null)
            {
                for (int i = 0; i <= Depth; i++)
                {
                    Dict.Add(i, new List<Segment>());
                }
                Root.FillDictionary(Dict, 0);
            }

            else
                Console.WriteLine("Tree is empty");
        }

        public void PrettyPrint()
        {
            FillDictionary();
            for (int i = 0; i <= Depth; i++)
            {
                List<Segment> l = Dict[i];
                foreach (Segment s in l)
                {
                    string indent = new string(' ', i);
                    Console.WriteLine(indent + s);
                }
            }
        }

        public void Height()
        {
            Depth = Root.Height();
        }
    }
}
