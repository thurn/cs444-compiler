// JOOS1:PARSER_WEEDER,PARSER_EXCEPTION
// JOOS2:PARSER_WEEDER,PARSER_EXCEPTION
// JAVAC:UNKNOWN
// 
/**
 * Parser/weeder:
 * - A PType node in an extends clause, implements clause, throws
 * clause or class instantiation expression must be an ANamedType
 */
public class Je_1_Extends_NamedTypeArray extends Object[] {

    public Je_1_Extends_NamedTypeArray() {}

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
public class Je_1_Extends_SimpleType extends int {

    public Je_1_Extends_SimpleType() {}
    
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
public class Je_1_Extends_SimpleTypeArray extends int[] {

    public Je_1_Extends_SimpleTypeArray() {}

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
 * - Values cannot be extended
 */
public class Je_1_Extends_Value extends 4 {

    public Je_1_Extends_Value() { }

    public static int test() { 
	return 123; 
    }

}
// PARSER_WEEDER
// JOOS1:PARSER_EXCEPTION,JOOS1_FINAL_FIELD_DECLARATION
// JOOS2:PARSER_EXCEPTION,MISSING_FINAL_FIELD_INITIALIZER
// JAVAC:UNKNOWN
/**
 * Parser/weeder:
 * - (Joos 1) No final field declarations allowed,
 * - (Joos 2) A final field must have an initializer.
 */
public class Je_1_FinalField_NoInitializer {

    public final int a;
    
    public Je_1_FinalField_NoInitializer() {}
    
    public static int test() {
        return 123;
    }
}
// JOOS1:PARSER_WEEDER,PARSER_EXCEPTION,SYNTAX_ERROR
// JOOS2:PARSER_WEEDER,PARSER_EXCEPTION,SYNTAX_ERROR
// JAVAC:UNKNOWN
// 
/**
 * Parser/weeder:
 * - Declarations not allowed in for update
 */
public class Je_1_For_DeclarationInUpdate {

    public Je_1_For_DeclarationInUpdate() {}

    public static int test() {
	for (int i=0; i<10; int j=i) {}
	return 123;
    }

}
// PARSER_WEEDER
// JOOS1: PARSER_EXCEPTION,SYNTAX_ERROR
// JOOS2: PARSER_EXCEPTION,SYNTAX_ERROR
// JAVAC: 
/**
 * Parser/weeder:
 * - Multiple declarations not allowed in for initializer.
 */
public class Je_1_For_MultipleDeclarationsInInit{

    public Je_1_For_MultipleDeclarationsInInit(){}

    public static int test(){
	for (int i = 0, j = 10; i < j; i = i + 1){}
	return 123;
    }
}
// PARSER_WEEDER
// JOOS1: PARSER_EXCEPTION,SYNTAX_ERROR
// JOOS2: PARSER_EXCEPTION,SYNTAX_ERROR
// JAVAC: 
/**
 * Parser/weeder:
 * - Multiple expressions not allowed in for update
 */
public class Je_1_For_MultipleUpdates{

    public Je_1_For_MultipleUpdates(){}

    public static int test(){
	for (int i = 0; i < 10; i = i + 1, i = i + 2){}
	return 123;
    }
}
//JOOS1:PARSER_WEEDER,PARSER_EXCEPTION,SYNTAX_ERROR
//JOOS2:PARSER_WEEDER,PARSER_EXCEPTION,SYNTAX_ERROR
//JAVAC:UNKNOWN

public class Je_1_For_NotAStatementInUpdate {
	public Je_1_For_NotAStatementInUpdate() {}
	public static int test() {
		for (boolean b=false;b;true||true);
		return 123;
	}
}

// JOOS1:PARSER_WEEDER,PARSER_EXCEPTION,SYNTAX_ERROR
// JOOS2:PARSER_WEEDER,PARSER_EXCEPTION,SYNTAX_ERROR
// JAVAC:UNKNOWN
// 
/**
 * Parser/weeder:
 * - Primary expression not allowed in init clause of for loop
 */
public class Je_1_For_PrimaryExpInInit {

    public Je_1_For_PrimaryExpInInit() {}

    public static int test() {
	int x = 0;
	for (7; x<10; x=x+1) {}
	return 123;
    }

}
// JOOS1:PARSER_WEEDER,PARSER_EXCEPTION,SYNTAX_ERROR
// JOOS2:PARSER_WEEDER,PARSER_EXCEPTION,SYNTAX_ERROR
// JAVAC:UNKNOWN
// 
/**
 * Parser/weeder:
 * - Primary expression not allowed in update clause of for loop
 */
public class Je_1_For_PrimaryExpInUpdate {

    public Je_1_For_PrimaryExpInUpdate() {}

    public static int test() {
	int x = 0;
	for (x=1; x<10; 42) { }
	return 123;
    }

}
//JOOS1:PARSER_WEEDER,PARSER_EXCEPTION,SYNTAX_ERROR
//JOOS2:PARSER_WEEDER,PARSER_EXCEPTION,SYNTAX_ERROR
//JAVAC:UNKNOWN

public class Je_1_For_StatementInInit {
	public Je_1_For_StatementInInit() {}
	
	public static int test() {
		int a = 1;
		int i = 1;
		for (if (a == 2) i = 2; i < 2 ; i = i + 1) {
			a = 123;
		}
		return a;
	}
}
// PARSER_WEEDER
// JOOS1:PARSER_EXCEPTION,SYNTAX_ERROR
// JOOS2:PARSER_EXCEPTION,SYNTAX_ERROR
// JAVAC:
/**
 * Parser/weeder:
 * - Formal parameters must not be final
 */
public class Je_1_Formals_Final {

    public Je_1_Formals_Final() {}

    public int m(final int x) {
	return 123;
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
 * - A formal parameter must not have an initializer.
 */
public class Je_1_Formals_Initializer_Constructor {

    public Je_1_Formals_Initializer_Constructor(int abc=123) {}

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
 * - A formal parameter must not have an initializer.
 */
public class Je_1_Formals_Initializer_Method {

    public Je_1_Formals_Initializer_Method() {}

    public static int test(int i = 123) {
	return 123;
    }
}
public class Je_1_Identifiers_Private {

    public Je_1_Identifiers_Private() {}

    public static int test() {
	int privat = 0;
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
public class Je_1_Implements_NamedTypeArray implements Object[] {

    public Je_1_Implements_NamedTypeArray() {}

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
public class Je_1_Implements_SimpleType implements int {

    public Je_1_Implements_SimpleType() {}

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
public class Je_1_Implements_SimpleTypeArray implements int[] {

    public Je_1_Implements_SimpleTypeArray() {}

    public static int test() {
	return 123;
    }

}

