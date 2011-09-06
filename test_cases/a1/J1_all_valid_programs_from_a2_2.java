
// PARSER_WEEDER
public class J1_IntCharInit {

    public J1_IntCharInit(){}

	public static int test() {
		int x = '*';
		return x + 81;
	}
}

// PARSER_WEEDER
public class J1_IntInit {

    public J1_IntInit(){}

	public static int test() {
		int x = 123456;
		return x - 123333;
	}
}

// PARSER_WEEDER
public class J1_IntRange_MinNegativeInt {

    public J1_IntRange_MinNegativeInt () {}
    // http://www.jroller.com/comments/slava/Weblog/pitfalls_of_2_s_complement

    public static int test() {
	if ((-(-2147483648)) == (-2147483648))
	    return 123;
	return 7;
    }

    public static void main(String[] args) {
	System.out.println(J1_IntRange_MinNegativeInt.test());
    }

}
// PARSER_WEEDER
public class J1_IsThisACast {

    public J1_IsThisACast () {}

    public static int test () {

	int J1_IsThisACast = 654;
	return (J1_IsThisACast)-531;
    }
}
// PARSER_WEEDER,CODE_GENERATION
public class J1_NamedTypeArray {

    public J1_NamedTypeArray(){}

	public static int test(){
		J1_NamedTypeArray[] a = new J1_NamedTypeArray[5];
		if (a[4] == null) {
			return 123;
		}
		return 444;
	}
}

// PARSER_WEEDER,CODE_GENERATION
public class J1_NegativeByteCast {

    public J1_NegativeByteCast(){}

       public static int test() {

	   return (byte)-123456 + 187;
       }
}
// PARSER_WEEDER,CODE_GENERATION
public class J1_NegativeCharCast {

    public J1_NegativeCharCast(){}

       public static int test() {

	   return (char)-123456 - 7493;
       }
}
// PARSER_WEEDER,CODE_GENERATION
public class J1_NegativeIntCast1 {

    public J1_NegativeIntCast1(){}

       public static int test() {

	   return (int)-456123 + 456246;
       }
}

// PARSER_WEEDER,CODE_GENERATION
public class J1_NegativeIntCast2 {

    public J1_NegativeIntCast2(){}

       public static int test() {

	   return 456246 + (int)-456123;
       }
}

// PARSER_WEEDER,CODE_GENERATION
public class J1_NegativeOneByteByteCast {

    public J1_NegativeOneByteByteCast(){}

       public static int test() {

	   return (byte)-123 + 246;
       }
}

// PARSER_WEEDER,CODE_GENERATION
public class J1_NegativeOneByteCharCast {
    
    public J1_NegativeOneByteCharCast(){}
    
    public static int test() {
	return (char)-123 - 65290;
    }
}

// PARSER_WEEDER,CODE_GENERATION
public class J1_NegativeOneByteIntCast {

    public J1_NegativeOneByteIntCast(){}

       public static int test() {

	   return (int)-123 + 246;
       }
}

// PARSER_WEEDER,CODE_GENERATION
public class J1_NegativeOneByteShortCast {

    public J1_NegativeOneByteShortCast(){}

       public static int test() {

	   return (short)-123 + 246;
       }
}

// PARSER_WEEDER,CODE_GENERATION
public class J1_NegativeShortCast {

    public J1_NegativeShortCast(){}

       public static int test() {

	   return (short)-123456 - 7493;
       }
}

// PARSER_WEEDER,CODE_GENERATION
public class J1_SimpleTypeArray {

    public J1_SimpleTypeArray(){}

	public static int test(){
		boolean[] a = new boolean[5];
		if (a[4] == false){
			return 123;
		}
		return 444;
	}
}

// PARSER_WEEDER,CODE_GENERATION
public class J1_SmallInt {

    public J1_SmallInt(){}

       public static int test() {

	   return -2147483648 + 2147483000 + 771;
       }
}

// PARSER_WEEDER
public abstract class J1_abstractclass {

    public J1_abstractclass() {}

    public static int test() {
	return 123;
    }
    
}
// PARSER_WEEDER
public abstract class J1_abstractmethodwithoutbody {

    public J1_abstractmethodwithoutbody() {}

    public abstract void flimflam();

    public static int test() {
	return 123;
    }

}
// PARSER_WEEDER,ENVIRONMENTS
public class J1_arbitrarylocaldeclaration {
    public static int test() {
	return new J1_arbitrarylocaldeclaration().m();
    }
    public J1_arbitrarylocaldeclaration() {}
    public int m() {
	int x = 35;
	x = x+1;
	int y = x+87;
	return y;
    }
}
// PARSER_WEEDER,CODE_GENERATION
public class J1_arithmeticoperations {
    public J1_arithmeticoperations() {}
    public static int test() {
	int x = 17;
	int y = -2*x+87%x-(x/7);
	return x+106;
    }
}
// PARSER_WEEDER
public class J1_assignment {

    public J1_assignment() {}

    public static int test() {
	int i = 123;
	return i;
    }
}
// PARSER_WEEDER
public class J1_assignmentExp {

    public J1_assignmentExp() {}

    public static int test() {
	int i = 1*100+2*10+3;
	return i;
    }

}
// PARSER_WEEDER
public class J1_barminusfoo {
    public J1_barminusfoo(){}

    public static int test() {
	int foo = -123;
	int bar = 0;
	return (bar)-foo;
    }
}

