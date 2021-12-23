import java.math.BigInteger;
import java.util.ArrayList;
import java.util.Scanner;

public class Main {
    public static String C1 = "[cC][rR][eE][aA][tT][eE]";
    public static String C2 = "[iI][nN][sS][eE][rR][tT]";
    public static String C3 = "[pP][rR][iI][nN][tT][_][tT][rR][eE][eE]";
    public static String C4 = "[cC][oO][nN][tT][aA][iI][nN][sS]";
    public static String C5 = "[sS][eE][aA][rR][cC][hH]";
    public static String C51 = "[cC][oO][nN][tT][aA][iI][nN][eE][dD][_][bB][yY]";
    public static String C52 = "[iI][nN][tT][eE][rR][sS][eE][cC][tT][sS]";
    public static String C53 = "[rR][iI][gG][hH][tT][_][oO][fF]";
    public static String C6 = "[wW][hH][eE][rR][eE]";
    public static void main(String []args){
        ArrayList<Base> base = new ArrayList<Base>();
        String res="";
        Scanner in = new Scanner(System.in);
        while(true){
            System.out.println("");
            System.out.println("Enter line:");
            String sRead = res;
            sRead+=in.nextLine();
            sRead+=" ";
            String []sarr = sRead.split(";");
            res = sarr[sarr.length-1];
            for(int i=0;i<sarr.length-1;i++){
                Comand c = ParseCommand(sarr[i]);
                if(c.comNumber==0){
                    return;
                }
                if(!c.error){
                ExecuteCommand(base,c);}
                if(c.error){
                    System.out.println("In expression: \""+sarr[i]+";\""+" Error: "+c.name);
                }
            }
        }

    }
    public static Comand ParseCommand(String s1){
        Comand ret= new Comand();
        //ret.comNumber=-1;
        s1 = s1.trim();
        s1 = s1.replace("\s","\s");
        s1= s1.replace("\n","\s");
        s1 = s1.replace("\r","\s");
        s1 = s1.replace(";","");

        s1 = s1.replaceAll("( )+"," ");

        s1 = s1.replace(", ",",");
        s1 = s1.replace(" ,",",");
        s1 = s1.replace("[ ","[");
        s1 = s1.replace(" ]","]");

        String []str = s1.split(" ");
        if(s1.matches("[.][eE][Xx][Ii][Tt]")){
            ret.error=true;
            ret.comNumber=0;
            return ret;
        }
        if(str.length!=2&&str.length!=3&&str.length!=5){
            ret.error=true;
            ret.name = "is not a command!";
            return ret;
        }
        else if(str.length==2){
            // create ghj;
            if(str[0].matches(C1)){
                if(str[1].matches("[a-zA-Z][a-zA-Z0-9_]*")){
                    ret.comNumber=1;
                    ret.name=str[1];
                }else{
                    ret.error=true;
                    ret.name="bad name!";
                }
                return ret;
            }
            if(str[0].matches(C3)){
                if(str[1].matches("[a-zA-Z][a-zA-Z0-9_]*")){
                    ret.comNumber=3;
                    ret.name=str[1];
                }else{
                    ret.error=true;
                    ret.name="bad name!";
                }
                return ret;
            }
            if(str[0].matches(C5)){
                if(str[1].matches("[a-zA-Z][a-zA-Z0-9_]*")){
                    ret.comNumber=50;
                    ret.name=str[1];
                }else{
                    ret.error=true;
                    ret.name="bad name!";
                }
                return ret;
            }
            else{
                ret.error=true;
                ret.name= "unknown command!";
                return ret;
            }
        }

        else if(str.length==3){
            if(str[2].matches("[\\[][-]?[0-9]*[,][-]?[0-9]*[\\]]")){
                String s = str[2].replace("[","");
                s = s.replace("]","");
                String []as = s.split(",");
                if(!as[0].matches("[0]|[-]?[1-9][0-9]*")||!as[1].matches("[0]|[-]?[1-9][0-9]*")){
                    ret.error=true;
                    ret.name="bad argument values!";
                    return ret;
                }
                BigInteger a =new BigInteger( as[0]);
                BigInteger b =new BigInteger(as[1]);
                if(a.compareTo(b)==1){
                    ret.error=true;
                    ret.name="left bound greater than right!";
                    return ret;
                }
                ret.argName=s;
                //return ret;
            }

            else{
                ret.error=true;
                ret.name="bad argument!";
                return ret;
            }
            if(str[0].matches(C2)){
                if(str[1].matches("[a-zA-Z][a-zA-Z0-9_]*")){
                    ret.comNumber=2;
                    ret.name=str[1];

                }else{
                    ret.error=true;
                    ret.name="bad name!";
                    return ret;
                }
                return ret;
            }
            if(str[0].matches(C4)){
                if(str[1].matches("[a-zA-Z][a-zA-Z0-9_]*")){
                    ret.comNumber=4;
                    ret.name=str[1];
                }else{
                    ret.error=true;
                    ret.name="bad name!";
                    return ret;
                }
                return ret;
            }
            else{
                ret.error=true;
                ret.name= "unknown command!";
                return ret;
            }
        }
        else if(str.length==5){
            if(str[4].matches("[\\[][-]?[0-9]*[,][-]?[0-9]*[\\]]")){
                String s = str[4].replace("[","");
                s = s.replace("]","");
                String []as = s.split(",");
                if(!as[0].matches("[0]|[-]?[1-9][0-9]*")||!as[1].matches("[0]|[-]?[1-9][0-9]*")){
                    ret.error=true;
                    ret.name="bad argument values!";
                    return ret;
                }
                int a =Integer.parseInt( as[0]);
                int b = Integer.parseInt(as[1]);
                if(a>b){
                    ret.error=true;
                    ret.name="left bound greater than right!";
                    return ret;
                }
                ret.argName=s;
                //return ret;

            }
            else if(str[4].matches("[0]|[-]?[1-9][0-9]*")){
                if(str[3].matches(C53)){
                    ret.comNumber=53;

                    ret.argName=str[4];
                    if(str[1].matches("[a-zA-Z][a-zA-Z0-9_]*")){
                        ret.name=str[1];
                    }else{
                        ret.error=true;
                        ret.name= "bad name!";
                        return ret;
                    }
                    return ret;
                }
                else {
                    ret.error=true;
                    ret.name= "unknown command!";
                    return ret;
                }
            }
            else{
                ret.error=true;
                ret.name="bad argument!";
                return ret;
            }
            if(str[0].matches(C5)){
                if(str[2].matches(C6))
                {
                    if(str[1].matches("[a-zA-Z][a-zA-Z0-9_]*")){
                        ret.name=str[1];
                    }else{
                        ret.error=true;
                        ret.name= "bad name!";
                        return ret;
                    }
                    if(str[3].matches(C51)){
                        ret.comNumber=51;

                    }
                    else if(str[3].matches(C52)){
                        ret.comNumber=52;

                    }
                    //else if(str[3].matches(C53)){
                      //  ret.comNumber=53;

                    //}
                }
                return ret;
            }
            ret.error=true;
            ret.name= "unknown command!";
            return ret;
        }
        else{
            ret.error=true;
            ret.name="unknown command!";
            return ret;
        }
        //return ret;

    }

