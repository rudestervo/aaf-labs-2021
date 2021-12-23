import java.util.StringTokenizer;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Parser {
    private static final Pattern INFO_INSIDE_BRACKETS = Pattern.compile("\\(([^{}()]*)\\)");
    private static final Pattern CREATE = Pattern.compile("(?i)create");
    private static final Pattern ONLY_WORDS = Pattern.compile("\\w*[^ +\\-:%@!#\"*\\\\(),;]");
    private static final Pattern INSERT = Pattern.compile("(?i)insert");
    private static final Pattern CONTAINS = Pattern.compile("(?i)contains");
    private static final Pattern SEARCH = Pattern.compile("(?i)search");
    private static final Pattern WHERE = Pattern.compile("(?i)where");
    private static final Pattern INSIDE = Pattern.compile("(?i)inside");
    private static final Pattern NN = Pattern.compile("(?i)nn");
    private static final Pattern ABOVE_TO = Pattern.compile("(?i)above_to");
    private static final Pattern NUMBER = Pattern.compile("( )*(-|)([0-9])+( )*");
    private static final Pattern PRINT_TREE = Pattern.compile("(?i)(print)_(?i)(tree)");
    private static final Pattern CREATECOM = Pattern.compile("(?i)create( )+(\\w|(_))+( )*");
    private static final Pattern INSERTCOM = Pattern.compile("(?i)insert( )+(\\w|(_))+( )*" +
            "\\(( )*(-|)[0-9]+( )*,( )*(-|)([0-9])+( )*\\)( )*");
    private static final Pattern SEARCHCOM = Pattern.compile("(?i)search( )+(\\w|(_))+( )*");
    private static final Pattern SEARCHWHERECOM = Pattern.compile("(?i)search( )+(\\w|(_))+(( )+" +
            "((?i)(where)( )*" +
            "(((?i)inside( )+\\(( )*(-|)([0-9])+( )*,( )*(-|)([0-9])+( )*\\)( )*,( )+\\(( )*(-|)([0-9])+( )*,( )*(-|)([0-9])+( )*\\)(  )*)" +
            "|((?i)above_to( )+(-|)([0-9])+( )*)" +
            "|((?i)nn( )+(\\(( )*(-|)([0-9])+( )*,( )*(-|)([0-9])+( )*\\)( )*)))))");
    private static final Pattern CONTAINSCOM = Pattern.compile("(?i)contains( )+(\\w|(_))+" +
            "( )*\\(( )*(-|)([0-9])+( )*,( )*(-|)([0-9])+( )*\\)( )*");
    private static final Pattern PRINT_TREECOM = Pattern.compile("(?i)(print)_(?i)(tree)( )+(\\w|(_))+(| )*");


    private String[][] parsedCommands;


    public boolean parse(String line) {
        try {
            StringTokenizer tokenizer = new StringTokenizer(line, ";", false);
            Matcher match;
            parsedCommands = new String[tokenizer.countTokens()][];
            for (int i = 0; tokenizer.hasMoreTokens(); i++) {
                String token = tokenizer.nextToken();

                if (CREATE.matcher(String.valueOf(token)).find()) {
                    if (!CREATECOM.matcher(String.valueOf(token)).matches()) {
                        return false;
                    }

                    parsedCommands[i] = new String[2];
                    match = ONLY_WORDS.matcher(token);
                    if (!match.find() || !CREATE.matcher(match.group()).matches()) {
                        return false;
                    }
                    parsedCommands[i][0] = match.group().toUpperCase();

                    if (!match.find()) {
                        return false;
                    }
                    parsedCommands[i][1] = match.group();

                    if (match.find() && !match.hitEnd()) {
                        return false;
                    }

                } else if (PRINT_TREE.matcher((String.valueOf(token))).find()) {
                    if (!PRINT_TREECOM.matcher(String.valueOf(token)).matches()) {
                        return false;
                    }

                    parsedCommands[i] = new String[2];
                    match = ONLY_WORDS.matcher(token);
                    if (!match.find() || !PRINT_TREE.matcher(match.group()).matches()) {
                        return false;
                    }
                    parsedCommands[i][0] = match.group().toUpperCase();

                    if (!match.find()) {
                        return false;
                    }
                    parsedCommands[i][1] = match.group();

                    if (match.find() && !match.hitEnd()) {
                        return false;
                    }

                } else if (INSERT.matcher(String.valueOf(token)).find()) {
                    if (!INSERTCOM.matcher(String.valueOf(token)).find()) {
                        return false;
                    }

                    parsedCommands[i] = new String[4];
                    match = ONLY_WORDS.matcher(token);

                    if (!match.find() || !INSERT.matcher(match.group()).matches()) {
                        return false;
                    }
                    parsedCommands[i][0] = match.group().toUpperCase();

                    if (!match.find()) {
                        return false;
                    }
                    parsedCommands[i][1] = match.group();

                    String[] point = token.substring(match.end()).replaceAll("(\\(|\\)| )", "").split(",");

                    if(!NUMBER.matcher(point[0]).matches() || !NUMBER.matcher(point[1]).matches()){
                        return false;
                    }
                    parsedCommands[i][2] = point[0];
                    parsedCommands[i][3] = point[1];

                } else if (CONTAINS.matcher(String.valueOf(token)).find()) {
                    if (!CONTAINSCOM.matcher(String.valueOf(token)).find()) {
                        return false;
                    }

                    parsedCommands[i] = new String[4];
                    match = ONLY_WORDS.matcher(token);

                    if (!match.find() || !CONTAINS.matcher(match.group()).matches()) {
                        return false;
                    }
                    parsedCommands[i][0] = match.group().toUpperCase();

                    if (!match.find()) {
                        return false;
                    }
                    parsedCommands[i][1] = match.group();

                    String[] point = token.substring(match.end()).replaceAll("(\\(|\\)| )", "").split(",");

                    if(!NUMBER.matcher(point[0]).matches() || !NUMBER.matcher(point[1]).matches()){
                        return false;
                    }
                    parsedCommands[i][2] = point[0];
                    parsedCommands[i][3] = point[1];

                } else if (SEARCH.matcher(String.valueOf(token)).find()) {
                    if (!SEARCHWHERECOM.matcher(String.valueOf(token)).find()
                            && !SEARCHCOM.matcher(String.valueOf(token)).find()) {
                        return false;
                    }

                    if (WHERE.matcher(String.valueOf(token)).find()) {
                        if (INSIDE.matcher(String.valueOf(token)).find()) {
                            parsedCommands[i] = new String[8];

                            match = ONLY_WORDS.matcher(token);
                            if (!match.find() || !SEARCH.matcher(match.group()).matches()) {
                                return false;
                            }
                            parsedCommands[i][0] = match.group().toUpperCase();

                            if (!match.find()) {
                                return false;
                            }
                            parsedCommands[i][1] = match.group();

                            if (!match.find() || !WHERE.matcher(match.group()).matches()) {
                                return false;
                            }
                            parsedCommands[i][2] = match.group().toUpperCase();

                            if (!match.find() || !INSIDE.matcher(match.group()).matches()) {
                                return false;
                            }
                            parsedCommands[i][3] = match.group().toUpperCase();

                            match = INFO_INSIDE_BRACKETS.matcher(token);
                            if (!match.find()) {
                                return false;
                            }
                            String[] point1 = match.group().replaceAll("(\\(|\\)| )", "").split(",");
                            if(!NUMBER.matcher(point1[0]).matches() || !NUMBER.matcher(point1[1]).matches()){
                                return false;
                            }
                            parsedCommands[i][4] = point1[0];
                            parsedCommands[i][5] = point1[1];

                            if (!match.find()) {
                                return false;
                            }
                            String[] point2 = match.group().replaceAll("(\\(|\\)| )", "").split(",");
                            if(!NUMBER.matcher(point2[0]).matches() || !NUMBER.matcher(point2[1]).matches()){
                                return false;
                            }

                            parsedCommands[i][6] = point2[0];
                            parsedCommands[i][7] = point2[1];

                            if (match.find() && !match.hitEnd()) {
                                return false;
                            }

                        } else if (NN.matcher(String.valueOf(token)).find()) {
                            parsedCommands[i] = new String[6];

                            match = ONLY_WORDS.matcher(token);
                            if (!match.find() || !SEARCH.matcher(match.group()).matches()) {
                                return false;
                            }
                            parsedCommands[i][0] = match.group().toUpperCase();

                            if (!match.find()) {
                                return false;
                            }
                            parsedCommands[i][1] = match.group();

                            if (!match.find() || !WHERE.matcher(match.group()).matches()) {
                                return false;
                            }
                            parsedCommands[i][2] = match.group().toUpperCase();

                            if (!match.find() || !NN.matcher(match.group()).matches()) {
                                return false;
                            }
                            parsedCommands[i][3] = match.group().toUpperCase();

                            String[] point = token.substring(match.end()).replaceAll("(\\(|\\)| )", "").split(",");

                            if(!NUMBER.matcher(point[0]).matches() || !NUMBER.matcher(point[1]).matches()){
                                return false;
                            }
                            parsedCommands[i][4] = point[0];
                            parsedCommands[i][5] = point[1];

                        } else if (ABOVE_TO.matcher(String.valueOf(token)).find()) {
                            parsedCommands[i] = new String[5];

                            match = ONLY_WORDS.matcher(token);
                            if (!match.find() || !SEARCH.matcher(match.group()).matches()) {
                                return false;
                            }
                            parsedCommands[i][0] = match.group().toUpperCase();

                            if (!match.find()) {
                                return false;
                            }
                            parsedCommands[i][1] = match.group();

                            if (!match.find() || !WHERE.matcher(match.group()).matches()) {
                                return false;
                            }
                            parsedCommands[i][2] = match.group().toUpperCase();

                            if (!match.find() || !ABOVE_TO.matcher(match.group()).matches()) {
                                return false;
                            }
                            parsedCommands[i][3] = match.group().toUpperCase();


                            String point = token.substring(match.end());

                            if (!NUMBER.matcher(point).matches()) {
                                return false;
                            }
                            parsedCommands[i][4] = point.replaceAll("( )", "");
                        }
                    } else {
                        parsedCommands[i] = new String[2];
                        match = ONLY_WORDS.matcher(token);
                        if (!match.find() || !SEARCH.matcher(match.group()).matches()) {
                            return false;
                        }
                        parsedCommands[i][0] = match.group().toUpperCase();

                        if (!match.find()) {
                            return false;
                        }
                        parsedCommands[i][1] = match.group();

                        if (match.find() && !match.hitEnd()) {
                            return false;
                        }
                    }
                } else {
                    return false;
                }
            }
        } catch (Exception e) {
            System.out.println(e.getCause() + e.getMessage());
        }

        return true;
    }

    public String[][] getArgs() {
        return parsedCommands;
    }
}
