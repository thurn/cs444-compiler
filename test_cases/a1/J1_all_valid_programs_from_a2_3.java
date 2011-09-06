// PARSER_WEEDER
public class J1_externalcall {

    public J1_externalcall() {}
    
    public static int test() {
	return new java.util.Vector().size()+123;
    }

}
// PARSER_WEEDER
public final class J1_finalclass {

    public J1_finalclass() {}

    public static int test() {
	return 123;
    }

}
// PARSER_WEEDER
public final class J1_finalclass2 {
	public J1_finalclass2() { }
	public static int test() { return 123; }
}
// PARSER_WEEDER
public class J1_forAllwaysInit {

    public J1_forAllwaysInit () {}

    public int foo() {
	return 123;
    }

    public int bar() {
	int i = 0;
	for (i=foo(); i>123; i=i+1) {}
	return i;
    }

    public static int test() {
	J1_forAllwaysInit j = new J1_forAllwaysInit();
	return j.bar();
    }

}
// PARSER_WEEDER
public class  J1_forAlwaysInitAsWhile {

    public J1_forAlwaysInitAsWhile () {}

    public int foo() {
		return 123;
    }

    public int bar() {
		int i = 0;
		{
			i=foo();
			
				while(i>123) {
					{
							
					}
					i=i+1;
				}
			
		}
		return i;
    }

    public static int test() {
		J1_forAlwaysInitAsWhile j = new J1_forAlwaysInitAsWhile();
		
		return j.bar();
    }

}
// PARSER_WEEDER
public class J1_forMethodInit {

    public J1_forMethodInit () {}

    public int foo() {
	return 7;
    }

    public static int test() {
	J1_forMethodInit k = new J1_forMethodInit();
        int i = 1;
	int j = 1;
	for (k.foo();i<6;i=i+1) {
	    j = i * j;
	}
	return j + 3;
    }

    public static void main(String[] args) {
	J1_forMethodInit.test();
    }
}
// PARSER_WEEDER
public class J1_forMethodUpdate {

    public J1_forMethodUpdate () {}

    public int i;

    public int foo() {
	int j = 1;
	for (i=1; i<6; bar()) {
	    j = j * i;
	}
	return j+3;
    }

    public void bar() {
	i = i + 1;
    }

    public static int test() {
	J1_forMethodUpdate j = new J1_forMethodUpdate();
       	return j.foo();
    }

    public static void main(String[] args) {
	System.out.println(J1_forMethodUpdate.test());
    }
}
// PARSER_WEEDER
public class J1_forMethodUpdate2 {
	public J1_forMethodUpdate2() {}

	public static int test() {
		Integer foo = new Integer(5);
		for (int i=0; i < 1; foo.hashCode()) {
			if (i == 0) return 123;
		}
		return 0;
	}

	public static void main(String[] args) {
		System.out.println(J1_forMethodUpdate2.test());
	}
}
// PARSER_WEEDER
public class J1_forWithoutExp {

    public J1_forWithoutExp () {}

    public static int test() {
	int j = 1;
	for (int i=1; ; i=i+1) {
	    j = i * j;
	    if (i == 5)
		return j+3;
	}
    }

    public static void main(String[] args) {
	System.out.println(J1_forWithoutExp.test());
    }
}
// PARSER_WEEDER
public class J1_forWithoutInit {

    public J1_forWithoutInit () {}

    public static int test() {
	int i = 1;
	int j = 1;
	for (; i<6; i=i+1) {
	    System.out.println(i);
	    j = i * j;
	}
        return j+3;
    }

    public static void main(String[] args) {
	System.out.println("j: "+J1_forWithoutInit.test());
    }

}
// PARSER_WEEDER
public class J1_forWithoutUpdate {

    public J1_forWithoutUpdate () {}

    public static int test() {
	int j = 1;
	for (int i=1; i<6;) {
	    j = i * j;
	    if (i == 5)
		return j+3;
	    i = i + 1;
	}
	return j+3;
    }

    public static void main(String[] args) {
	System.out.println(J1_forWithoutUpdate.test());
    }
}
// PARSER_WEEDER
public class J1_for_no_short_if{
    
    public J1_for_no_short_if(){}

    public static int test(){
	int a = 43;
	if (a == 43)
	    for (int i = 0; a+i < 123; a = a + 1){ i = i+1; }
	else return 10;
	return a+40;
    }

}
// PARSER_WEEDER
public class J1_forbodycast {

    public J1_forbodycast() {}

    public static int test() {
	String String = "Hello";
	for (int i=0; i<10; i=i+1) {
	    String = (String)+(String)"World";
	}
	return String.length()+68;
    }


}
// PARSER_WEEDER
public class J1_forifstatements1 {
    
    public J1_forifstatements1() {}

    public static int test() {
	int i = 42;
	if (i==42)
	    for (i=0; i<10; i=i+1) 
		if (i!=0) 
		    i = i; 
		else 
		    return 123;
	else
	    return 42;
	return 42;
    }
    
}
// PARSER_WEEDER
public class J1_forifstatements2 {
    
    public J1_forifstatements2() {}

    public static int test() {
	int i = 42;
	if (i==42)
	    for (i=0; i<10; i=i+1) 
		if (i!=0) 
		    i=i; 
	else // must bind to closest if 
	    return 123;
	return 42;
    }
    
}
// PARSER_WEEDER
public class J1_forifstatements3 {
    
    public J1_forifstatements3() {}

    public static int test() {
	int i = 42;
	for (i=0; i<10; i=i+1) 
	    if (i==0)
		if (i!=0) 
		    return 42; 
	    else // must bind to closest if 
		return 123;
	return 42;
    }
    
}

