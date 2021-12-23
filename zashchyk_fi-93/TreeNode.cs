using System;
using System.Collections.Generic;
using System.Text;

namespace NewLab
{
    class TreeNode
    {
        public Segment segment;
        private TreeNode leftChild;
        private TreeNode rightChild;

        public TreeNode()
        {
            segment = null;
            leftChild = null;
            rightChild = null;
        }

        public TreeNode(Segment data)
        {
            segment = data;
            leftChild = null;
            rightChild = null;
        }

        public TreeNode Insert(Segment segmentToInsert)
        {
            TreeNode newParent = new TreeNode(segment.mutualSegment(segment, segmentToInsert));
            if (segment.Includes(segment, segmentToInsert))
            {
                if (leftChild == null)
                {
                    newParent.leftChild = this;
                    newParent.rightChild = new TreeNode(segmentToInsert);                    
                }
                else
                {
                    newParent = this;
                    if (segmentToInsert.comapare(segmentToInsert, leftChild.segment) < segmentToInsert.comapare(segmentToInsert, rightChild.segment))
                    {                      
                        leftChild = leftChild.Insert(segmentToInsert);
                    }
                    else
                    {                        
                        rightChild = rightChild.Insert(segmentToInsert);
                    }
                }
            }
            else
            {
                newParent.leftChild = this;
                newParent.rightChild = new TreeNode(segmentToInsert);
            }           
            return newParent;
        }

        public void FillDictionary(Dictionary<int, List<Segment>> dict, int depth)
        {
            dict[depth].Add(segment);
            depth++;            
            if (leftChild != null)
            {                
                leftChild.FillDictionary(dict, depth);
            }                        
            if (rightChild != null)
            {
                rightChild.FillDictionary(dict, depth);
            }
        }
        
        public int Height()
        {
            
            if (leftChild == null && rightChild == null)
            {
                return 0;
            }

            int left = 0;
            int right = 0;

            
            if (leftChild != null)
                left = leftChild.Height();
            if (rightChild != null)
                right = rightChild.Height();

            
            if (left > right)
            {
                return left + 1;
            }
            else
            {
                return right + 1;
            }

        }
    }
}
