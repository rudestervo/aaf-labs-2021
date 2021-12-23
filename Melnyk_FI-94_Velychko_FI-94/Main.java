import java.util.Scanner;
import java.util.regex.Pattern;

public class Main {

    private static final String Exit = "[ ]*[.](E|e)(X|x)(I|i)(T|t)*[ ]*";
    private static final Pattern patternExit = Pattern.compile(Exit);

    public static void main(String[] args) {


        // Auto test
        /*
        SqlParser.commandHandler("create cat (x INDEXED, y, z)");
        SqlParser.commandHandler("create cat (x, y, d, s)");

        SqlParser.commandHandler("insert into cat (1, 2, 3)");
        SqlParser.commandHandler("insert into cat (4, 5, 6)");
        SqlParser.commandHandler("insert into cat (7, 8, 9)");
        SqlParser.commandHandler("insert into cat (10, 11, 12)");

        SqlParser.commandHandler("select * from cat");
        SqlParser.commandHandler("select a, z, x from cat");
        SqlParser.commandHandler("select z, x from cat");

        SqlParser.commandHandler("select z, x from cat where (x > 5) & (y < 11)");

        SqlParser.commandHandler("delete from cat where (x > 5) & (y < 11)");
        SqlParser.commandHandler("select * from cat where x>3 ");
        SqlParser.commandHandler("select * from cat where (x = 4) ");
        SqlParser.commandHandler("delete cat where x=4");
        SqlParser.commandHandler("select * from cat");
        SqlParser.commandHandler("DELETE FROM cat");
        SqlParser.commandHandler("select * from cat");
        */


        System.out.println("Hello! Enter your command.If you want to finish enter .EXIT");

        Scanner scanner = new Scanner(System.in);
        boolean nextCommand = true;
        while (true) {
            System.out.print(" > ");
            StringBuilder command = new StringBuilder();
            while (command.toString().indexOf(";") == -1) {
                String name = scanner.nextLine();
                command.append(name);
                String fullCommand = command.substring(0, command.toString().indexOf(";"));
                if (patternExit.matcher(fullCommand).matches()) {
                    System.out.println("Current command is : " + command);
                    return;
                } else
                    SqlParser.commandHandler(fullCommand);
            }
        }
    }
}
