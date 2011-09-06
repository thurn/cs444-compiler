// JOOS1:PARSER_WEEDER,PARSER_EXCEPTION,ABSTRACT_METHOD_FINAL_OR_STATIC
// JOOS2:PARSER_WEEDER,PARSER_EXCEPTION,ABSTRACT_METHOD_FINAL_OR_STATIC
// JAVAC:UNKNOWN
/**
 * Parser/weeder:
 * - An abstract method cannot be static or final.
 */
public abstract class Je_1_AbstractMethod_Static {

    public Je_1_AbstractMethod_Static() { }

    public static int test() { 
	return 123; 
    }

    public abstract static void foo();
}
public class Je_1_Access_PrivateLocal{

    public Je_1_Access_PrivateLocal(){}

    public static int test(){
	int a = 123;
	return a;
    }
}
// JOOS1:PARSER_WEEDER,PARSER_EXCEPTION
// JOOS2:PARSER_WEEDER,PARSER_EXCEPTION
// JAVAC:UNKNOWN
/**
 * Parser/weeder:
 * - A local variable must not have an access modifier.
 */
public class Je_1_Access_ProtectedLocal{

    public Je_1_Access_ProtectedLocal(){}

    public static int test(){
	protected int a = 123;
	return a;
    }
}
// JOOS1:PARSER_WEEDER,PARSER_EXCEPTION
// JOOS2:PARSER_WEEDER,PARSER_EXCEPTION
// JAVAC:UNKNOWN
/**
 * Parser/weeder:
 * - A local variable must not have an access modifier.
 */
public class Je_1_Access_PublicLocal{

    public Je_1_Access_PublicLocal(){}

    public static int test(){
	public int a = 123;
	return a;
    }
}
// PARSER_WEEDER
// JOOS1:PARSER_EXCEPTION
// JOOS2:PARSER_EXCEPTION
// JAVAC:
/**
 * Parser/weeder:
 * - Array data expressions not allowed
 */
public class Je_1_Array_Data {

    public Je_1_Array_Data() {}

    public static int test() {
	int[] x = { 123,1,2,3 };
	return 123;
    }
}

// PARSER_WEEDER
// JOOS1:PARSER_EXCEPTION
// JOOS2:PARSER_EXCEPTION
// JAVAC:
/**
 * Parser/weeder:
 * - Array data expressions not allowed
 */
public class Je_1_Array_Data_Empty {

    public Je_1_Array_Data_Empty() {}

    public static int test() {
	int[] x = {};
	return 123;
    }
}

// PARSER_WEEDER
// JOOS1:PARSER_EXCEPTION
// JOOS2:PARSER_EXCEPTION
// JAVAC:
/**
 * Parser/weeder:
 * - Array brackets ('[]') are not allowed to occur in the name of a
 *   variable being declared.
 */
public class Je_1_Array_OnVariableNameInDecl {

    public Je_1_Array_OnVariableNameInDecl() { }

    public static int test() {
	int a[];
	return 123;
    }

}
// JOOS1:PARSER_WEEDER,PARSER_EXCEPTION,SYNTAX_ERROR
// JOOS2:PARSER_WEEDER,PARSER_EXCEPTION,SYNTAX_ERROR
// JAVAC:UNKNOWN
public class Je_1_CastToArrayLvalue {
	public Je_1_CastToArrayLvalue() {}

	public static int test() {
		int[] ia = new int[5];
		int i = (ia[5]) ia;
		return 123;
	}

	public static void main(String[] args) {
		System.out.println(Je_1_CastToArrayLvalue.test());
	}
}
//JOOS1:PARSER_WEEDER,PARSER_EXCEPTION,SYNTAX_ERROR
//JOOS2:PARSER_WEEDER,PARSER_EXCEPTION,SYNTAX_ERROR
//JAVAC:UNKNOWN
public class Je_1_Cast_DoubleParenthese {
	public Je_1_Cast_DoubleParenthese() {}
	
	public static int test() {
		Object o = ((Object))null;
		return 123;
	}
}
// JOOS1:PARSER_WEEDER,PARSER_EXCEPTION,SYNTAX_ERROR
// JOOS2:PARSER_WEEDER,PARSER_EXCEPTION,SYNTAX_ERROR
// JAVAC:UNKNOWN

public class Je_1_Cast_Expression {
    	/* Parser+Weeder => cast to an expression is not allowed */
	public Je_1_Cast_Expression() {}
	
	public static int test() {
		int a = 1;
		Object o = (5-a)null;
		return 123;
	}
}
// JOOS1:PARSER_WEEDER,PARSER_EXCEPTION
// JOOS2:PARSER_WEEDER,PARSER_EXCEPTION
// JAVAC:UNKNOWN

/**
 * Parser/weeder:
 * - Cast of left-hand side of assignment not allowed
 */
public class Je_1_Cast_LeftHandSideOfAssignment_1 {

    public Je_1_Cast_LeftHandSideOfAssignment_1() {}

    public static int test() {
	Object o;
	(Object)o=null;
	return 123;
    }


}
// JOOS1:PARSER_WEEDER,PARSER_EXCEPTION
// JOOS2:PARSER_WEEDER,PARSER_EXCEPTION
// JAVAC:UNKNOWN
/**
 * Parser/weeder:
 * - Cast of left-hand side of assignment not allowed
 */
