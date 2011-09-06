// PARSER_WEEDER,CODE_GENERATION
public class J1_01 {
    public J1_01() {}
    public static int test() {
        int r1 = J1_01.m0(0);
        int r2 = J1_01.m0(1);
        int r3 = J1_01.m0(100);
        int r4 = J1_01.m1(0);
        int r5 = J1_01.m1(1);
        int r6 = J1_01.m1(100);

        int r = 0;
        if (r1==9) r=r+1;
        if (r2==6) r=r+1;
        if (r3==6) r=r+1;

        if (r4==6) r=r+1;
        if (r5==9) r=r+1;
        if (r6==6) r=r+1;

        return 117+r;
    }

    public static int m0(int a) {
        int r = 0;
        if (a==0) r=r+1;
        if (a!=0) r=r+2;
        if (!(a==0)) r=r+4;
        if (!(a!=0)) r=r+8;
        return r;
    }

    public static int m1(int a) {
        int r = 0;
        if (a==1) r=r+1;
        if (a!=1) r=r+2;
        if (!(a==1)) r=r+4;
        if (!(a!=1)) r=r+8;
        return r;
    }
}
// PARSER_WEEDER
/**
 * This method is supposed to test whether access to the resulting
 * objects of method calls are parsed correctly.
 **/
public class J1_1_AmbiguousName_AccessResultFromMethod{

    public int i;

    public J1_1_AmbiguousName_AccessResultFromMethod(int j){
        i = j;
    }

    public J1_1_AmbiguousName_AccessResultFromMethod inc(){
        return new J1_1_AmbiguousName_AccessResultFromMethod(i+1);
    }

    public static int test(){
        return new J1_1_AmbiguousName_AccessResultFromMethod(120).inc().inc().inc().i;
    }

}

// PARSER_WEEDER
/**
 * Parser/weeder
 * - Cast of complement expression
 */
public class J1_1_Cast_Complement{
        
    public J1_1_Cast_Complement(){}
        
    public static int test(){

        boolean t = true;
        boolean b = (boolean)!t;
        if (b){
            return 124733;
        }
        else {
            return 123;
        }
    }
        
}



// PARSER_WEEDER
public class J1_1_Cast_MultipleCastOfSameValue_1{

    public J1_1_Cast_MultipleCastOfSameValue_1 () {}

    public static int test() {
        Object a = new Object();
        a = (Object) (Object) a;
        return 123;
    }

}
// PARSER_WEEDER
public class J1_1_Cast_MultipleCastOfSameValue_2{

    public J1_1_Cast_MultipleCastOfSameValue_2 () {}

    public static int test() {
        Object a = new Object();
        a = (Object) ((Object) a);
        return 123;
    }

}
// PARSER_WEEDER
public class J1_1_Cast_MultipleCastOfSameValue_3{

    public J1_1_Cast_MultipleCastOfSameValue_3 () {}

    public static int test() {
        Object a = new Integer(0);
        a = (Object) (Number) (Integer) a;
        return 123;
    }

}
//PARSER_WEEDER
public class J1_1_Cast_MultipleReferenceArray {
        public J1_1_Cast_MultipleReferenceArray() {}

        public static int test() {
                Object a = null;
                a = (Object)(int[])(Object)(Integer[])a;
                return 123;
        }
}

// PARSER_WEEDER
public class J1_char {
    public J1_char() {}
    protected char x = (char)123;
    public static int test() {
	J1_char obj = new J1_char();
	char y = obj.x;
	return (int)y;
    }
}

// PARSER_WEEDER
public class J1_char_escape {
    public J1_char_escape() {}
    public static int test() {
	int r = 107;

	if ('\b' == 8) r=r+1;
	if ((int)("\b".charAt(0)) == 8) r=r+1;

	if ('\t' == 9) r=r+1;
	if ((int)("\t".charAt(0)) == 9) r=r+1;

	if ('\n' == 10) r=r+1;
	if ((int)("\n".charAt(0)) == 10) r=r+1;

	if ('\f' == 12) r=r+1;
	if ((int)("\f".charAt(0)) == 12) r=r+1;

	if ('\r' == 13) r=r+1;
	if ((int)("\r".charAt(0)) == 13) r=r+1;

	if ('\"' == 34) r=r+1;
	if ((int)("\"".charAt(0)) == 34) r=r+1;

	if ('\'' == 39) r=r+1;
	if ((int)("\'".charAt(0)) == 39) r=r+1;

	if ('\\' == 92) r=r+1;
	if ((int)("\\".charAt(0)) == 92) r=r+1;

	return r;
    }
}
// PARSER_WEEDER
public class J1_char_escape2 {
    public J1_char_escape2() {}
    public static int test() {
	int r = 0;
	if (J1_char_escape2.eq("\\b",   ((char)92+"b"))) r=r+1;
	if (J1_char_escape2.eq("\\f",   (char)92+"f")) r=r+1;
	if (J1_char_escape2.eq("\\n",   (char)92+"n")) r=r+1;
	if (J1_char_escape2.eq("\\r",   (char)92+"r")) r=r+1;
	if (J1_char_escape2.eq("\\'",   (char)92+"'")) r=r+1;
	if (J1_char_escape2.eq("'\\\'", "'"+(char)92+"'")) r=r+1;
	if (J1_char_escape2.eq("'\\\"", "'"+(char)92+(char)34)) r=r+1;
	return r+116;
    }
    public static boolean eq(String a, String b) {return a.equals((Object)b);}
}

