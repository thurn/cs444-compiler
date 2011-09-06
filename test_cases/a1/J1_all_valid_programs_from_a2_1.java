// PARSER_WEEDER
public class J1_char_escape3 {
    public J1_char_escape3() {}
    public static int test() {
	int r = 0;
	if (J1_char_escape3.eq("\\123", ((char)92+"123"))) r=r+1;
	if (J1_char_escape3.eq("\\12", ((char)92+"12"))) r=r+1;
	if (J1_char_escape3.eq("\\1", ((char)92+"1"))) r=r+1;
	if (J1_char_escape3.eq("\134123", ((char)92+"123"))) r=r+1;
	if (J1_char_escape3.eq("\13412", ((char)92+"12"))) r=r+1;
	if (J1_char_escape3.eq("\1341", ((char)92+"1"))) r=r+1;
	return r+117;
    }
    public static boolean eq(String a, String b) {return a.equals((Object)b);}
}
// PARSER_WEEDER,CODE_GENERATION
public class J1_charadd {
    public J1_charadd() {}
    public static int test() {
	String s = '2'+'4'+""+'2'+'4';
	//System.out.println(s);
	return Integer.parseInt(s) - 10101;
    }
}
// PARSER_WEEDER
public class J1_charliterals {
    public J1_charliterals() {}
    public static int test() {
	char c1 = 'a';
	char c2 = '7';
	return 123;
    }
}
// PARSER_WEEDER
public class J1_classinstance {

    public int foo;
    
    public J1_classinstance() {}
    
    public static int test() {
        (new J1_classinstance()).foo = 42;
	new J1_classinstance().foo = 42;
	return 123;
    }
 
}
// PARSER_WEEDER
public class J1_commentsInExp1 {

    public J1_commentsInExp1 () {}

    public static int test() {
	int a = - /* comments are funny */ 123;
        return -a; 
    }

}
// PARSER_WEEDER
public class J1_commentsInExp2 {

    public J1_commentsInExp2 () {}

    public static int test() {
        return /* fun with comments */123;
    }

}
// PARSER_WEEDER
public class J1_commentsInExp3 {

    public J1_commentsInExp3 () {}

    public static int test() {
        return 11 /* eleven */ * /* times */ 12 - 9;
    }

}
// PARSER_WEEDER
public class J1_commentsInExp4 {

    public J1_commentsInExp4 () {}

    public int // too many
		  foo() {
	return 123;
    }

    public static int test() {
	J1_commentsInExp4 j = /* comments */ new /* are */ J1_commentsInExp4();
        return j./* not enough! */foo();
    }

}
// PARSER_WEEDER
public class J1_commentsInExp5 {

    public J1_commentsInExp5 () {}

    public static int test() {
	String s = (String) /* String conversion */ "String";
        return 123;
    }

}
// PARSER_WEEDER
public class J1_commentsInExp6 {

    public J1_commentsInExp6 () {}

    public static int test() {
        return (120) /* Java rocks */ + 3;
    }

}
// PARSER_WEEDER
public class J1_commentsInExp7 {

    public J1_commentsInExp7 () {}

    public static int test() {
        return (126) /* Java rocks */ -3;
    }

}
// PARSER_WEEDER
public class J1_commentsInExp8 {

    public J1_commentsInExp8 () {}

    public static int test() {
	int aaaa = 120;
        return (aaaa) /* Java rocks */ +3;
    }

}
// PARSER_WEEDER
public class J1_commentsInExp9 {

    public J1_commentsInExp9 () {}

    public static int test() {
        return (126) /* Java rocks */ - /* foo */ 3;
    }

}
// PARSER_WEEDER
public class J1_comparisonoperations {
    public J1_comparisonoperations() {}
    public static int test() {
	int x = 51;
	boolean b = (x<87) && (x>42) && (x<=86) && (x>=43) && (x==51) && (x!=52);
	return 123;
    }
}

// PARSER_WEEDER,CODE_GENERATION
public class J1_concat_in_binop {
    public J1_concat_in_binop() {}
    public static int test() {
	String x = "";
	String y = ("Result: "+("abc"+x == null)); // "Result: false"
	return 110+y.length();
    }
}
// PARSER_WEEDER,HIERARCHY
public class J1_constructorWithSameNameAsMethod {

    public J1_constructorWithSameNameAsMethod () {}

    public int J1_constructorWithSameNameAsMethod () {
        return 123;
    }

    public static int test() {
        return new J1_constructorWithSameNameAsMethod().J1_constructorWithSameNameAsMethod();
    }

}
// PARSER_WEEDER,RESOURCES,CODE_GENERATION
public class J1_constructorbodycast {

    public int x;

    public J1_constructorbodycast () {
	String String = "Hello";
	for (int i=0; i<10; i=i+1) {
	    String = (String)+(String)"World";
	}
	this.x = String.length()+68;
    }

    public static int test() {
        return new J1_constructorbodycast().x;
    }

}
// PARSER_WEEDER
public class J1_constructorparameter {

    protected int i;

    public J1_constructorparameter(int i) {
	this.i = i;
    }

    public static int test() {
        return new J1_constructorparameter(123).i;
    }

}
// PARSER_WEEDER
public class J1_eagerbooleanoperations {
  public J1_eagerbooleanoperations() {}
  public static int test() {
      boolean x = false;
      boolean b = (x & true) | !x;
      return 123;
  }
}
// PARSER_WEEDER,TYPE_CHECKING
public class J1_evalMethodInvocationFromParExp {
    
    public J1_evalMethodInvocationFromParExp() {}

    public static int test() {
	return new Integer(("12"+"3").toString()).intValue();
    }
}
// PARSER_WEEDER
public class J1_exp {

    public J1_exp() {}

    public static int test() {
	return 123;
    }
}
// PARSER_WEEDER
public class J1_extends extends java.lang.Thread {

    public int y;

    public J1_extends() {}

    public static int test() {
	return 123;
    }
}

