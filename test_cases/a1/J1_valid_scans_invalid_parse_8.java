
public class Je_1_NonJoosConstructs_SuperMethodCall{

    public Je_1_NonJoosConstructs_SuperMethodCall(){}

    public static int test(){
	return 123;
    }

}
public class Je_1_NonJoosConstructs_Synchronized{

    public Je_1_NonJoosConstructs_Synchronized(){}

    public void m(){
    }

    public static int test(){
	return 123;
    }
}


public class Je_1_NonJoosConstructs_SynchronizedStatement{

    public Je_1_NonJoosConstructs_SynchronizedStatement(){}

    public static int test() {
	Integer x = new Integer(16);
	    x = new Integer(42);
	return 123;
    }
    
}
public class Je_1_NonJoosConstructs_Transient {

    public Je_1_NonJoosConstructs_Transient() {}

    public int x;

    public static int test() {
	return 123;
    }
}
// JOOS1:PARSER_WEEDER,PARSER_EXCEPTION
// JOOS2:PARSER_WEEDER,PARSER_EXCEPTION
// JAVAC:
/**
 * Parser/weeder:
 * - Unary plus operator not allowed in Joos
 */
public class Je_1_NonJoosConstructs_UnaryPlus {

    public Je_1_NonJoosConstructs_UnaryPlus() {}

    public static int test() {
	int x = 123;
	return +x; 
    }
}
// JOOS1:PARSER_WEEDER,PARSER_EXCEPTION
// JOOS2:PARSER_WEEDER,PARSER_EXCEPTION
// JAVAC:
/**
 * Parser/weeder:
 * - Keyword not allowed in Joos
 */
public class Je_1_NonJoosConstructs_Volatile {

    public Je_1_NonJoosConstructs_Volatile() {}

    public int x;

    public static int test() {
	return 123;
    }
}
// JOOS1:PARSER_WEEDER,PARSER_EXCEPTION
// JOOS2:PARSER_WEEDER,PARSER_EXCEPTION
// JAVAC:RUN_EXCEPTION
class Je_1_PackagePrivate_Class {
    
    public Je_1_PackagePrivate_Class() {}
    
    public static int test() {
	return 123;
    }
}
// JOOS1:PARSER_WEEDER,PARSER_EXCEPTION
// JOOS2:PARSER_WEEDER,PARSER_EXCEPTION
// JAVAC:
public class Je_1_PackagePrivate_Field {

    int x;

    public Je_1_PackagePrivate_Field() { }

    public static int test() {
	return 123;
    }
}
// JOOS1:PARSER_WEEDER,PARSER_EXCEPTION
// JOOS2:PARSER_WEEDER,PARSER_EXCEPTION
// JAVAC:
public class Je_1_PackagePrivate_Method {

    public Je_1_PackagePrivate_Method() {}

    public static int test() {
		return 123;
    }

    static void packagePrivateMethod() {
    }
}
public class Je_1_SuperThis_SuperAfterStatement {
	
    public Je_1_SuperThis_SuperAfterStatement(){
	int j = 0;
    }
    
    public int test() {
	return 123;
    }
    
}
// PARSER_WEEDER,
// JOOS1: JOOS1_EXPLICIT_SUPER_CALL,SUPER_CALL_NOT_FIRST_STATEMENT,PARSER_EXCEPTION
// JOOS2: SUPER_CALL_NOT_FIRST_STATEMENT,PARSER_EXCEPTION
// JAVAC: UNKNOWN
/**
 * Parser/weeder:
 * - (Joos 1) No explicit super or this statements allowed
 * - (Joos 2) A super or this statement must be the first statement in
 *   a constructor body.
 */
public class Je_1_SuperThis_SuperInBlock {
	
    public Je_1_SuperThis_SuperInBlock(){
	{
	}
    }
    
    public int test() {
	return 123;
    }
    
}
public class Je_1_SuperThis_SuperInMethod {
	
    public Je_1_SuperThis_SuperInMethod(){
    }
	
    public void test(int foo) {
    }

}
public class Je_1_SuperThis_SuperThis {
	
    public Je_1_SuperThis_SuperThis(){
	this();
    }
    
    public int test() {
	return 123;
    }

}
public class Je_1_SuperThis_ThisAfterStatement {
    
    public Je_1_SuperThis_ThisAfterStatement(){
	int j = 0;
	this();
    }
    
    public int test() {
	return 123;
    }
    
}
public class Je_1_SuperThis_ThisInMethod {
	
    public Je_1_SuperThis_ThisInMethod(){}
    
    public int test() {
	this();
	return 123;
    }
    
}
public class Je_1_SuperThis_TwoSuperCalls {
	
    public Je_1_SuperThis_TwoSuperCalls(){
    }
	
    public int test() {
	return 123;
    }

}
public class Je_1_Throw_NotExpression {

    public Je_1_Throw_NotExpression() {}
    
    public static int test() {
	return 123;
    }
}

