// JOOS1:PARSER_WEEDER,PARSER_EXCEPTION
// JOOS2:PARSER_WEEDER,PARSER_EXCEPTION
// JAVAC:UNKNOWN
// 
/**
 * Parser/weeder:
 * - A PType node in an extends clause, implements clause, throws
 * clause or class instantiation expression must be an ANamedType
 */
public class Je_1_Implements_Value implements 4 {

    public Je_1_Implements_Value() { }

    public static int test() { 
	return 123; 
    }

}
// PARSER_WEEDER
// JOOS1: PARSER_EXCEPTION
// JOOS2: PARSER_EXCEPTION
// JAVAC: 
/**
 * Parser/weeder:
 * - Instance initializers not allowed.
 */
public class Je_1_InstanceInitializers {

    public Je_1_InstanceInitializers() {}

    public int x;

    {
	x = 123; 
    }

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
 * - null value is not a type
 */
public class Je_1_InstanceOf_Null {

    public Je_1_InstanceOf_Null() { }

    public static int test() {
	Object o=new Object();
	if (o instanceof null)
	    return 100;
	return 123;
    }
}
// JOOS1:PARSER_WEEDER,PARSER_EXCEPTION,TYPE_CHECKING,INVALID_INSTANCEOF
// JOOS2:PARSER_WEEDER,PARSER_EXCEPTION,TYPE_CHECKING,INVALID_INSTANCEOF
// JAVAC:UNKNOWN
// 
public class Je_1_InstanceOf_Primitive {
    /* Parser+Weeder => instanceof is not allowed on primitive types */
    public Je_1_InstanceOf_Primitive() {}
    
    public static int test() {
	int a = 0;
	if (a instanceof int) return 42;
	return 123;
    }
}
// JOOS1:PARSER_WEEDER,VOID_TYPE_NOT_RETURN_TYPE,VOID_TYPE_INSTANCEOF,PARSER_EXCEPTION
// JOOS2:PARSER_WEEDER,VOID_TYPE_NOT_RETURN_TYPE,VOID_TYPE_INSTANCEOF,PARSER_EXCEPTION
// JAVAC:UNKNOWN
// 
/**
 * Parser/weeder:
 * - A PType node which is not the return type of a method must not be
 * an AVoidType
 */
public class Je_1_InstanceOf_Void {

    public Je_1_InstanceOf_Void() {}

    public static int test() { 
	return 123; 
    }

    public boolean foo(Object o) {
	return o instanceof void;
    }
}
// JOOS1:PARSER_WEEDER,INVALID_INTEGER
// JOOS2:PARSER_WEEDER,INVALID_INTEGER
// JAVAC:UNKNOWN
// 
/**
 * Parser/weeder:
 * - Check that all integer constant values are within the legal range
 * for the int type.
 */
public class Je_1_IntRange_MinusTooBigInt {
    
    public Je_1_IntRange_MinusTooBigInt(){}
    
    public static int test() {
	return 2147483000 - 2147483648 + 771;
    }
}

// JOOS1:PARSER_WEEDER,INVALID_INTEGER
// JOOS2:PARSER_WEEDER,INVALID_INTEGER
// JAVAC:UNKNOWN
// 
/**
 * Parser/weeder:
 * - For each integer literal in the program, .... check that the
 * number is within the legal range for 32-bit signed integers.  
 */
public class Je_1_IntRange_PlusTooBigInt {

    public Je_1_IntRange_PlusTooBigInt(){}
    
    public static int test() {
	return  0 - 2147483525 + 2147483648;
    }
}

// JOOS1:PARSER_WEEDER,INVALID_INTEGER
// JOOS2:PARSER_WEEDER,INVALID_INTEGER
// JAVAC:UNKNOWN
// 
/**
 * Parser/weeder:
 * - For each integer literal in the program, .... check that the
 * number is within the legal range for 32-bit signed integers.  
 */
public class Je_1_IntRange_TooBigInt {

    public Je_1_IntRange_TooBigInt(){}
    
    public static int test() {
	return 2147483648 - 2147483525;
    }
}

// JOOS1:PARSER_WEEDER,INVALID_INTEGER
// JOOS2:PARSER_WEEDER,INVALID_INTEGER
// JAVAC:UNKNOWN
// 
/**
 * Parser/weeder:
 * - For each integer literal in the program, .... check that the
 * number is within the legal range for 32-bit signed integers.  
 */
public class Je_1_IntRange_TooBigIntNegated {

