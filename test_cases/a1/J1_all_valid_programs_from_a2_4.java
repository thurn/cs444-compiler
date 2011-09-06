// PARSER_WEEDER
public class J1_forinfor {

    public J1_forinfor () {}

    public static int test() {
	int i = 42;
	int j = 117;
	int k = 512;
	for (i=0; i<5; i=i+1)
	    for (j=0; j<10; j=j+1)
		k = i+j;
	return 123;
    }

}
// PARSER_WEEDER
public class J1_forinitcast {

    public J1_forinitcast() {}

    public static int test() {
	String String = "Hello";
	for (int i=(String=(String)+(String)"World").length(); String.length()<100; ) {
	    String=(String)+(String)"World";
	}
	return String.length()+23;
    }


}
// PARSER_WEEDER
public class J1_forupdatecast {

    public J1_forupdatecast() {}

    public static int test() {
	String String = "Hello";
	for (int i=String.length(); String.length()<100; String=(String)+(String)"World") {}
	return String.length()+23;
    }


}
// PARSER_WEEDER
public/**/class/*H*/J1_hello_comment/*e*/{/*ll*/
    public/*o*/
	J1_hello_comment/*,*/
	(/* */
        )/*w*/
	{/*o*/
	}/*r*/
    /*l*//*d*/ //!
    // :-)
    /*H*/public/*o*/static/*w*/int/* */test/*a*/(/*r*/)/*e*/{// 
	String/*y*/s/*o*/=/*u*/"Hello, World!"/*?*/;
	/* */System/*I*/./* */out/*a*/./*m*/println/* */(/*f*/s/*i*/)/*n*/;/*e*/
	int/*,*/r/* */=/*t*/0/*h*/;/*a*/
	for/*n*/(/*k*/int/* */i/*y*/=/*o*/0/*u*/;/*.*/i/* */</*A*/s/*n*/./*d*/length/* */(/*h*/)/*o*/;/*w*/ /* */i/*i*/=/*s*/i/* */+/*y*/1/*o*/)/*u*/ {//r
/*	    */r/*a*/=/*u*/17/*n*/*/*t*/r/*?*/+/* */s/*J*/./*o*/charAt/*l*/(/*l*/i/*y*/)/* */;/* g*/
        /*o*/}/*o*/
	/*d*/return/*.*/248113298/*.*/+/*.*/r/* */;// See
    /*y*/}/*o*/
/*u*/}// then, goodbye.

// PARSER_WEEDER
public class J1_if {
    public J1_if() {}
    public static int test() {
	return new J1_if().m(-117);
    }
    public int m(int x) {
	int y = 0;
	if (x==0) y=42;
	else y=123;
	return y;
    }
}

// PARSER_WEEDER,REACHABILITY
public class J1_ifThenElse {

    public J1_ifThenElse () {

    }

    public static int test() {
	if (true)
	    if (false) {
		return 7;
	    }
	    else {
		return 123;
	    }
	else
	    return 7;
    }

    public static void main(String[] args) {
	System.out.println(J1_ifThenElse.test());
    }
}
// PARSER_WEEDER,REACHABILITY
public class J1_if_then {

    public J1_if_then() {}

    public static int test() {
	if (true)
	    return 123;
	return 7;
    }
}
// PARSER_WEEDER
public class J1_if_then_for{
    
    public J1_if_then_for(){}

    public static int test(){
	int a = 43;
	if (a == 43)
	    for (int i = 0; a+i < 123; a = a + 1){ i = i+1; }
	return a+40;
    }

}
// PARSER_WEEDER
public class J1_implements implements java.io.Serializable {

    public J1_implements() {}

    public int x;

    public static int test() {
	return 123;
    }

}
// PARSER_WEEDER
public class J1_integerFun {

    public J1_integerFun () {}

    public static int test() {
	if ((65536*65536) == (16777216*256))
	    return 123;
        return 7;
    }

    public static void main(String[] args) {
	System.out.println(J1_integerFun.test());
    }

}
// PARSER_WEEDER
public class J1_integerFun1 {

    public J1_integerFun1 () {}

    public static int test() {
	if ((-2147483648 + -2147483648) == 0)
	    return 123;
        return 7;
    }

    public static void main(String[] args) {
	System.out.println(J1_integerFun1.test());
    }
}
// PARSER_WEEDER
public class J1_integerFun3 {

    public J1_integerFun3 () {}

    public static int test() {
	if ((641 * 6700417) == 1)
	    return 123;
        return 7;
    }

    public static void main(String[] args) {
	System.out.println(J1_integerFun3.test());
    }
}

