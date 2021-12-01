using System;
using System.Collections.Generic;
using System.Text;

namespace P1
{
    public class Node
    {
        public Node left, right;
        public Rectangle rec;
        public Point point;

        public Node(int x0, int y0, int x1, int y1)
        {
            left = null;
            right = null;
            rec = new Rectangle(x0, y0, x1, y1);
            point = null;
        }

        public Node(int x, int y)
        {
            left = null;
            right = null;
            rec = null;
            point = new Point(x, y);
        }
    }
}
