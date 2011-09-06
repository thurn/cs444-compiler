// PARSER_WEEDER
/**
 * Parser/weeder
 * - Test of octal escape decoding
 */
public class J1_1_Escapes_3DigitOctalAndDigit{

    public J1_1_Escapes_3DigitOctalAndDigit(){}

    public static int test(){
        String s = "\1674";
        return s.charAt(0) + s.charAt(1) - '0';
    }

}
// PARSER_WEEDER,CODE_GENERATION
/**
 * Parser/weeder:
 * - Tests the priority of instanceof
 */
public class J1_1_Instanceof_InLazyExp{

    public J1_1_Instanceof_InLazyExp(){}

    public static int test(){
	
	boolean b = true;
	boolean e = false;
	Object a = new J1_1_Instanceof_InLazyExp();
	boolean c = e || a instanceof J1_1_Instanceof_InLazyExp;
	boolean d = b && a instanceof J1_1_Instanceof_InLazyExp;

	if (c && d){
	    return 123;
	}
	else {
	    return 12378;
	}
    }

}
// PARSER_WEEDER,CODE_GENERATION
/**
 * Parser/weeder:
 * - Tests the precedence of instanceof
 */
public class J1_1_Instanceof_OfAdditiveExpression{

    public J1_1_Instanceof_OfAdditiveExpression(){}

    public static int test(){
	String a = "123";
	boolean b = a + 3 instanceof String;

	if (b){
	    return Integer.parseInt(a);
	}
	else {
	    return -1;
	}
    }

}
// PARSER_WEEDER,CODE_GENERATION
/**
 * Parser/weeder:
 * Tests the precedence relation between casts and instanceof
 */
public class J1_1_Instanceof_OfCastExpression{

    public J1_1_Instanceof_OfCastExpression(){}

    public static int test(){
	J1_1_Instanceof_OfCastExpression o = new J1_1_Instanceof_OfCastExpression();
	boolean b = (Object) o instanceof J1_1_Instanceof_OfCastExpression;
	if (b){
	    return 123;
	}
	else {
	    return -1;
	}
    }

}

// PARSER_WEEDER
public class J1_1_IntRange_NegativeInt {
    public J1_1_IntRange_NegativeInt() {}
    
    public static int test() {
	int a = -2147483648;
	if (a-1 > a) 
	    return 123;
	return 42;
    }
}
// PARSER_WEEDER,CODE_GENERATION
public class J1_ArrayCreateAndIndex {
    public J1_ArrayCreateAndIndex() {}
    public static int test() {
	return 123 + (new int[1])[0];
    }
}
// PARSER_WEEDER
public class J1_BigInt {

    public J1_BigInt(){}

       public static int test() {

	   return 2147483647 - 2147483524;
       }
}

// PARSER_WEEDER,TYPE_CHECKING
public class J1_CharCast {

    public J1_CharCast(){}

       public static int test() {

	   return (char)123456 - 57797;
       }
}

// PARSER_WEEDER,TYPE_CHECKING
public class J1_CharCharInit1 {

    public J1_CharCharInit1(){}

	public static int test() {
		char x = (char)1;
		return x + 122;
	}
}

// PARSER_WEEDER
public class J1_CharCharInit2 {

    public J1_CharCharInit2(){}

	public static int test() {
		char x = '*';
		return x + 81;
	}
}

// PARSER_WEEDER
public class J1_EscapeEscape {
	public J1_EscapeEscape() {}
	
	public static int test() {
		String s = "\\\\\\";
		return s.length()+120;
	}
}
// PARSER_WEEDER
public class J1_ForUpdate_ClassCreation {
    public J1_ForUpdate_ClassCreation() {}
    
    public static int test() {
	for (int i = 0 ; i < 10 ; new String("foo")) {
	    i = 10;
	}
	return 123;
    }
}
// PARSER_WEEDER
public class J1_IntArrayDecl1{

    public J1_IntArrayDecl1(){}

    public static int test(){
	    int[] a = new int[5];
	    return 123;
    }
}

// PARSER_WEEDER
public class J1_IntArrayDecl2{

    public J1_IntArrayDecl2(){}

    public static int test(){
	    (new int[5])[2] = 42;
	    return 123;
    }
}

// PARSER_WEEDER
public class J1_IntCast {

    public J1_IntCast(){}

       public static int test() {

	   return (int)123456 - 123333;
       }
}