    public static void ExecuteCommand(ArrayList<Base> lst,Comand comand){

        if(comand.comNumber==1){

            for(int i=0;i<lst.toArray().length;i++){

                if(comand.name.equals(lst.get(i).s1)){
                    System.out.println(comand.name+" already exist!");
                    return;
                }
            }
            KDTree tr = new KDTree();
            tr.node=null;
            Base b = new Base();
            b.tree=tr;
            b.s1=comand.name;
            lst.add(b);
            System.out.println(b.s1+" successfully created!");
            return;
        }
        if(comand.comNumber==2){
            int check=-1;
            for(int i=0;i<lst.toArray().length;i++){
                if(comand.name.equals(lst.get(i).s1)){
                    check=i;
                }
            }
            if(check==-1){
                System.out.println(comand.name+" does not exist!");
                return;
            }
            AddSection(lst.get(check).tree,comand.argName);
            System.out.println("["+comand.argName+"]"+" added to "+lst.get(check).s1+"!");

        }
        if(comand.comNumber==3||comand.comNumber==50){
            int check=-1;
            for(int i=0;i<lst.toArray().length;i++){
                if(comand.name.equals(lst.get(i).s1)){
                    check=i;
                }
            }
            if(check==-1){
                System.out.println(comand.name+" does not exist!");
                return;
            }
            PrintTree(lst.get(check).tree,0,0);
            System.out.println("");
        }
        if(comand.comNumber==4){
            int check=-1;
            for(int i=0;i<lst.toArray().length;i++){
                if(comand.name.equals(lst.get(i).s1)){
                    check=i;
                }
            }
            if(check==-1){
                System.out.println(comand.name+" does not exist!");
                return;
            }
            boolean cont=false;
            System.out.println("In "+comand.name+" contains section ["+comand.argName+"]");
            cont =Contains(lst.get(check).tree,comand.argName,cont);
            System.out.println(cont);
        }
        if(comand.comNumber==51){
            int check=-1;
            for(int i=0;i<lst.toArray().length;i++){
                if(comand.name.equals(lst.get(i).s1)){
                    check=i;
                }
            }
            if(check==-1){
                System.out.println(comand.name+" does not exist!");
                return;
            }

            System.out.println("In "+comand.name+" contains in boundaries ["+comand.argName+"] next sections:");
            ContainBy(lst.get(check).tree,comand.argName);

        }
        if(comand.comNumber==52){
            int check=-1;
            for(int i=0;i<lst.toArray().length;i++){
                if(comand.name.equals(lst.get(i).s1)){
                    check=i;
                }
            }
            if(check==-1){
                System.out.println(comand.name+" does not exist!");
                return;
            }

            System.out.println("In "+comand.name+" contains intersected with ["+comand.argName+"] next sections:");
            ContainIntersect(lst.get(check).tree,comand.argName);

        }
        if(comand.comNumber==53){
            int check=-1;
            for(int i=0;i<lst.toArray().length;i++){
                if(comand.name.equals(lst.get(i).s1)){
                    check=i;
                }
            }
            if(check==-1){
                System.out.println(comand.name+" does not exist!");
                return;
            }

            System.out.println("In "+comand.name+" contains further right then "+comand.argName+" next sections:");
            ContainRight(lst.get(check).tree,comand.argName);

        }
    }
    public static void AddSection(KDTree tree,String bnds){
        BigInteger l = new BigInteger( (bnds.split(",")[0]));
        BigInteger r = new BigInteger(bnds.split(",")[1]);
        KDNode node = new KDNode();
        node.bLeft=l;
        node.bRight=r;
        if(tree.node==null){
            tree.node=node;
            return;
        }else{
            if(tree.node.bLeft.compareTo(l)==1){
                if(tree.left==null){
                    tree.left=new KDTree();
                }
                AddSection(tree.left,bnds);
            }
            else{
                if(tree.right==null){
                    tree.right=new KDTree();
                }
                AddSection(tree.right,bnds);
            }
        }
    }

