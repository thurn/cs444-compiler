// JOOS1:PARSER_WEEDER,PARSER_EXCEPTION
// JOOS2:PARSER_WEEDER,PARSER_EXCEPTION
// JAVAC:UNKNOWN
// 
/**
 * Parser/weeder:
 * - A PType node in an extends clause, implements clause, throws
 * clause or class instantiation expression must be an ANamedType
 */
public class Je_1_Throws_Array {

    public Je_1_Throws_Array() {}

    public static int test() {
	return 123;
    }

}
// JOOS1:PARSER_WEEDER,PARSER_EXCEPTION
// JOOS2:PARSER_WEEDER,PARSER_EXCEPTION
// JAVAC:UNKNOWN
// 
/**
 * Parser/weeder:
 * - A PType node in an extends clause, implements clause, throws
 * clause or class instantiation expression must be an ANamedType
 */
public class Je_1_Throws_SimpleType {

    public Je_1_Throws_SimpleType() {}

    public static int test() {
	return 123;
    }

}
// JOOS1:PARSER_WEEDER,PARSER_EXCEPTION
// JOOS2:PARSER_WEEDER,PARSER_EXCEPTION
// JAVAC:UNKNOWN
// 
/**
 * Parser/weeder:
 * - A PType node which is not the return type of a method must not
 * be an AVoidType.
 */
public class Je_1_Throws_Void{
    
    public static int test(){
	return 123;
    }
    
}
// JOOS1:PARSER_WEEDER,VOID_TYPE_NOT_RETURN_TYPE,VOID_TYPE_ARRAY,PARSER_EXCEPTION
// JOOS2:PARSER_WEEDER,VOID_TYPE_NOT_RETURN_TYPE,VOID_TYPE_ARRAY,PARSER_EXCEPTION
// JAVAC:UNKNOWN
// 
/**
 * Parser/weeder:
 * - A PType node which is not the return type of a method must not be
 * an AVoidType 
 */
public class Je_1_VoidType_ArrayCreation {
    
    public Je_1_VoidType_ArrayCreation(){}
    
    public static int test(){
	Object a = new void[5];
	return 123;
    }
}

// JOOS1:PARSER_WEEDER,VOID_TYPE_NOT_RETURN_TYPE,VOID_TYPE_ARRAY,PARSER_EXCEPTION
// JOOS2:PARSER_WEEDER,VOID_TYPE_NOT_RETURN_TYPE,VOID_TYPE_ARRAY,PARSER_EXCEPTION
// JAVAC:UNKNOWN
// 
/**
 * Parser/weeder:
 * - A PType node which is not the return type of a method must not be
 * an AVoidType 
 */
public class Je_1_VoidType_ArrayDeclaration {

    public Je_1_VoidType_ArrayDeclaration(){}
    
    public static int test(){
	void[] a;
	return 123;
    }
}

// JOOS1:PARSER_WEEDER,VOID_TYPE_NOT_RETURN_TYPE,VOID_TYPE_CAST,SYNTAX_ERROR,PARSER_EXCEPTION
// JOOS2:PARSER_WEEDER,VOID_TYPE_NOT_RETURN_TYPE,VOID_TYPE_CAST,SYNTAX_ERROR,PARSER_EXCEPTION
// JAVAC:UNKNOWN
// 
/**
 * Parser/weeder:
 * - A PType node which is not the return type of a method must not be
 * an AVoidType 
 */
public class Je_1_VoidType_Cast {

    public Je_1_VoidType_Cast(){}

    public static int test(){
	Je_VoidCast a = null;
	Object b = (void) a;
	return 123;
    }

}
// JOOS1:PARSER_WEEDER,VOID_TYPE_NOT_RETURN_TYPE,VOID_TYPE_FIELD,PARSER_EXCEPTION
// JOOS2:PARSER_WEEDER,VOID_TYPE_NOT_RETURN_TYPE,VOID_TYPE_FIELD,PARSER_EXCEPTION
// JAVAC:UNKNOWN
// 
/**
 * Parser/weeder:
 * - Void type not allowed for fields
 */
public class Je_1_VoidType_Field {

    public void foo;

