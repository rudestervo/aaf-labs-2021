using System;
using System.Collections.Generic;
using System.Text;

namespace NewLab
{
    class Segment
    {
        private int Min { get; set; }
        private int Max { get; set; }

        public Segment(int min, int max) //Конструктор для Segment
        {
            Min = min;
            Max = max;
        }

        public Segment mutualSegment(Segment segment1, Segment segment2)
        {
            int newMin = Math.Min(segment1.Min, segment2.Min);
            int newMax = Math.Max(segment1.Max, segment2.Max);

            Segment newSeg = new Segment(newMin, newMax);

            return newSeg;
        }

        public int comapare(Segment segment1, Segment segment2)
        {
            int difference = Math.Max(segment1.Min, segment2.Min) - Math.Min(segment1.Min, segment2.Min) +
                             Math.Max(segment1.Max, segment2.Max) - Math.Min(segment1.Max, segment2.Max);
            return difference;
        }

        public bool Includes(Segment segment1, Segment segment2) //Перевірка на включення 2 в 1
        {
            if (segment1.Min < segment2.Min && segment1.Max > segment2.Max)
            {
                return true;
            }

            else if (segment1.Min == segment2.Min && segment1.Max > segment2.Max)
            {
                return true;
            }

            else if (segment1.Min < segment2.Min && segment1.Max == segment2.Max)
            {
                return true;
            }

            else if (segment1.Min == segment2.Min && segment1.Max == segment2.Max)
            {
                return true;
            }

            else return false;
        }
        public override string ToString()
        {
            return $"{Min} , {Max}";
        }
    }
}