public class Je_1_Cast_LeftHandSideOfAssignment_2 {

    public Je_1_Cast_LeftHandSideOfAssignment_2() {}

    public static int test() {
	Object o;
	Object p = (Object)o=null;
	return 123;
    }


}
// JOOS1:PARSER_WEEDER,PARSER_EXCEPTION
// JOOS2:PARSER_WEEDER,PARSER_EXCEPTION
// JAVAC:UNKNOWN
/**
 * Parser/weeder:
 * - Type clause in cast must be enclosed in parentheses
 */
public class Je_1_Cast_NoParenthesis {

    public Je_1_Cast_NoParenthesis(){}

    public static int test() {
	int foo = -123;
	return int-foo;
    }
}
// JOOS1:PARSER_WEEDER,PARSER_EXCEPTION,SYNTAX_ERROR
// JOOS2:PARSER_WEEDER,PARSER_EXCEPTION,SYNTAX_ERROR
// JAVAC:UNKNOWN
public class Je_1_Cast_NonstaticField {
    /* Parser+Weeder => cast to a nonstatic field is not allowed */
    public int value = 123;
    
    public Je_1_Cast_NonstaticField() {}
    
    public static int test() {
	int a = (new Je_1_Cast_NonstaticField().value)123;
	return a;
    }
}
// JOOS1:PARSER_WEEDER,PARSER_EXCEPTION,SYNTAX_ERROR
// JOOS2:PARSER_WEEDER,PARSER_EXCEPTION,SYNTAX_ERROR
// JAVAC:UNKNOWN
// 
/**
 * Parser/weeder:
 * - Method invocation not allowed as type in cast.
 */
public class Je_1_Cast_ToMethodInvoke {

    public Je_1_Cast_ToMethodInvoke () {}

    public Je_1_Cast_ToMethodInvoke foo() {
	return null;
    }

    public static int test() {
	Je_1_Cast_ToMethodInvoke x = null;
	Object y = (x.foo()) x;
        return 123;
    }

}
// JOOS1:PARSER_WEEDER,INVALID_SOURCE_FILE_NAME
// JOOS2:PARSER_WEEDER,INVALID_SOURCE_FILE_NAME
// JAVAC:UNKNOWN
// 
public class WrongName {
    
    public WrongName(){}

}
// JOOS1:PARSER_WEEDER,INVALID_SOURCE_FILE_NAME
// JOOS2:PARSER_WEEDER,INVALID_SOURCE_FILE_NAME
// JAVAC:UNKNOWN
// 
public class Je_1_ClassDeclaration_WrongFileName_Dot {
	public Je_1_ClassDeclaration_WrongFileName_Dot() {}
	
	public static int test() {
		return 123;
	}
}
// JOOS1:PARSER_WEEDER,INVALID_SOURCE_FILE_NAME
// JOOS2:PARSER_WEEDER,INVALID_SOURCE_FILE_NAME
// JAVAC:UNKNOWN
// 
/**
 * Parser/weeder:
 * - A class declaration must reside in a .java source file with the same
 * base name as the class.
 **/
public class Suffix{

    public Suffix(){}

    public static int test(){
	return 123;
    }
}
// JOOS1:PARSER_WEEDER,PARSER_EXCEPTION
// JOOS2:PARSER_WEEDER,PARSER_EXCEPTION
// JAVAC:UNKNOWN
/**
 * Parser/weeder:
 * - A PType node in an extends clause, implements clause, throws
 * clause or class instantiation expression must be an ANamedType
 */
public class Je_1_ClassInstantiation_InstantiateSimpleType {

    public Je_1_ClassInstantiation_InstantiateSimpleType() { }

    public static int test() { 
	new boolean();
	return 123; 
    }

}
// JOOS1:PARSER_WEEDER,PARSER_EXCEPTION
// JOOS2:PARSER_WEEDER,PARSER_EXCEPTION
// JAVAC:UNKNOWN
/**
 * Parser/weeder:
 * - A PType node in an extends clause, implements clause, throws
 * clause or class instantiation expression must be an ANamedType
 */
public class Je_1_ClassInstantiation_InstantiateSimpleValue {

    public Je_1_ClassInstantiation_InstantiateSimpleValue() { }

    public static int test() { 
	new 1();
	return 123; 
    }

}
// PARSER_WEEDER
// JOOS1:PARSER_EXCEPTION
// JOOS2:PARSER_EXCEPTION
// JAVAC:
/**
 * Parser/weeder:
 * - Multiple variable in same declaration not allowed. 
 */
public class Je_1_Declarations_MultipleVars {

    public Je_1_Declarations_MultipleVars() {}

    public static int test() {
	int i=0, j=10;
	return 123;
    }

}
// PARSER_WEEDER
// JOOS1:PARSER_EXCEPTION
// JOOS2:PARSER_EXCEPTION
// JAVAC:
/**
 * Parser/weeder:
 * - Multiple variables in same declaration not allowed. 
 */
public class Je_1_Declarations_MultipleVars_Fields {

    public int x,y,z;
    
    public Je_1_Declarations_MultipleVars_Fields() {}
    
    public static int test() {
	return 123;
    }
}

