using System;

namespace NewLab
{
    class Program
    {
        static void Main(string[] args)
        {
            Tree newTree = new Tree(new TreeNode(new Segment(3, 4)));
            

            newTree.Insert(new Segment(2, 7));
            newTree.Insert(new Segment(5, 8));
            newTree.Insert(new Segment(4, 6));
            newTree.Insert(new Segment(5, 10));

            newTree.PrettyPrint();
        }
    }
}
