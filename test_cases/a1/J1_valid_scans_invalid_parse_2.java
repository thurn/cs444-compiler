//JOOS1:PARSER_WEEDER,PARSER_EXCEPTION,JOOS1_MULTI_ARRAY
//JOOS2:TYPE_CHECKING,NON_NUMERIC_ARRAY_SIZE
//JAVAC:UNKNOWN
public class Je_16_MultiArrayCreation_Null {
	public Je_16_MultiArrayCreation_Null() {}
	
	public static int test() {
		int[][][] a = new int[5][null][];
		return 123;
	}
}
// JOOS1: PARSER_WEEDER,JOOS1_THIS_CALL,PARSER_EXCEPTION
// JOOS2: TYPE_CHECKING,THIS_BEFORE_SUPER_CALL
// JAVAC:UNKNOWN
/**
 * Parser/weeder:
 * - (Joos 1) Explicit this statements not allowed
 * Typecheck:
 * - A this reference (AThisExp) must not occur, explicitly or
 * implicitly, in a static method, an initializer for a static field,
 * or an argument to a super or this constructor invocation.  
 */
public class Je_16_StaticThis_ArgumentToThis{

    public Je_16_StaticThis_ArgumentToThis(){
	this(this);
    }

    public Je_16_StaticThis_ArgumentToThis(Je_16_StaticThis_ArgumentToThis o){}

    public static int test(){
	return 123;
    }
}
// JOOS1: PARSER_WEEDER,JOOS1_THIS_CALL,PARSER_EXCEPTION
// JOOS2: TYPE_CHECKING,NO_MATCHING_CONSTRUCTOR_FOUND
// JAVAC:UNKNOWN
/**
 * Parser/weeder:
 * - (Joos 1) No explicit super or this statements allowed.
 * Typecheck:
 * - (Joos 2) Check that any method or constructor invocation
 * resolves to a uniquely closest matching method or constructor
 * (15.12.2).  
 */
public class Je_16_SuperThis_InvalidThisParameter {

    public Je_16_SuperThis_InvalidThisParameter() {
	this(42);
    }

    public Je_16_SuperThis_InvalidThisParameter(String s) {}
    
    public static int test() { 
	return 123; 
    }
}


// JOOS1:PARSER_WEEDER,PARSER_EXCEPTION
// JOOS2:PARSER_WEEDER,PARSER_EXCEPTION
// JAVAC:UNKNOWN
/**
 * Parser/weeder:
 * - A constructor must not be abstract.
 */
public abstract class Je_1_AbstractClass_AbstractConstructor{

    public abstract Je_1_AbstractClass_AbstractConstructor();

}
// JOOS1:PARSER_WEEDER,ABSTRACT_FINAL_CLASS,PARSER_EXCEPTION
// JOOS2:PARSER_WEEDER,ABSTRACT_FINAL_CLASS,PARSER_EXCEPTION
// JAVAC:UNKNOWN
/**
 * Parser/weeder:
 * - An abstract class cannot be final
 */
public final abstract class Je_1_AbstractClass_Final {

    public Je_1_AbstractClass_Final() {}

    public static int test() {
	return 123;
    }

}
// JOOS1:PARSER_WEEDER,ABSTRACT_METHOD_FINAL_OR_STATIC,PARSER_EXCEPTION
// JOOS2:PARSER_WEEDER,ABSTRACT_METHOD_FINAL_OR_STATIC,PARSER_EXCEPTION
// JAVAC:UNKNOWN
/**
  * Parser/weeder:
	* - An abstract method cannot be final.
	*/
public abstract class Je_1_AbstractMethodCannotBeFinal {
	public Je_1_AbstractMethodCannotBeFinal() {}
	public final abstract void foo();
}
// JOOS1:PARSER_WEEDER,PARSER_EXCEPTION,ABSTRACT_METHOD_BODY
// JOOS2:PARSER_WEEDER,PARSER_EXCEPTION,ABSTRACT_METHOD_BODY
// JAVAC:UNKNOWN
/**
 * Parser/weeder:
 * - An abstract method must not have a body
 */
public class Je_1_AbstractMethod_Body {

    public Je_1_AbstractMethod_Body() { }

    public static int test() { 
	return 123;
    }

    public abstract int foo() {
	return 123;
    }
}
// JOOS1:PARSER_WEEDER,PARSER_EXCEPTION,ABSTRACT_METHOD_BODY
// JOOS2:PARSER_WEEDER,PARSER_EXCEPTION,ABSTRACT_METHOD_BODY
// JAVAC:UNKNOWN
/**
 * Parser/weeder:
 * - An abstract method must not have a body
 */
public abstract class Je_1_AbstractMethod_EmptyBody {

    public Je_1_AbstractMethod_EmptyBody () {}
    
    public abstract int foo() {}

    public static int test() {
        return 123;
    }

}
// JOOS1:PARSER_WEEDER,ABSTRACT_METHOD_FINAL_OR_STATIC,PARSER_EXCEPTION
// JOOS2:PARSER_WEEDER,ABSTRACT_METHOD_FINAL_OR_STATIC,PARSER_EXCEPTION
// JAVAC:UNKNOWN
/**
 * Parser/weeder:
 * - An abstract method cannot be static or final.
 */
public abstract class Je_1_AbstractMethod_Final {

    public Je_1_AbstractMethod_Final() { }

    public static int test() { 
	return 123; 
    }

    public abstract final void foo();
}

