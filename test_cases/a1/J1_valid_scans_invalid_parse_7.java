// JOOS1:PARSER_WEEDER,PARSER_EXCEPTION
// JOOS2:PARSER_WEEDER,PARSER_EXCEPTION
// JAVAC:
// 
/**
 * Parser/weeder:
 * - Assignment operations not allowed
 */
public class Je_1_NonJoosConstructs_AssignmentOperations_BitwiseXOR {

    public Je_1_NonJoosConstructs_AssignmentOperations_BitwiseXOR() {}

    public static int test() {
	int x = 42;
	return x;
    }
}
// JOOS1:PARSER_WEEDER,PARSER_EXCEPTION
// JOOS2:PARSER_WEEDER,PARSER_EXCEPTION
// JAVAC:
// 
/**
 * Parser/weeder:
 * - Assignment operations not allowed
 */
public class Je_1_NonJoosConstructs_AssignmentOperations_Divide {

    public Je_1_NonJoosConstructs_AssignmentOperations_Divide() {}

    public static int test() {
	int x = 246;
	x/=2;
	return x;
    }
}
// JOOS1:PARSER_WEEDER,PARSER_EXCEPTION
// JOOS2:PARSER_WEEDER,PARSER_EXCEPTION
// JAVAC:
// 
/**
 * Parser/weeder:
 * - Assignment operations not allowed
 */
public class Je_1_NonJoosConstructs_AssignmentOperations_Minus {

    public Je_1_NonJoosConstructs_AssignmentOperations_Minus() {}

    public static int test() {
	int x = 165;
	x-=42;
	return x;
    }
}
// JOOS1:PARSER_WEEDER,PARSER_EXCEPTION
// JOOS2:PARSER_WEEDER,PARSER_EXCEPTION
// JAVAC:
// 
/**
 * Parser/weeder:
 * - Assignment operations not allowed
 */
public class Je_1_NonJoosConstructs_AssignmentOperations_Multiply {

    public Je_1_NonJoosConstructs_AssignmentOperations_Multiply() {}

    public static int test() {
	int x = 3;
	x*=41;
	return x;
    }
}
// JOOS1:PARSER_WEEDER,PARSER_EXCEPTION
// JOOS2:PARSER_WEEDER,PARSER_EXCEPTION
// JAVAC:
// 
/**
 * Parser/weeder:
 * - Assignment operations not allowed
 */
public class Je_1_NonJoosConstructs_AssignmentOperations_Plus {

    public Je_1_NonJoosConstructs_AssignmentOperations_Plus() {}

    public static int test() {
	int x = 81;
	x+=42;
	return x;
    }
}
// JOOS1:PARSER_WEEDER,PARSER_EXCEPTION
// JOOS2:PARSER_WEEDER,PARSER_EXCEPTION
/**
 * Parser/weeder:
 * - Assignment operations not allowed
 */
public class Je_1_NonJoosConstructs_AssignmentOperations_Remainder {

    public Je_1_NonJoosConstructs_AssignmentOperations_Remainder() {}

    public static int test() {
	int x = 15375;
	x%=124;
	return x;
    }
}
// JOOS1:PARSER_WEEDER,PARSER_EXCEPTION
// JOOS2:PARSER_WEEDER,PARSER_EXCEPTION
// 
/**
 * Parser/weeder:
 * - Assignment operations not allowed
 */
public class Je_1_NonJoosConstructs_AssignmentOperations_ShiftLeft {

    public Je_1_NonJoosConstructs_AssignmentOperations_ShiftLeft() {}

    public static int test() {
	int x = 30;
	x<<=2;
	return x+3;
    }
}
// JOOS1:PARSER_WEEDER,PARSER_EXCEPTION
// JOOS2:PARSER_WEEDER,PARSER_EXCEPTION
/**
 * Parser/weeder:
 * - Assignment operations not allowed
 */
public class Je_1_NonJoosConstructs_AssignmentOperations_SignShiftRight {

    public Je_1_NonJoosConstructs_AssignmentOperations_SignShiftRight() {}

    public static int test() {
	int x = -492;
	x>>=2;
	return x+246;
    }
}
// JOOS1:PARSER_WEEDER,PARSER_EXCEPTION
// JOOS2:PARSER_WEEDER,PARSER_EXCEPTION
/**
 * Parser/weeder:
 * - Assignment operations not allowed
 */
public class Je_1_NonJoosConstructs_AssignmentOperations_ZeroShiftRight {

    public Je_1_NonJoosConstructs_AssignmentOperations_ZeroShiftRight() {}

    public static int test() {
	int x = -492;
	x>>>=2;
	return x-1073741578;
    }
}
// JOOS1:PARSER_WEEDER,PARSER_EXCEPTION
// JOOS2:PARSER_WEEDER,PARSER_EXCEPTION
/**
 * Parser/weeder:
 * - Bitshift operators not allowed
 */
