import edu.princeton.cs.algs4.Point2D;
import edu.princeton.cs.algs4.RectHV;

import java.util.Arrays;
import java.util.Scanner;
import java.util.regex.Pattern;

public class Exec {

    final static Pattern EXIT = Pattern.compile("( )*(?i)exit( )*");

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Parser parser = new Parser();
        Switcher switcher = new Switcher();
        String str;
        DataBase db = new DataBase();

        while (true) {
            System.out.print(">> ");
            str = scanner.nextLine();
            if (EXIT.matcher(str).matches()) {
                break;
            }
            if (parser.parse(str)) {
                switcher.execCommand(parser.getArgs(), db);
            } else {
                System.out.println("incorrect input");
            }
        }

        scanner.close();
    }
}
