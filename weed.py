#!/usr/bin/env python2.6
from util import error_if, onein, allin, modifiers
import re


def weed(tree, filename):
    """Weeds the AST tree.  If the tree is invalid, throws an exception."""
    fn = re.match("(?:.*/)*([^/]*).java", filename).groups(1)[0]
    check_methods(tree)
    check_classes(tree, fn)
    check_fields(tree)
    check_dims(tree)
    check_interfaces(tree, fn)


def check_cast_target(element):
    valid_cast_targets = ['name', 'primitive_type', 'class_or_interface_type']
    if element.tag == 'expression' and len(list(element)) == 1:
        if element[0].tag == 'name' or element[0].tag == 'qualified_name':
            return True
    elif element.tag in valid_cast_targets:
        return True
    return False


def check_casts(tree):
    for cast in tree.findall(".//cast_expression"):
        children = list(cast)
        error_if(children[0].tag != 'tok_l_parenthese',
                 'Malformed cast opening.')
        error_if(not check_cast_target(children[1]), 'Cast target invalid.')
        error_if(not ((children[2].tag == 'dims' and
                    children[3].tag == 'tok_r_parenthese')
        or children[2].tag == 'tok_r_parenthese'), 'Malformed cast closing.')


def check_methods(tree):
    for method in tree.findall(".//method"):
        for modifier_list in method.findall(".//block//modifiers"):
            error_if(onein(["private", "public", "protected", "final"],
                        modifiers(modifier_list)),
                  "local variables cannot be private/public/protected/final.")

        for lvar in tree.findall(".//local_variable_declaration"):
            error_if(lvar.find(".//expression") is None and lvar.find(
                    ".//array_initializer") is None,
                  "Cannot have uninitialized local var declaration.")

        mods = modifiers(method)

        error_if("private" in mods, "private methods disallowed in joos.")
        error_if(allin(["static", "final"], mods),
              "#A static method cannot be final.")
        error_if("native" in mods and not "static" in mods,
              "#A native method must be static.")
        error_if("abstract" in mods and onein(["static", "final"], mods),
              "#An abstract method cannot be static or final.")

        if "abstract" in mods or "native" in mods:
            error_if(method.find(".//block") is not None,
                  "#A method has a body if and only if it is neither " +
                  "abstract nor native.")
        else:
            error_if(method.find(".//block") is None,
                  "A method has a body if and only if it is neither " +
                  "abstract nor native.")

        error_if(not onein(["public", "protected", "private"], mods),
              "A method cannot be package-private")
        error_if(tree.find(".//param//tok_final") is not None,
              "A formal parameter cannot be final.")


def check_classes(tree, filename):
    for clazz in tree.findall(".//class"):
        mods = modifiers(clazz)
        error_if(allin(["abstract", "final"], mods),
              "A class cannot be both abstract and final")
        error_if(not onein(["public", "protected", "private"],
                           modifiers(clazz)),
              "A class cannot be package-private")
        name = clazz.get("name")
        error_if(name != filename, "Class must have same name as file.")


def check_fields(tree):
    for field_declaration in tree.findall(".//field"):
        mods = modifiers(field_declaration)

        error_if("private" in mods, "Fields cannot be private.")
        error_if("final" in mods and not field_declaration.find(
                "field_initializer"),
              "Final fields need a initializer.")
        error_if(not onein(["public", "protected", "private"], mods),
              "A field cannot be package-private")


def check_literals(tree):
    integer_literals = tree.findall(".//integer_literal")
    minus_expr = [x for x in tree.findall(".//unary_expression")
                  if x.getchildren()[0].tag == "tok_minus"]
    minus_literals = []
    for minus in minus_expr:
        if minus.find("./integer_literal") is not None:
            minus_literals += minus.findall(".//integer_literal")
    for literal in integer_literals:
        error_if((not literal in minus_literals) and
              int(literal.get("value")) >= 2 ** 31,
              "Integer literal too large")

    complement_expr = [x for x in
                       tree.findall(".//unary_expression_not_plus_minus")
                       if x.getchildren()[0].tag == "tok_complement" or
                          x.getchildren()[0].tag == "tok_bit_complement"]
    for tag in complement_expr:
        error_if(tag.find("./integer_literal") is not None,
              "Bit complement not allowed.")


def check_dims(tree):
    if tree.findall(".//dim_expr//tok_null"):
        error_if(True, "Null cannot appear in a dim expr")


def check_interfaces(tree, filename):
    for interface in tree.findall(".//interface"):
        name = interface.get("name")
        error_if(name != filename, "interface must have same name as file.")
        for method in interface.findall(".//abstract_method"):
            mods = modifiers(method)
            error_if(onein(["static", "final", "native"], mods),
                  "An interface method cannot be static, final, or native.")
