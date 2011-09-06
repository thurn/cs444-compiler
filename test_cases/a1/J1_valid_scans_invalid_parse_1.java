// JOOS1: PARSER_WEEDER,JOOS1_THIS_CALL,PARSER_EXCEPTION
// JOOS2: TYPE_CHECKING,CIRCULAR_CONSTRUCTOR_INVOCATION
// JAVAC:UNKNOWN
/**
 * Parser/weeder:
 * - (Joos 1) No explicit super or this statements allowed
 * Typecheck:
 * - (Joos 2) Check that constructors are not invoking each other
 * circularly using explicit this constructor invocation statements.
 */
public class Je_16_Circularity_1 {
	
    public Je_16_Circularity_1(int i) {
	this();
    }
    
    public Je_16_Circularity_1() {
	this(100);
    }
    
    public static int test() {
	return 123;
    }
}
// JOOS1: PARSER_WEEDER,JOOS1_THIS_CALL,PARSER_EXCEPTION
// JOOS2: TYPE_CHECKING,CIRCULAR_CONSTRUCTOR_INVOCATION
// JAVAC:UNKNOWN
/**
 * Parser/weeder:
 * - (Joos 1) No explicit super or this statements allowed
 * Typecheck:
 * - (Joos 2) Check that constructors are not invoking each other
 * circularly using explicit this constructor invocation statements.
 */
public class Je_16_Circularity_2 {
	
    public Je_16_Circularity_2(int i) {
	this();
    }
    
    public Je_16_Circularity_2() {
	this("foo", "bar");
    }
    
    public Je_16_Circularity_2(String s1, String s2) {
	this(100);
    }
    
    public static int test() {
	return 123;
    }
    
}
// JOOS1: PARSER_WEEDER,JOOS1_THIS_CALL,PARSER_EXCEPTION
// JOOS2: TYPE_CHECKING,CIRCULAR_CONSTRUCTOR_INVOCATION
// JAVAC:UNKNOWN
/**
 * Parser/weeder:
 * - (Joos 1) No explicit super or this statements allowed
 * Typecheck:
 * - (Joos 2) Check that constructors are not invoking each other
 * circularly using explicit this constructor invocation statements.
 */
public class Je_16_Circularity_3 {
	
    public Je_16_Circularity_3(int i, String s) {
	this(100, "foo");
    }
    
    public static int test() {
	return 123;
    }
    
}
// JOOS1: PARSER_WEEDER,JOOS1_THIS_CALL,PARSER_EXCEPTION
// JOOS2: TYPE_CHECKING,CIRCULAR_CONSTRUCTOR_INVOCATION
// JAVAC:UNKNOWN
/**
 * Parser/weeder:
 * - (Joos 1) No explicit super or this statements allowed
 * Typecheck:
 * - (Joos 2) Check that constructors are not invoking each other
 * circularly using explicit this constructor invocation statements.
 */
public class Je_16_Circularity_4_Rhoshaped {
	public Je_16_Circularity_4_Rhoshaped() {
		this(1);
	}
	public Je_16_Circularity_4_Rhoshaped(int x) {
		this(1,2);
	}
	public Je_16_Circularity_4_Rhoshaped(int x, int y) {
		this(1);
	}
	public static int test() {
		return 123;
	}
}
// JOOS1: PARSER_WEEDER,JOOS1_MULTI_ARRAY,PARSER_EXCEPTION
// JOOS2: TYPE_CHECKING,ASSIGN_TYPE
// JAVAC:UNKNOWN
/* 
 * Calls a static method without naming the class. 
 */

public class Je_16_ClosestMatch_Array {
    public Je_16_ClosestMatch_Array() {}
    
    public static int method(Object[] e) { return 123; }
    public static void method(Cloneable[][] e) {}
    public static int method(Cloneable[] e) { return 123; }
    
    public static int test() {
	Cloneable[][] c = null;
	return method(c);
    }
}
// TYPE_CHECKING
// JOOS1: PARSER_WEEDER,JOOS1_THIS_CALL,PARSER_EXCEPTION
// JOOS2: AMBIGUOUS_OVERLOADING
// JAVAC:UNKNOWN
/**
 * Typecheck: 
 * - (Joos 1) Check that any method or constructor invocation resolves
 *   to a unique method with a type signature matching exactly the
 *   static types of the argument expressions.
 * - (Joos 2) Check that any method or constructor invocation resolves
 *   to a uniquely closest matching method or constructor (15.12.2).  
 */
