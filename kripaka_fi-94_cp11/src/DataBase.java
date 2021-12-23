import java.util.HashMap;

public class DataBase {

    private HashMap<String, KDTree> treeMap;

    public DataBase() {
        treeMap = new HashMap<>();
        System.out.println("Database created");
    }

    public boolean create(String dbName) {
        treeMap.put(dbName, new KDTree());
        System.out.println("CREATED table " + dbName + " with " + " columns");
        return true;
    }

    public boolean insert(String dbName, int[] point) {
        if(!treeMap.isEmpty() && treeMap.containsKey(dbName)){
            Point2d newPoint = new Point2d(point[0], point[1]);
            treeMap.get(dbName).add(newPoint);
            System.out.println("Point2d " + newPoint.toString() + " has been added to " + dbName);
            return true;
        }
        System.out.println("There are no such database name as " + dbName);
        return false;
    }

    public boolean contains(String dbName, int[] point) {
        if(!treeMap.isEmpty() && treeMap.containsKey(dbName)) {
            boolean queryResult = treeMap.get(dbName).contains(new Point2d(point[0], point[1]));
            System.out.println("CONTAINS: " + queryResult);
            return queryResult;
        }
        System.out.println("There are no such database name as " + dbName);
        return false;
    }

    public boolean search(String dbName) {
        if(!treeMap.isEmpty() && treeMap.containsKey(dbName)) {
            System.out.println("SEARCH: \n" + treeMap.get(dbName).search());
            return true;
        }
        System.out.println("There are no such database name as " + dbName);
        return false;
    }

    public boolean printTree(String dbName) {
        if(!treeMap.isEmpty() && treeMap.containsKey(dbName)) {
            treeMap.get(dbName).printTree();
            return true;
        }
        System.out.println("There are no such database name as " + dbName);
        return false;
    }

    public boolean searchAboveTo(String dbName, int bottomBorder) {
        if(!treeMap.isEmpty() && treeMap.containsKey(dbName)) {
            treeMap.get(dbName).searchAboveTo(bottomBorder);
            return true;
        }
        System.out.println("There are no such database name as " + dbName);
        return false;
    }

    public boolean searchNN(String dbName, int[] point) {
        if(!treeMap.isEmpty() && treeMap.containsKey(dbName)) {
            System.out.println("SEARCH NN: "+treeMap.get(dbName).searchNearestNeighbor(new Point2d(point[0], point[1])));
            return true;
        }
        System.out.println("There are no such database name as " + dbName);
        return false;
    }

    public boolean searchInside(String dbName, int[] point1, int[] point2) {
        if(!treeMap.isEmpty() && treeMap.containsKey(dbName)) {
            treeMap.get(dbName).searchInside(new Point2d(point1[0], point1[1]), new Point2d(point2[0], point2[1]));
            return true;
        }
        System.out.println("There are no such database name as " + dbName);
        return false;
    }

    public boolean isDBEmpty(){
        return treeMap.keySet().isEmpty();
    }
}
