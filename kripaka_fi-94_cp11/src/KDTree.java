import java.util.Arrays;
import java.util.LinkedList;
import java.util.List;

public class KDTree {
    private int size = 0;
    Point2d head;

    public KDTree() {
        head = null;
    }

    public void add(Point2d point) {
        add(point, head, true);
    }

    private boolean add(Point2d point2d, Point2d node, boolean isXComparable) {
        if (size == 0 && node == head && head == null) {
            head = point2d;
            size++;
        } else if (isXComparable && point2d.getX() < node.getX()) {
            if (node.left == null) {
                node.left = point2d;
                size++;
            } else add(point2d, node.left, false);
        } else if (isXComparable) {
            if (node.right == null) {
                node.right = point2d;
                size++;
            } else add(point2d, node.right, false);

        } else if (!isXComparable && point2d.getY() < node.getY()) {
            if (node.left == null) {
                node.left = point2d;
                size++;
            } else add(point2d, node.left, true);

        } else if (!isXComparable) {
            if (node.right == null) {
                node.right = point2d;
                size++;
            } else add(point2d, node.right, true);
        }
        return true;
    }


    public void printTree() {
        System.out.println(toString());
    }

    public String toString() {
        StringBuilder builder = new StringBuilder(50);
        head.print(builder, "", "");

        return builder.toString();
    }


    public boolean contains(Point2d point) {
        if (size > 0)
            return head.contains(point, true);
        return false;
    }

    public LinkedList<Point2d> search() {
        LinkedList<Point2d> list = new LinkedList<>();
        search(list, head);
        return list;
    }

    private void search(LinkedList<Point2d> list, Point2d node) {
        if (node.left != null) search(list, node.left);
        if (node.right != null) search(list, node.right);
        list.add(node);
    }

    public List<Point2d> searchInside(Point2d point2d, Point2d d) {

        return Arrays.asList(null, null);
    }

    public List<Point2d> searchAboveTo(int bottomBorder) {

        return Arrays.asList(null, null);
    }

    public LinkedList<Point2d> searchNearestNeighbor(Point2d point) {
        Point2d minPoint = head;
        Double minLength = Double.MAX_VALUE;
        LinkedList<Point2d> minElementsList = new LinkedList<>();
        // like "dfs" searching aproximate value where searching point may be in
        // 2dtree and finding min length simultaneously
        minLength = findApproximateNearestPoint(head, point, minLength, minElementsList);
        //search new min points that can be less than previous value
        searchNN(head, point, minLength, minElementsList);
        return minElementsList;
    }

    private double findApproximateNearestPoint(Point2d node, Point2d lookForClosestEl, double minLength,
                                               LinkedList<Point2d> minElementsList) {
        Point2d currentNode = node;
        double currentLength = 0;
        for (int depth = 1; node != null; depth++) {
            for (int i = 0; i < 2; i++) {
                if (i == 0) currentNode = node.left;
                else currentNode = node.right;

                if (node.left == null || node.right == null) continue;
                currentLength = currentNode.distanceSquaredTo(lookForClosestEl);
                if (minLength > currentLength) {

                    minLength = currentLength;
                    minElementsList.clear();
                    minElementsList.add(currentNode);
                } else if (minLength == currentLength) {
                    minElementsList.add(currentNode);
                }
                if (currentNode.equal(lookForClosestEl)) {
                    minLength = 1.0;
                    return minLength;
                }
            }

            if ((depth & 1) == 0 && lookForClosestEl.getX() < node.getX()) {
                node = node.left;
            } else if ((depth & 1) == 0) {
                node = node.right;
            } else if ((depth & 1) == 1 && lookForClosestEl.getY() < node.getY()) {
                node = node.left;
            } else if ((depth & 1) == 1) {
                node = node.right;
            }
        }
        return minLength;
    }

    private void searchNN(Point2d currentNode, Point2d lookForClosestEl, Double minLength,
                          LinkedList<Point2d> minElementsList) {
        if (currentNode != null) {

            double currentLength = currentNode.distanceSquaredTo(lookForClosestEl);
            if (currentLength < minLength) {
                minLength = currentLength;
                minElementsList.clear();
                minElementsList.add(currentNode);
            } else if (currentLength == minLength) {
                if (!minElementsList.contains(currentNode))
                    minElementsList.add(currentNode);
            }
            searchNN(currentNode.left, lookForClosestEl, minLength, minElementsList);
            searchNN(currentNode.right, lookForClosestEl, minLength, minElementsList);
        }
    }
}