public class Je_16_ClosestMatch_Constructor_NoClosestMatch_This{

    public Je_16_ClosestMatch_Constructor_NoClosestMatch_This(){
	this ((short)1, (short)2);
    }

    public Je_16_ClosestMatch_Constructor_NoClosestMatch_This(int a, short b) {}
    
    public Je_16_ClosestMatch_Constructor_NoClosestMatch_This(short a, int b) {}
    
    public static int test() {
	return 123;
    }
}
// JOOS1: PARSER_WEEDER, JOOS1_INC_DEC,PARSER_EXCEPTION
// JOOS2: TYPE_CHECKING, ASSIGN_TO_ARRAY_LENGTH
// JAVAC:UNKNOWN
/**
 * Parser/weeder:
 * - (Joos 1) Increment and decrement operators not allowed
 * Typecheck:
 * - (Joos 2) A final field must not be assigned to. (Array.length is final)
 */
public class Je_16_IncDec_Final_ArrayLengthInc {

    public Je_16_IncDec_Final_ArrayLengthInc() {}

    public static int test() {
	int[] a = new int[7];
	a.length=a.length+1;
        return 123;
    }

}
// JOOS1: PARSER_WEEDER, JOOS1_INC_DEC,PARSER_EXCEPTION
// JOOS2: TYPE_CHECKING, ASSIGN_TO_FINAL_FIELD
// JAVAC:UNKNOWN
/**
 * Parser/weeder:
 * - (Joos 1) Increment or decrement operators not allowed
 * Typecheck:
 * - (Joos 2) A final field must not be assigned to.
 */
public class Je_16_IncDec_Final_PostDec {

    public Je_16_IncDec_Final_PostDec(){
	Integer.MAX_VALUE=Integer.MAX_VALUE-1;
    }
    
    public static int test() {
	return 123;
    }

}
// JOOS1: PARSER_WEEDER, JOOS1_INC_DEC,PARSER_EXCEPTION
// JOOS2: TYPE_CHECKING, ASSIGN_TO_FINAL_FIELD
// JAVAC:UNKNOWN
/**
 * Parser/weeder:
 * - (Joos 1) Increment and decrement operations not allowed.
 * Typecheck:
 * - (Joos 2) A final field must not be assigned to.
 */
public class Je_16_IncDec_Final_PostInc {
	
    public Je_16_IncDec_Final_PostInc(){
	Integer.MIN_VALUE=Integer.MIN_VALUE+1;
    }
    
    public static int test() {
	return 123;
    }

}
// JOOS1: PARSER_WEEDER, JOOS1_INC_DEC,PARSER_EXCEPTION
// JOOS2: TYPE_CHECKING, NON_NUMERIC_INC_DEC
// JAVAC:UNKNOWN
/**
 * Parser/Weeder:
 * - (Joos 1) Increment and decrement operators not allowed
 * Typecheck:
 * - (Joos 2) Increment operator only allowed on numeric types
 */
public class Je_16_IncDec_StringPostDec{
	
    public Je_16_IncDec_StringPostDec() {}
    
    public static int test() {
	String d = "1";
	d=d-1;
	return 123;
    }
}
// JOOS1: PARSER_WEEDER, JOOS1_INC_DEC,PARSER_EXCEPTION
// JOOS2: TYPE_CHECKING, NON_NUMERIC_INC_DEC
// JAVAC:UNKNOWN
/**
 * Parser/Weeder:
 * - (Joos 1) Increment and decrement operators not allowed
 * Typecheck:
 * - (Joos 2) Increment operator only allowed on numeric types
 */
public class Je_16_IncDec_StringPostInc{
	
    public Je_16_IncDec_StringPostInc() {}
    
    public static int test() {
	String d = "1";
	d=d+1;
	return 123;
    }
}

// JOOS1: PARSER_WEEDER,JOOS1_MULTI_ARRAY,PARSER_EXCEPTION
// JOOS2: TYPE_CHECKING,ASSIGN_TYPE
// JAVAC:UNKNOWN
/**
 * Parser/weeder:
 * - (Joos 1) No multidimensional array creation expressions allowed.
 * - (Joos 2) int[][] is not assignable to int
 */
public class Je_16_MultiArrayCreation_Assign_1{
    
    public Je_16_MultiArrayCreation_Assign_1(){}
    
    public static int test(){
	int a = new int[5][2];
	return 120;
    }
}

