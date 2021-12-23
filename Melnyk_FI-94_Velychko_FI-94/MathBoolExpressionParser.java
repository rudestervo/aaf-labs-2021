import java.util.Arrays;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;

public class MathBoolExpressionParser {
    final static String digitChars = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz01234567890_.";
    final static String symbolChars = "+-/*=<>&|!^()";

    final static List<String> operators1 = Arrays.asList("(", ")");
    final static List<String> operators2 = Arrays.asList("=", "<", ">", "<=", "=>", "!=", "&", "|", "^");
    final static List<String> operators3 = Arrays.asList("!");
    final static List<String> operators4 = Arrays.asList("+", "-");
    final static List<String> operators5 = Arrays.asList("/", "*");

    private final LinkedList<String> resultList = new LinkedList<>();
    private final Map<String, Object> mapVariables = new HashMap<>();
    private String strExpression;

    MathBoolExpressionParser(String strExpression) {
        this.strExpression = strExpression;
        parseToPolishNotation();
    }

    public boolean isVarUsed(String varName) {
        return resultList.contains(varName);
    }
    
    private static boolean isOperator(String token) {
        return (operators1.contains(token) ||
                operators2.contains(token) ||
                operators3.contains(token) ||
                operators4.contains(token) ||
                operators5.contains(token));
    }

    private static int priority(String token) {
        if (operators1.contains(token)) return 1;
        if (operators2.contains(token)) return 2;
        if (operators3.contains(token)) return 3;
        if (operators4.contains(token)) return 4;
        if (operators5.contains(token)) return 5;
        return 6;
    }

    public void setStringExpression(String strExpression) {
        if (strExpression == null || strExpression.isEmpty())
            return;
        this.strExpression = strExpression;
        parseToPolishNotation();
        mapVariables.clear();
    }

    public Object calculate() {
        if (resultList.isEmpty())
            parseToPolishNotation();
        return evaluatePolishNotation();
    }

    public void addNewVariable(String key, Object value) {
        if (key == null || key.isEmpty() || value == null)
            return;
        if (value instanceof Double)
            mapVariables.put(key, value);
        else if (value instanceof Number) {
            Double newVal = (double) ((Integer) value);
            mapVariables.put(key, newVal);
        } else
            mapVariables.put(key, value);
    }

    public void parseToPolishNotation() {
        LinkedList<String> queue = new LinkedList<>();
        LinkedList<String> tokenList = new LinkedList<>();
        resultList.clear();

        String expression = strExpression.replaceAll(" ", "");

        int start = 0;

        while (start < expression.length()) {
            if (expression.charAt(start) == ' ') {
                start++;
                continue;
            }
            if (digitChars.indexOf(expression.charAt(start)) > -1) {
                StringBuilder digitObj = new StringBuilder();
                while (start < expression.length() &&
                        digitChars.indexOf(expression.charAt(start)) > -1) {
                    digitObj.append(expression.charAt(start));
                    start++;
                }
                tokenList.add(digitObj.toString());
            } else if (symbolChars.indexOf(expression.charAt(start)) > -1) {
                StringBuilder symbolObj = new StringBuilder();
                while (start < expression.length() &&
                        symbolChars.indexOf(expression.charAt(start)) > -1) {
                    symbolObj.append(expression.charAt(start));
                    start++;
                }
                if (isOperator(symbolObj.toString())) {
                    tokenList.add(symbolObj.toString());
                } else {
                    int i0 = 0;
                    int i1 = 1;
                    while (i0 < symbolObj.length()) {
                        if (i1 < symbolObj.length() && isOperator(symbolObj.substring(i0, i1 + 1))) {
                            tokenList.add(symbolObj.substring(i0, i1 + 1));
                            i0 += 2;
                        } else {
                            tokenList.add(symbolObj.substring(i0, i1));
                            i0++;
                        }
                        i1 = i0 + 1;
                        i1 = Math.min(i1, symbolObj.length());
                    }
                }
            }
        }

        for (String token : tokenList) {
            if (isOperator(token)) {
                if (token.equals("(")) {
                    queue.addFirst(token);
                } else if (token.equals(")")) {
                    String item = queue.removeFirst();
                    while (!"(".equals(item)) {
                        resultList.addLast(item);
                        item = queue.removeFirst();
                    }
                } else {
                    while (!queue.isEmpty() &&
                            (priority(token) <= priority(queue.peek()))) {
                        resultList.add(queue.removeFirst());
                    }
                    queue.addFirst(token);
                }
            } else {
                resultList.add(token);
            }
        }

        while (!queue.isEmpty()) {
            resultList.add(queue.removeFirst());
        }
    }