    public static void PrintTree(KDTree tree,int i,int end){

        if(i!=0) {
            System.out.println("");

            for (int j = 0; j < i; j++) {
                System.out.print(" ");
            }
            if(end==1) System.out.print("\u2514");
            if(end==0) System.out.print("\u251C");
            System.out.print("\u2500");
            System.out.print("[" + tree.node.bLeft + "," + tree.node.bRight + "]");
        }else{
            System.out.print("[" + tree.node.bLeft + "," + tree.node.bRight + "]");
        }
        if(tree.left!=null){
            PrintTree(tree.left,i+1,0);// end = 1 to produce more accurate view, but left-right can be unrecognized;
        }
        if(tree.right!=null){
            PrintTree(tree.right,i+1,1);
        }

    }
    public static boolean Contains(KDTree tree,String bnds,boolean c){
        BigInteger l = new BigInteger(bnds.split(",")[0]);
        BigInteger r = new BigInteger(bnds.split(",")[1]);
        if(tree.node.bLeft.compareTo(l)==1){
            if(tree.left!=null){
               c = Contains(tree.left,bnds,c);
            }
            return c;
        }
        if(tree.node.bLeft.compareTo(l)==-1){
            if(tree.right!=null){
                c = Contains(tree.right,bnds,c);
            }
            return c;
        }
        if(tree.node.bLeft.compareTo(l)==0){
            if(tree.node.bRight.compareTo(r)==0){
                c = true;
                return c;
            }
            if(tree.right!=null){
              c = Contains(tree.right,bnds,c);
            }
            return c;
        }
        return c;
    }
    public  static void ContainBy(KDTree tree, String bnds){
        BigInteger l = new BigInteger(bnds.split(",")[0]);
        BigInteger r = new BigInteger(bnds.split(",")[1]);
        if(tree.node.bLeft.compareTo(l)==-1){
            if(tree.right!=null){
                ContainBy(tree.right,bnds);
            }
            return;
        }

        if((tree.node.bLeft.compareTo(l)==0||tree.node.bLeft.compareTo(l)==1)
                &&(tree.node.bLeft.compareTo(r)==0||tree.node.bLeft.compareTo(r)==-1)){
            if(tree.node.bRight.compareTo(r)==0||tree.node.bRight.compareTo(r)==-1){
                System.out.println("["+tree.node.bLeft+","+tree.node.bRight+"]");
            }
            if(tree.right!=null){
                ContainBy(tree.right,bnds);
            }
            if(tree.left!=null){
                ContainBy(tree.left,bnds);
            }
        }
        else{
            if(tree.left!=null){
                ContainBy(tree.left,bnds);
            }
        }
        return;
    }
    public  static  void ContainIntersect(KDTree tree,String bnds){

        BigInteger l= new BigInteger(bnds.split(",")[0]);
        BigInteger r = new BigInteger(bnds.split(",")[1]);
        if(tree.node.bLeft.compareTo(r)==1){
            if(tree.left!=null){
                ContainIntersect(tree.left,bnds);
            }
            return;
        }


        if(tree.node.bLeft.compareTo(r)==0||tree.node.bLeft.compareTo(r)==-1){
            if(((tree.node.bLeft.compareTo(l)==0||tree.node.bLeft.compareTo(l)==1)
                    &&(tree.node.bLeft.compareTo(r)==0||tree.node.bLeft.compareTo(r)==-1))
                    ||
                    ((tree.node.bRight.compareTo(l)==0||tree.node.bRight.compareTo(l)==1)
                    &&(tree.node.bRight.compareTo(r)==0||tree.node.bRight.compareTo(r)==-1))){
                System.out.println("["+tree.node.bLeft+","+tree.node.bRight+"]");
            }
            if(tree.left!=null){
                ContainIntersect(tree.left,bnds);
            }
            if(tree.right!=null){
                ContainIntersect(tree.right,bnds);
            }

        }
        else{
            if(tree.right!=null){
                ContainIntersect(tree.right,bnds);
            }
        }

    }
    public static void  ContainRight(KDTree tree,String bnds){
        BigInteger l = new BigInteger(bnds);

        if(tree.node.bLeft.compareTo(l)==1||tree.node.bLeft.compareTo(l)==0){
            System.out.println("["+tree.node.bLeft+","+tree.node.bRight+"]");
            if(tree.right!=null){
                ContainRight(tree.right,bnds);
            }
            if(tree.left!=null){
                ContainRight(tree.left,bnds);
            }
            return;
        }
        if(tree.node.bLeft.compareTo(l)==-1){
            if(tree.right!=null){
                ContainRight(tree.right,bnds);
            }
            return;
        }
    }

}
