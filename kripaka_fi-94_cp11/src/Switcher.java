public class Switcher {

    public boolean execCommand(String[][] args, DataBase db) {
        for (int i = 0; i < args.length; i++) {
            if(args[i] == null)
                return false;
            switch (args[i][0]) {
                case "CREATE": {
                    db.create(args[i][1]);
                    break;
                }
                case "INSERT": {
                    if (!db.isDBEmpty())
                        db.insert(args[i][1], new int[]{Integer.parseInt(args[i][2]), Integer.parseInt(args[i][3])});
                    else System.out.println("DB is empty!");

                    break;
                }
                case "PRINT_TREE": {
                    if (!db.isDBEmpty())
                        db.printTree(args[i][1]);
                    else System.out.println("DB is empty!");

                    break;
                }
                case "CONTAINS": {
                    if (!db.isDBEmpty())
                        db.contains(args[i][1], new int[]{Integer.parseInt(args[i][2]), Integer.parseInt(args[i][3])});
                    else System.out.println("DB is empty!");

                    break;
                }
                case "SEARCH": {
                    if (!db.isDBEmpty()) {
                        switch (args[i].length) {
                            case 2 -> {
                                db.search(args[i][1]);
                            }
                            case 5 -> {
                                db.searchAboveTo(args[i][1], Integer.parseInt(args[i][4]));
                            }
                            case 6 -> {
                                db.searchNN(args[i][1], new int[]{Integer.parseInt(args[i][4]), Integer.parseInt(args[i][5])});
                            }
                            case 8 -> {
                                db.searchInside(args[i][1],
                                        new int[]{Integer.parseInt(args[i][4]), Integer.parseInt(args[i][5])},
                                        new int[]{Integer.parseInt(args[i][6]), Integer.parseInt(args[i][7])});
                            }
                        }
                        break;
                    } else {
                        System.out.println("DB is empty!");
                    }
                }
                default:
                    return false;
            }
        }

        return true;
    }
}
