
// PARSER_WEEDER
// JOOS1: PARSER_EXCEPTION
// JOOS2: PARSER_EXCEPTION
// JAVAC:
/**
 * Parser/weeder:
 * - Class literals not allowed.
 */
public class Je_1_Literals_Class {

    public Je_1_Literals_Class() {}

    public static int test() {
	java.lang.Class y = Object.class;
	return 123;
    }
}

public class Je_1_Literals_Hex{

    public Je_1_Literals_Hex(){}

    public static int test(){
	return 100;
    }
}
public class Je_1_Literals_Octal{

    public Je_1_Literals_Octal(){}

    public static int test(){
	return 173;
    }
}
// PARSER_WEEDER
// JOOS1: PARSER_EXCEPTION
// JOOS2: PARSER_EXCEPTION
// JAVAC:
/**
 * Parser/weeder:
 * - Local variables must not be final
 */
public class Je_1_Locals_Final {

    public Je_1_Locals_Final() {}

    public static int test() {
	final int x = 123;
	return 123;
    }
}
 
// JOOS1:PARSER_WEEDER,PARSER_EXCEPTION
// JOOS2:PARSER_WEEDER,PARSER_EXCEPTION
// JAVAC:
/**
 * Parser/weeder:
 * - Methods must have a modifier
 */
public class Je_1_Methods_MissingAccessModifier {

    public Je_1_Methods_MissingAccessModifier() { }
    
    public static int test() { 
	return 123;
    }
	
    int bar() {
	return 123;
    }
				  
}
// JOOS1:PARSER_WEEDER,NON_ABSTRACT_METHOD_BODY,PARSER_EXCEPTION
// JOOS2:PARSER_WEEDER,NON_ABSTRACT_METHOD_BODY,PARSER_EXCEPTION
// JAVAC:UNKNOWN
// 
/**
 * Parser/weeder:
 * - A non-abstract method must have a body.
 */
public class Je_1_NonAbstractMethod_Body {

    public Je_1_NonAbstractMethod_Body() { }

    public static int test() { 
	return 123; 
    }

    public void foo();

}
// JOOS1:PARSER_WEEDER,STATIC_FINAL_METHOD,PARSER_EXCEPTION
// JOOS2:PARSER_WEEDER,STATIC_FINAL_METHOD,PARSER_EXCEPTION
// JAVAC:
/**
 * Parser/weeder:
 * - A static method cannot be final.
 */
public class Je_1_Methods_StaticFinal {

    public Je_1_Methods_StaticFinal() {}

    public static final int test(){
	return 123;
    }

}
// JOOS1:PARSER_WEEDER,PARSER_EXCEPTION
// JOOS2:PARSER_WEEDER,PARSER_EXCEPTION
// JAVAC:UNKNOWN
// 
/**
 * Parser/weeder:
 * - (Joos 1) No multidimensional array creation expressions allowed.
 * - (Joos 2) Multidimensional array creation expression is not an
 * lvalue
 */
public class Je_1_MultiArrayCreation_Assign_2{
    
    public Je_1_MultiArrayCreation_Assign_2(){}
    
    public static int test(){
	new int[5][2] = 42;
	return 120;
    }
}

// JOOS1:PARSER_WEEDER,PARSER_EXCEPTION,JOOS1_MULTI_ARRAY
// JOOS2:PARSER_WEEDER,PARSER_EXCEPTION,SYNTAX_ERROR
// JAVAC:UNKNOWN
// 
/**
 * Parser/weeder: 
 * - (Joos 1) No multidimensional array creation expressions allowed.
 * - (Joos 2) Missing dimensions in multiple array creation
 * expressions are only allowed from the right end of the
 * dimension sequence.
 */
public class Je_1_MultiArrayCreation_MissingDimension_1 {

    public Je_1_MultiArrayCreation_MissingDimension_1() {}

    public static int test() {
        int[][]a = new int[][2];
        return 123;
    }
}
// JOOS1:PARSER_WEEDER,PARSER_EXCEPTION
// JOOS2:PARSER_WEEDER,PARSER_EXCEPTION
// JAVAC:UNKNOWN
// 
/**
 * Parser/weeder:
 * - (Joos 1) No multidimensional array creation expressions allowed.
 * - (Joos 2) At least one dimension must be given in multidimensional
 * array creation expressions.  
 */
public class Je_1_MultiArrayCreation_MissingDimension_3 {

    public Je_1_MultiArrayCreation_MissingDimension_3() {}

    public static int test() {
        int[][] a = new int[][];
        return 123;
    }
}
//PARSER_WEEDER
//JOOS1:PARSER_EXCEPTION
//JOOS2:PARSER_EXCEPTION
//JAVAC:UNKNOWN

public Je_1_MultiArrayCreation_MissingDimension_4 {
	
	public Je_1_MultiArrayCreation_MissingDimension_4() {}

	public static int test() {
		int[][][] array = new int[2][][2];
		return 123;
	}
	
}
// JOOS1:PARSER_WEEDER,PARSER_EXCEPTION
// JOOS2:PARSER_WEEDER,PARSER_EXCEPTION
// JAVAC:UNKNOWN
// 
/**
 * Parser/weeder:
 * - (Joos 1) No multidimensional array creation expressions allowed
 * - (Joos 2) Multidimenstional array creation expressions must have a
 * base type.
 */
public class Je_1_MultiArrayCreation_NoType {

    public Je_1_MultiArrayCreation_NoType() {}

    public static int test() {
        int[][] a = new [2][2];
        return 123;
    }
}
// JOOS1:PARSER_WEEDER,PARSER_EXCEPTION
// JOOS2:PARSER_WEEDER,PARSER_EXCEPTION
// JAVAC:UNKNOWN
// 
/**
 * Parser/weeder:
 * - (Joos 1) Multidimensional array types not allowed
 * - (Joos 2) Dimensions not allowed in array types.
 */
public class Je_1_MultiArrayTypes_Dimensions {

    public Je_1_MultiArrayTypes_Dimensions() {}

    public static int test() {
        int[][42] a = new int[2][2];
        return 123;
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
public class Je_1_NonJoosConstructs_AssignmentOperations_BitwiseAnd {

    public Je_1_NonJoosConstructs_AssignmentOperations_BitwiseAnd() {}

    public static int test() {
	int x = 127;
	x&=251;
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
public class Je_1_NonJoosConstructs_AssignmentOperations_BitwiseOr {

    public Je_1_NonJoosConstructs_AssignmentOperations_BitwiseOr() {}

    public static int test() {
	int x = 91;
	x|=42;
	return x;
    }
}

