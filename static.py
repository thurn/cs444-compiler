#!/usr/bin/env python2.6
from environment import build_envs
from util import error_if, JoosSyntaxException, Testing, name_to_str
import sys

def always_returns(block):
    """Returns whether the method always returns."""
    if block is None:
        return True
    for stmt in block:
        if stmt.tag == "if_then_statement":
            if (always_returns(stmt.find("./then")) and
                always_returns(stmt.find("./else"))):
                return True
        elif stmt.tag == "return_statement":
            return True
        elif stmt.tag == "block":
            if always_returns(stmt):
                return True
        elif stmt.tag in ["while_statement", "for_statement"]:
            if stmt.find("./expression").get("value") == "True":
                return True  # TODO Do we need to recurse here?
    return False


def check_reachability(block):
    """Checks to ensure reachability constraints"""
    fail_next = False
    if block is None:
        return True
    for stmt in block:
        error_if(fail_next, "Unreachable statement")
        if stmt.tag == "block":
            check_reachability(stmt)
        if stmt.tag == "while_statement":
            #A while statement can complete normally iff at least one of the
            #following is true:

            #There is a reachable break statement that exits the while
            #statement.

            #The while statement is reachable and the condition expression is
            #not a constant expression with value true.

            #The contained statement is reachable iff the while statement is
            #reachable and the condition expression is not a constant
            #expression whose value is false.
            if stmt.find("./expression").get("value") == "True":
                fail_next = True
            check_reachability(stmt.getchildren()[-1])
            error_if(stmt.find("./expression").get("value") == "False",
                  "Unreachable while")

        if stmt.tag == "for_statement":
            #A basic for statement can complete normally iff at least one of
            #the following is true:

            #The for statement is reachable, there is a condition expression,
            #and the condition expression is not a constant expression with
            #value true.
            if stmt.find("./expression").get("value") == "True":
                fail_next = True
            error_if(stmt.find("./expression").get("value") == "False",
                  "unreachable For")
        if stmt.tag in ["return_statement"]:
            fail_next = True
            pass
        if stmt.tag == "if_then_statement":
            check_reachability(stmt.find(".//then"))
            check_reachability(stmt.find(".//else"))
            if (always_returns(stmt.find("./then")) and
                always_returns(stmt.find("./else"))):
                fail_next = True
        #labeled exception
    pass


def check(files):
    try:
        trees = build_envs(files)
        #All statements must be reachable. Details of the exact definition of
        #reachability are specified in Section 14.20 of the Java Language
        #Specification.
        for tree in trees:
            for block in (tree.findall(".//method/block") +
                          tree.findall(".//constructor_body")):
                check_reachability(block)
            for method in tree.findall(".//method"):
                if method.find(".//tok_void") is None:
                    returns = always_returns(method.find("block"))
                    error_if(not returns,
                          "Doesn't always return from nonvoid method")

        #Every local variable must have an initializer, and the variable must
        #not occur in its own initializer.
        for tree in trees:
            for lvar in tree.findall(".//local_variable_declaration"):
                name = lvar.find(".//variable/tok_identifier").text
                error_if(lvar.find(".//expression") is None,
                      "Every local variable must have an initializer")
                for ident in lvar.findall(".//expression//name"):
                    error_if(name == name_to_str(ident),
                          "Self cannot appear in local variable initializer.")
        return 0
    except JoosSyntaxException, e:
        if not Testing.testing:
            print e.msg
        return 42

if __name__ == '__main__':
    sys.exit(check(sys.argv[1:]))