    private static boolean isDouble(String strNum) {
        if (strNum == null) {
            return false;
        }
        try {
            double d = Double.parseDouble(strNum);
        } catch (NumberFormatException nfe) {
            return false;
        }
        return true;
    }

    public Object evaluatePolishNotation() {

        LinkedList<Object> queue = new LinkedList<>();
        Object result = 0.0;

        for (String token : resultList) {

            if (isOperator(token)) {
                Double valRight = 0.0;
                Double valLeft = 0.0;
                Boolean bRight = false;
                Boolean bLeft = false;
                Object oRight = null;
                Object oLeft = null;
                boolean bresult;

                switch (token) {
                    // "+", "-", "*", "/"
                    case "+":
                        valRight = (Double) queue.removeFirst();
                        valLeft = (Double) queue.removeFirst();
                        queue.addFirst(valLeft + valRight);
                        break;
                    case "-":
                        valRight = (Double) queue.removeFirst();
                        valLeft = (Double) queue.removeFirst();
                        queue.addFirst(valLeft - valRight);
                        break;
                    case "*":
                        valRight = (Double) queue.removeFirst();
                        valLeft = (Double) queue.removeFirst();
                        queue.addFirst(valLeft * valRight);
                        break;
                    case "/":
                        valRight = (Double) queue.removeFirst();
                        valLeft = (Double) queue.removeFirst();
                        queue.addFirst(valLeft / valRight);
                        break;
                    case "<":
                        valRight = (Double) queue.removeFirst();
                        valLeft = (Double) queue.removeFirst();
                        queue.addFirst(valLeft < valRight);
                        break;
                    case ">":
                        valRight = (Double) queue.removeFirst();
                        valLeft = (Double) queue.removeFirst();
                        queue.addFirst(valLeft > valRight);
                        break;
                    case "<=":
                        valRight = (Double) queue.removeFirst();
                        valLeft = (Double) queue.removeFirst();
                        queue.addFirst(valLeft <= valRight);
                        break;
                    case ">=":
                        valRight = (Double) queue.removeFirst();
                        valLeft = (Double) queue.removeFirst();
                        queue.addFirst(valLeft >= valRight);
                        break;
                    case "=":
                        oRight = queue.removeFirst();
                        oLeft = queue.removeFirst();
                        if (oRight instanceof Number && oLeft instanceof Number)
                            bresult = oLeft.equals(oRight);
                        else if (oRight instanceof Boolean && oLeft instanceof Boolean)
                            bresult = oLeft == oRight;
                        else
                            bresult = false;
                        queue.addFirst(bresult);
                        break;
                    case "!=":
                        oRight = queue.removeFirst();
                        oLeft = queue.removeFirst();
                        if (oRight instanceof Number && oLeft instanceof Number)
                            bresult = oLeft.equals(oRight);
                        else if (oRight instanceof Boolean && oLeft instanceof Boolean)
                            bresult = oLeft == oRight;
                        else
                            bresult = false;
                        queue.addFirst(!bresult);
                        break;

                    case "&":
                        bRight = (Boolean) queue.removeFirst();
                        bLeft = (Boolean) queue.removeFirst();
                        queue.addFirst(bLeft && bRight);
                        break;
                    case "|":
                        bRight = (Boolean) queue.removeFirst();
                        bLeft = (Boolean) queue.removeFirst();
                        queue.addFirst(bLeft || bRight);
                        break;
                    case "!":
                        bRight = (Boolean) queue.removeFirst();
                        queue.addFirst(!bRight);
                        break;
                }
            } else {
                if (isDouble(token)) {
                    queue.addFirst(Double.parseDouble(token));
                } else if (token.equalsIgnoreCase("true")) {
                    queue.addFirst(true);
                } else if (token.equalsIgnoreCase("false")) {
                    queue.addFirst(false);
                } else if (mapVariables.containsKey(token) && mapVariables.get(token) != null) {
                    queue.addFirst(mapVariables.get(token));
                } else {
                    throw new ArithmeticException(token);
                }
            }
        }
        if (queue.size() > 1)
            throw new ArithmeticException(queue.toString());
        return queue.removeFirst();
    }
}