public class Je_1_NonJoosConstructs_BitShift_Left {

    public Je_1_NonJoosConstructs_BitShift_Left() {}
    
    public static int test() {
	int x = 30;
	return (x << 2) + 3;
    }
}

// JOOS1:PARSER_WEEDER,PARSER_EXCEPTION
// JOOS2:PARSER_WEEDER,PARSER_EXCEPTION
/**
 * Parser/weeder:
 * - Bitshift operators not allowed
 */
public class Je_1_NonJoosConstructs_BitShift_SignRight {

    public Je_1_NonJoosConstructs_BitShift_SignRight() {}
    
    public static int test() {
	int x = -492;
	return (x >> 2) + 246;
    }
}

// JOOS1:PARSER_WEEDER,PARSER_EXCEPTION
// JOOS2:PARSER_WEEDER,PARSER_EXCEPTION
/**
 * Parser/weeder:
 * - Bitshift operators not allowed
 */
public class Je_1_NonJoosConstructs_BitShift_ZeroRight {

    public Je_1_NonJoosConstructs_BitShift_ZeroRight() {}
    
    public static int test() {
	int x = -492;
	return (x >>> 2) - 1073741578;
    }
}

// JOOS1:PARSER_WEEDER,PARSER_EXCEPTION
// JOOS2:PARSER_WEEDER,PARSER_EXCEPTION
// JAVAC:
/**
 * Parser/weeder:
 * - Break statement not allowed.
 */
public class Je_1_NonJoosConstructs_Break {

    public Je_1_NonJoosConstructs_Break() {}

    public static int test() {
	int x = 117;
	while (x>0) {
	    x=x-1;
	}
	return 123;
    }
}

// JOOS1:PARSER_WEEDER,PARSER_EXCEPTION
// JOOS2:PARSER_WEEDER,PARSER_EXCEPTION
/**
 * Parser/weeder:
 * - Continue statements not allowed.
 */
public class Je_1_NonJoosConstructs_Continue {

    public Je_1_NonJoosConstructs_Continue() {}

    public static int test() {
	int x = 117;
	while (x>0) {
		x = x - 1;
	}
	return 123;
    }
}


// JOOS1:PARSER_WEEDER,PARSER_EXCEPTION
// JOOS2:PARSER_WEEDER,PARSER_EXCEPTION
// JAVAC:UNKNOWN
/**
 * Parser/weeder:
 * - Expression sequencing not allowed.
 */
public class Je_1_NonJoosConstructs_ExpressionSequence {

    public Je_1_NonJoosConstructs_ExpressionSequence() {}

    public static int test() {
	int i = 0;
	int j= (i = i + 1, i); 
	return 123;
    }

}
// JOOS1:PARSER_WEEDER,PARSER_EXCEPTION
// JOOS2:PARSER_WEEDER,PARSER_EXCEPTION
/**
 * Parser/weeder:
 * - Multiple types pr. file not allowed.
 */
public class Je_1_NonJoosConstructs_MultipleTypesPrFile {

    public Je_1_NonJoosConstructs_MultipleTypesPrFile(){}
    
    public static int test() {
    	return 123;
    }
}

class A {

    public A(){}
}
// JOOS1:PARSER_WEEDER,PARSER_EXCEPTION
// JOOS2:PARSER_WEEDER,PARSER_EXCEPTION
/**
 * Parser/weeder:
 * - Nested types not allowed.
 */
public class Je_1_NonJoosConstructs_NestedTypes {

    public Je_1_NonJoosConstructs_NestedTypes() {}

    public class A {
	
		public A(){}
    }
    
    public static int test() {
    	return 123;
    }
}
public class Je_1_NonJoosConstructs_PrivateFields {

    public int x;

    public Je_1_NonJoosConstructs_PrivateFields() {}

    public static int test() {
	return 123;
    }
}
public class Je_1_NonJoosConstructs_PrivateMethods {

    public Je_1_NonJoosConstructs_PrivateMethods () {}

    public int m() {
	return 42;
    }

    public static int test() {
	return 123;
    }
}
// JOOS1:PARSER_WEEDER,PARSER_EXCEPTION
// JOOS2:PARSER_WEEDER,PARSER_EXCEPTION
// JAVAC:
/**
 * Parser/weeder:
 * - Static initializers not allowed in joos
 */
public class Je_1_NonJoosConstructs_StaticInitializers {

    public Je_1_NonJoosConstructs_StaticInitializers() {}

    static { 
	Je_1_NonJoosConstructs_StaticInitializers.test(); 
    }

    public static int test() {
	return 123;
    }
}