    public Je_1_IntRange_TooBigIntNegated(){}
    
    public static int test() {
	return -(2147483648) + 2147483000 + 771;
    }
}

// JOOS1:PARSER_WEEDER,INVALID_INTEGER
// JOOS2:PARSER_WEEDER,INVALID_INTEGER
// JAVAC:UNKNOWN
// 
/**
 * Parser/weeder:
 * - For each integer ... Check that the number is within
 * the legal range for 32-bit signed integers.
 */
public class Je_1_IntRange_TooBigInt_InInitializer {

    public Je_1_IntRange_TooBigInt_InInitializer () {}

    public static int test() {
       	int i = 2147483648;
        return 123;
    }

}
// PARSER_WEEDER
// JOOS1: JOOS1_INTERFACE,PARSER_EXCEPTION
// JOOS2: INTERFACE_CONSTRUCTOR,PARSER_EXCEPTION
// JAVAC: UNKNOWN
/**
 * Parser/weeder:
 * - (Joos 1) No interfaces allowed
 * - (Joos 2) An interface must contain no fields or constructors
 */
public interface Je_1_Interface_ConstructorAbstract {
	
    public Je_1_Interface_ConstructorAbstract();
    
    public int test();

}
// PARSER_WEEDER
// JOOS1: JOOS1_INTERFACE,PARSER_EXCEPTION
// JOOS2: INTERFACE_CONSTRUCTOR,PARSER_EXCEPTION
// JAVAC: UNKNOWN
/**
 * Parser/weeder:
 * - (Joos 1) No interfaces allowed
 * - (Joos 2) An interface must contain no fields or constructors
 */
public interface Je_1_Interface_ConstructorBody {
	
    public Je_1_Interface_ConstructorBody() {}
    
    public int test();

}
// PARSER_WEEDER
// JOOS1: JOOS1_INTERFACE,PARSER_EXCEPTION
// JOOS2: INTERFACE_FIELD,PARSER_EXCEPTION
// JAVAC: UNKNOWN
/**
 * Parser/weeder:
 * - (Joos 1) No interfaces allowed
 * - (Joos 2) An interface must contain no fields or constructors
 */
public interface Je_1_Interface_Field {
    
    public int field;
    
}
// PARSER_WEEDER
// JOOS1: JOOS1_INTERFACE,PARSER_EXCEPTION
// JOOS2: STATIC_OR_FINAL_INTERFACE_METHOD,PARSER_EXCEPTION
// JAVAC: UNKNOWN
/**
 * Parser/weeder:
 * - (Joos 1) No interfaces allowed
 * - (Joos 2) An interface method cannot be static or final
 */
public interface Je_1_Interface_FinalMethod {
    
    public final void foo();

}
// PARSER_WEEDER
// JOOS1: JOOS1_INTERFACE,PARSER_EXCEPTION
// JOOS2: INTERFACE_METHOD_WITH_BODY,PARSER_EXCEPTION
// JAVAC: UNKNOWN
/**
 * Parser/weeder:
 * - (Joos 1) No interfaces allowed
 * - (Joos 2) An interface method must not have a body
 */
public interface Je_1_Interface_MethodBody {
	
    public int test() {
	return 123;
    }

}
// JOOS1:PARSER_WEEDER,PARSER_EXCEPTION
// JOOS2:PARSER_WEEDER,PARSER_EXCEPTION
// JAVAC:UNKNOWN
// 
/**
 * Parser/weeder:
 * - (Joos 1) No interfaces allowed
 * - (Joos2) An interface must have a body
 */
public interface Je_1_Interface_NoBody
// PARSER_WEEDER
// JOOS1: JOOS1_INTERFACE,PARSER_EXCEPTION
// JOOS2: STATIC_OR_FINAL_INTERFACE_METHOD,PARSER_EXCEPTION
// JAVAC: UNKNOWN
/**
 * Parser/weeder:
 * - (Joos 1) No interfaces allowed
 * - (Joos 2) An interface method cannot be static or final
 */
public interface Je_1_Interface_StaticMethod {

    public static void foo();

}
