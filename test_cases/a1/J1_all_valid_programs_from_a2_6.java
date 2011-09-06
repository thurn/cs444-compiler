// PARSER_WEEDER
public class J1_intliterals {
    public J1_intliterals() {}
    public static int test() {
	return 123;
    }
}
// PARSER_WEEDER
public class J1_intminusfoo {
    public J1_intminusfoo(){}

    public static int test() {
	int foo = -123;
	return (int)-foo;    
    }
}
// PARSER_WEEDER
public class J1_lazybooleanoperations {
    public J1_lazybooleanoperations() {}
    public static int test() {
	boolean x = true;
	boolean y = (x && true) || x;
	return 123;
    }
}
// PARSER_WEEDER
public class J1_maxint_comment {
    public /*one*/J1_maxint_comment/*two*/(/*three*/)/*four*/{/*five*/}

    protected int huge = -/*helo?*/2147483648/*hello!*/;
    public static int test() {return new J1_maxint_comment().test2();}
    public int test2() {
	int gargantuan = -/*word?*/2147483648/*world!*/;
	return (huge+123-gargantuan);
    }

}
// PARSER_WEEDER,CODE_GENERATION
public class J1_minuschar {
    public J1_minuschar() {}
    public static int test() {return - - '{';}
}
// PARSER_WEEDER,CODE_GENERATION
public class J1_minusminusminus {

    public J1_minusminusminus() {}

    public static int test() {
	int x = - - - -123;
	return x;
    }

}
// PARSER_WEEDER,CODE_GENERATION
public class J1_negativeintcast3 {

    public J1_negativeintcast3() {}

    public static int test() {
	return -(int)-123;
    }

}
// PARSER_WEEDER
public class J1_newobject {

    public J1_newobject() {}

    public static int test() {
	return 123;
    }

}
// PARSER_WEEDER
public class J1_nonemptyconstructor {

    public J1_nonemptyconstructor () {
	String s = "123";
    }

    public static int test() {
        return 123;
    }

}
// PARSER_WEEDER,TYPE_CHECKING
public class J1_nullinstanceof1 {
	public J1_nullinstanceof1() { }
	public static int test() {
		if (null instanceof Object)
			return 100;
		else
			return 123;
	}
}
// PARSER_WEEDER
public class J1_nullliteral {
    public J1_nullliteral() {}
    public static int test() {
	Object o = null;
	return 123;
    }
}
// PARSER_WEEDER
public class J1_octal_escape {
    public J1_octal_escape() {}
    public static int test() {return 3*(int)'\051';}
}
// PARSER_WEEDER
public class J1_octal_escape2 {
    public J1_octal_escape2() {}
    public static int test() {return (int)'\173';}
}
// PARSER_WEEDER
public class J1_octal_escape3 {
    public J1_octal_escape3() {}
    public static int test() {return (int)'\7'+(int)'\77'+53;}
}
// PARSER_WEEDER
public class J1_octal_escape4 {
    public J1_octal_escape4() {}
    public static int test() {
	String s = "\3\20\100(";
	int r = 0;
	for (int i=0; i<s.length(); i=i+1) r=r+(int)s.charAt(i);
	return r;
    }
}
// PARSER_WEEDER
public class J1_octal_escape5 {
    public J1_octal_escape5() {}
    public static int test() {
	String s = "\421abc\2400xyz\377\19\400";
	String s2 = (char)34 + "1abc" + (char)160 + "0xyz" + (char)255 + (char)1 + "9 0";
	if (s.equals((Object)s2)) return 123;
	else return 0;
    }
}
// PARSER_WEEDER,TYPE_CHECKING
public class J1_primitivecasts {
  public J1_primitivecasts() {}
  public static int test() {
      boolean t = (boolean)true;
      char c = (char)'y';
      short s = (short)17;
      byte b = (byte)5;
      return (int)123;
  }
}
// PARSER_WEEDER
public class J1_protected {

    protected int i;

    public J1_protected () {}

    public static int test() {
        return 123;
    }

}
// PARSER_WEEDER
public class J1_protectedfields {
    public J1_protectedfields() {}
    protected int x;
    public static int test() {
	return 123;
    }
}
// PARSER_WEEDER
public class J1_publicclasses {
    public J1_publicclasses() {}
    public static int test() {
	return 123;
    }
}
// PARSER_WEEDER
public class J1_publicconstructors {
    public J1_publicconstructors() {}
    public static int test() {
	return 123;
    }
}
// PARSER_WEEDER
public class J1_publicfields {
    protected J1_publicfields() {
	this.x = 123;
    }
    public int x;
    public static int test() {
	return new J1_publicfields().x;
    }
}

// PARSER_WEEDER
public class J1_publicmethods {
    public J1_publicmethods() {}
    public int m() {
	return 123;
    }
    public static int test() {
	return new J1_publicmethods().m();
    }
}
// PARSER_WEEDER
public class J1_staticmethoddeclaration {

  public J1_staticmethoddeclaration() {}

  public static int test() {
    return 123;
  }

}
// PARSER_WEEDER
public class J1_stringliteralinvoke {

    public J1_stringliteralinvoke() {}

    public static int test() {
	int len = "HelloWorld".length();
	return len+113;
    }

}
// PARSER_WEEDER
public class J1_stringliterals {
    public J1_stringliterals() {}
    public static int test() {
	String s1 = "";
	String s2 = "123abcABC$%*~";
	return 123;
    }
}
// PARSER_WEEDER
public class J1_weird_chars{

    public J1_weird_chars(){}

    public static int test(){

	String s = "\\b";
	if (s.indexOf("\\") == 0
	    && s.indexOf("b") == 1
	    && s.indexOf("\b") == -1
	    && s.length() == 2) {
		return 123;
	}

	return 42;
    }
}
public interface J1w_Interface {}
public class J1w_RestrictedNative {
    public J1w_RestrictedNative() {}
    public static native int m(int i);
}
public class J1w_StaticField {
    public J1w_StaticField() {}
      protected static int x;
}