    public Je_1_VoidType_Field() {}

    public static int test() {
	return 123;
    }

}
// JOOS1:PARSER_WEEDER,VOID_TYPE_NOT_RETURN_TYPE,VOID_TYPE_VARIABLE,PARSER_EXCEPTION
// JOOS2:PARSER_WEEDER,VOID_TYPE_NOT_RETURN_TYPE,VOID_TYPE_VARIABLE,PARSER_EXCEPTION
// JAVAC:UNKNOWN
// 
/**
 * Parser/weeder:
 * - Void type not allowed for formal parameters
 */
public class Je_1_VoidType_Formals {

    public Je_1_VoidType_Formals() {}

    public static int test(void foo) {
	return 123;
    }
}
// JOOS1:PARSER_WEEDER,VOID_TYPE_NOT_RETURN_TYPE,VOID_TYPE_VARIABLE,PARSER_EXCEPTION
// JOOS2:PARSER_WEEDER,VOID_TYPE_NOT_RETURN_TYPE,VOID_TYPE_VARIABLE,PARSER_EXCEPTION
// JAVAC:UNKNOWN
// 
/**
 * Parser/weeder:
 * - A PType node which is not the return type of a method must not be
 * an AVoidType
 */
public class Je_1_VoidType_Local {

    public Je_1_VoidType_Local() {}

    public static int test() {
	void foo = null;
	return 123;
    }
}
// JOOS1:PARSER_WEEDER,VOID_TYPE_NOT_RETURN_TYPE,VOID_TYPE_VARIABLE,PARSER_EXCEPTION
// JOOS2:PARSER_WEEDER,VOID_TYPE_NOT_RETURN_TYPE,VOID_TYPE_VARIABLE,PARSER_EXCEPTION
// JAVAC:UNKNOWN
// 
/**
 * Parser/weeder:
 * - Void type not allowed for formal parameters
 */
public class Je_1_VoidType_VoidMethod {
	public Je_1_VoidType_VoidMethod() {
		
	}
	
	public void method(void i) {
	}
	
	public static int test() {
		return 123;
	}
}
// JOOS1:PARSER_WEEDER,PARSER_EXCEPTION,TYPE_CHECKING,INVALID_INSTANCEOF
// JOOS2:PARSER_WEEDER,PARSER_EXCEPTION,TYPE_CHECKING,INVALID_INSTANCEOF
// JAVAC:UNKNOWN
// 
/**
 * Typecheck:
 * - Cannot check instanceof on int
 */
public class Je_6_Assignable_Instanceof_SimpleTypeOfSimpleType {

    public Je_6_Assignable_Instanceof_SimpleTypeOfSimpleType () {}

    public static int test() {
	boolean b = (7 instanceof int);
        return 123;
    }

}
// JOOS1:PARSER_WEEDER,PARSER_EXCEPTION,TYPE_CHECKING,INVALID_INSTANCEOF
// JOOS2:PARSER_WEEDER,PARSER_EXCEPTION,TYPE_CHECKING,INVALID_INSTANCEOF
// JAVAC:UNKNOWN
// 
/**
 * Typecheck:
 * - Type clause of instanceof must be a reference type
 */
public class Je_6_InstanceOf_Primitive_1 {

    public Je_6_InstanceOf_Primitive_1() {}

    public static int test() { 
	return 123; 
    }

    public boolean foo(int i) {
	return i instanceof int;
    }
}
// JOOS1:PARSER_WEEDER,PARSER_EXCEPTION,TYPE_CHECKING,INVALID_INSTANCEOF
// JOOS2:PARSER_WEEDER,PARSER_EXCEPTION,TYPE_CHECKING,INVALID_INSTANCEOF
// JAVAC:UNKNOWN
// 
/**
 * Typecheck:
 * - Type clause of instanceof must be a reference type
 */
public class Je_6_InstanceOf_Primitive_2 {

    public Je_6_InstanceOf_Primitive_2() {}

    public static int test() { 
	return 123; 
    }

    public boolean foo(Object o) {
	return o instanceof int;
    }
}
public class Je_Native {
    public native int m();
}
public class A {
    public A() {}
}

