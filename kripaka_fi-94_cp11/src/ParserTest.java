import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

import java.util.Arrays;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class ParserTest {
    Parser parser = new Parser();

    @Test
    void OneCommand(){
        System.out.println(parser.parse("CREATE cats ;"));
//        Assertions.assertEquals("[[CREATE, cats]]",Arrays.deepToString(parser.getArgs()));
        System.out.println(Arrays.deepToString(parser.getArgs()));

       System.out.println(parser.parse("SeArChH cities;"));
//        Assertions.assertEquals("[[null, null]]",Arrays.deepToString(parser.getArgs()));
        System.out.println(Arrays.deepToString(parser.getArgs()));

       System.out.println(parser.parse("search cities where nn ( 3 , 3 );"));
//        Assertions.assertEquals("[[SEARCH, cities, WHERE, NN, 3, 3]]",Arrays.deepToString(parser.getArgs()));
        System.out.println(Arrays.deepToString(parser.getArgs()));

       System.out.println(parser.parse("SEARCH cities WHERE NN (  379  ,   547  );"));
//        Assertions.assertEquals("[[SEARCH, cities, WHERE, NN, 379, 547]]",Arrays.deepToString(parser.getArgs()));
        System.out.println(Arrays.deepToString(parser.getArgs()));

       System.out.println(parser.parse("iNSERT cities (4, 1);"));
//        Assertions.assertEquals("[[INSERT, cities, 4, 1]]",Arrays.deepToString(parser.getArgs()));
        System.out.println(Arrays.deepToString(parser.getArgs()));

       System.out.println(parser.parse("CONTAINS cities (2, 8);"));
//        Assertions.assertEquals("[[CONTAINS, cities, 2, 8]]",Arrays.deepToString(parser.getArgs()));
        System.out.println(Arrays.deepToString(parser.getArgs()));

       System.out.println(parser.parse("SEARCH cities WHERE LEFT_of 9;"));
//        Assertions.assertEquals("[[SEARCH, cities, WHERE, LEFT_OF, 9]]",Arrays.deepToString(parser.getArgs()));
        System.out.println(Arrays.deepToString(parser.getArgs()));

       System.out.println(parser.parse("SEARCH cities WHERE INSIDE (5, 5), (6,6);"));
//        Assertions.assertEquals("[[SEARCH, cities, WHERE, INSIDE, 5, 5, 6, 6]]",Arrays.deepToString(parser.getArgs()));
        System.out.println(Arrays.deepToString(parser.getArgs()));
    }

    @Test
    void TwoAndMoreCommands(){
       System.out.println(parser.parse("SEARCH cities WHERE INSIDE (0, 0), (3, 5);"));
       System.out.println(parser.parse("CREATE new_table; INSERT set_name (8, 8); CONTAINS set_name (9, 1);"));
    }
}
