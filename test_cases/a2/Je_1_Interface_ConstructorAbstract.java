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
