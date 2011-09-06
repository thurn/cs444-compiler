#!/usr/bin/env python2.6
from environment import build_envs
from util import error_if, JoosSyntaxException, CurrentFile, \
    is_primitive, is_integral_primitive, isarray, argument_list, \
    Testing, isvariable
from util import modifiers, name_to_str, type_string, collect_token_text, to_file
import sys
from elementtree.ElementTree import dump

def check_files(files):
    trees = build_envs(files)
    for tree in [x for x in trees if not hasattr(x, "typechecked")]:
        CurrentFile.name = tree.filename
        populate_environment(tree)
    for tree in [x for x in trees if not hasattr(x, "typechecked")]:
        CurrentFile.name = tree.filename
        typecheck(tree)
        typecheck_other_conditions(tree)
        check_field_initializers(tree)
        tree.typechecked = True
    return trees


def typecheck_files(files):
    """Takes a list of filenames and verifies that the corresponding source
    files typecheck. Prints an error message an exits with return code 42 if
    they do not."""
    try:
        check_files(files)
        return 0
    except JoosSyntaxException, e:
        if not Testing.testing:
            print e.msg
            raise
        return 42


def typecheck_other_conditions(tree):
    """Takes an abstract syntax tree which has Environments associated with it
    and typechecks it. Raises JoosSyntaxException if the tree does not
    typecheck."""
    # A constructor in a class other than java.lang.Object implicitly calls the
    # zero-argument constructor of its superclass. Check that this
    # zero-argument constructor exists.
    #
    # Check that the name of a constructor is the same as the name of its
    # enclosing class.

    for ctor in tree.findall(".//constructor_declaration"):
        clazz = ctor.env.findclass(ctor.get("name"))
        superclazz = clazz.superclass
        error_if(not superclazz.env.find_constructor(tuple([])),
              "No zero-argument constructor")

    for lhs in tree.findall(".//assignment/left_hand_side"):
        if lhs.find("./name") is None:
            continue
        type_name = name_to_str(lhs.find("./name"))
        type_decl = lhs.env.get_declaration_site_for_variable_name(type_name, lhs.find("./name"))

        error_if("final" in modifiers(type_decl),
              "Final field on LHS")

    #Check that no objects of abstract classes are created.
    for expr in tree.findall(".//class_instance_creation_expression"):
        expr_type = name_to_str(expr.find("./name"))
        instantiated_class = tree.env.findclass(expr_type)

        error_if("abstract" in modifiers(instantiated_class) or
              instantiated_class.tag == "interface",
              "Cannot instantiate abstract classes.")

        class_name = instantiated_class.get("canonical_name")
        ctor_decl = expr.env.get_declaration_site_for_constructor_name(
            class_name,
            argument_list(expr))

        error_if(expr.env.find_package_name() !=
                 ctor_decl.env.find_package_name()
                 and "protected" in modifiers(ctor_decl),
              "Invocation of Protected Constructor.")

    # Check that the implicit this variable is not accessed in a static method
    # or in the initializer of a static field.
    for smethod in \
            [x for x in tree.findall(".//method") if "static" in modifiers(x)]:
        error_if(smethod.find(".//tok_this") is not None,
              "Cannot acces this in static method.")
    for field in \
            [x for x in tree.findall(".//field") if "static" in modifiers(x)]:
        error_if(field.find(".//tok_this") is not None,
              "Cannot acces this in static field.")

    #if_then_stmts = tree.find(".//if_then_statement/expression//assignment")
    #error_if(if_then_stmts is not None,
           #"No assignment in if_then expressions")
    while_stmts = tree.find(".//while_statement/expression//assignment")
    #error_if(while_stmts is not None,
           #"No assignment in if_then expressions")


def assign_simple_type(type_string):
    def result(x):
        x.attrib["type"] = type_string
    return result


def bubble_or_resolve_child_type(function):
    def result(element):
        if len(element) == 1:
            if element[0].tag == "name" or element[0].tag == "qualified_name":
                name_string = name_to_str(element[0])
                declaration_site = \
                    element.env.get_declaration_site_for_variable_name(
                    name_string,
                    element[0])
                type_string = \
                    declaration_site.env.get_type_for_declaration_site(
                    declaration_site)
                element.attrib["type"] = type_string
                element[0].attrib["type"] = type_string
            elif element[0].tag == "tok_this":
                element.attrib["type"] = element.env.canonicalize_name("this")
                element[0].declaration = element.env.findclass("this")
            else:
                element.attrib["type"] = element[0].attrib["type"]
        else:
            function(element)
    return result


def binary_expression(expected_type_string):
    @bubble_or_resolve_child_type
    def result(element):
        lhs_type = element.env.canonicalize_name(type_string(element[0]))
        rhs_type = element.env.canonicalize_name(type_string(element[2]))
        if is_integral_primitive(lhs_type) and is_integral_primitive(rhs_type):
            element.attrib["type"] = "int"
            return
        error_if(lhs_type != rhs_type != expected_type_string,
              "binary_expression type mismatch")
        element.attrib["type"] = expected_type_string
    return result


@bubble_or_resolve_child_type
def relational_expression(element):
    lhs_type = element.env.canonicalize_name(element[0].attrib['type'])
    rhs_type = element.env.canonicalize_name(element[2].attrib['type'])
    if element[1].text in ["<", ">", "<=", ">="]:
        error_if(not (is_integral_primitive(lhs_type) and
                   is_integral_primitive(rhs_type)),
              "Relational expression passed non-integral types.")
    elif element[1].text == "instanceof":
        error_if(is_primitive(lhs_type) or is_primitive(rhs_type),
               "Cannot have primitives in instanceof")
    element.attrib["type"] = "boolean"


@bubble_or_resolve_child_type
def unary_expression(element):
    if len(element) == 2:
        # Unary minus.
        if element[0].tag == "tok_minus":
            error_if(not is_integral_primitive(element[1].attrib["type"]),
                     "must negate integral primitive")
            element.attrib["type"] = element[1].attrib["type"]
        if element[0].tag == "tok_complement":
            error_if(element[1].attrib["type"] != "boolean", "must !boolean")
            element.attrib["type"] = element[1].attrib["type"]



@bubble_or_resolve_child_type
def cast_expression(element):
    if element[1].tag == "name":
        expression_being_cast = element.find("unary_expression_not_plus_minus")
        cast_type = element.env.canonicalize_name(name_to_str(element[1]))
        if element.find("dims"):
            cast_type += "[]"
    elif element[1].tag == "expression":
        # Expression case
        cast_type = element[1].attrib["type"]
        expression_being_cast = element[-1]
    else:
        # Primitive cast case
        cast_type = collect_token_text(element[1])
        if element[2].tag == "dims":
            cast_type += "[]"
        expression_being_cast = element[-1]

    error_if(not element.env.can_be_cast(expression_being_cast.attrib["type"],
                                  cast_type), "TODO(thurn): This is an error.")
    element.attrib["type"] = cast_type


@bubble_or_resolve_child_type
def equality_expression(element):
    lhs_type = element[0].attrib["type"]
    rhs_type = element[2].attrib["type"]
    error_if(not element.env.are_identity_comparable(lhs_type, rhs_type)
          or "void" in [lhs_type, rhs_type],
          "Incompatible types in equality '%s' vs '%s'" % (lhs_type, rhs_type))
    element.attrib["type"] = "boolean"


@bubble_or_resolve_child_type
def additive_expression(element):
    if element[1].tag == 'tok_plus':
        types = [element[0].attrib["type"], element[2].attrib["type"]]
        if "java.lang.String" in types and "void" not in types:
            element.attrib["type"] = "java.lang.String"
        else:
            binary_expression("int")(element)
    elif element[1].tag == 'tok_minus':
        binary_expression("int")(element)


@bubble_or_resolve_child_type
def return_statement(element):
    element.attrib["type"] = element[1].attrib["type"]

def method(element):
    method_type = element.env.canonicalize_name(type_string(element))
    block = element.find("block")
    if block is not None:
        return_statements = block.findall(".//return_statement")
        error_if(len(return_statements) == 0 and method_type != "void",
              "Missing return statement in function not returning void.")
        for return_statement in return_statements:
            return_statement_type = return_statement.attrib["type"]
            if method_type == "void":
                error_if(return_statement_type != "",
                      "Void method returns a value.")
            else:
                error_if(not element.env.is_assignable(method_type,
                                                    return_statement_type),
                      "Cannot return '" + return_statement_type +
                      "' in a method returning '" + method_type + "'")
    element.attrib["type"] = method_type


def is_primitive_variable_declaration_site(element):
    return is_primitive(element.env.get_type_for_declaration_site(element))


def method_invocation(element):
    if element[0].tag == "name":
        name = name_to_str(element.find("name"))
        to_file(element)
        declaration_site = element.env.get_declaration_site_for_method_name(
            name,
            argument_list(element))
        element.attrib["type"] = element.env.get_type_for_declaration_site(
            declaration_site)
        element.declaration = declaration_site
    elif element[0].tag == "primary":
        primary_type = element[0].attrib["type"]
        error_if(is_primitive(primary_type),
              "Cannot invoke method on primitive " + primary_type)
        declaration_site = element.env.get_declaration_site_for_class_name(
            primary_type)
        identifier = element.find("tok_identifier").text
        method_declaration = \
            declaration_site.env.get_declaration_site_for_method_name(
            identifier,
            argument_list(element))
        element.attrib["type"] = \
            method_declaration.env.get_type_for_declaration_site(
            method_declaration)
        element.declaration = method_declaration
    else:
        assert False


@bubble_or_resolve_child_type
def field_access(element):
    primary_type = element[0].attrib["type"]
    error_if(is_primitive(primary_type), "No fields on primitive type.")
    declaration_site = \
        element.env.get_declaration_site_for_class_name(primary_type)
    identifier = element.find("tok_identifier").text
    secondary_site = \
        declaration_site.env.get_declaration_site_for_variable_name(identifier,
                                                                    element.find("tok_identifier"))
    secondary_type = \
        secondary_site.env.get_type_for_declaration_site(secondary_site)
    element.attrib["type"] = secondary_type
    element.declaration = secondary_site


def populate_environment(element, environment=None):
    if not hasattr(element, "env"):
        element.env = environment
    env = element.env
    for child in element:
        populate_environment(child, env)
        if env != child.env:
            env = child.env


def resolve_constructor_name(element):
    return element.env.get_declaration_site_for_constructor_name(
            name_to_str(element.find("name")),
            argument_list(element))

def class_instance_creation(element):
    name = name_to_str(element.find("name"))
    element.attrib["type"] = element.env.canonicalize_name(name)
    resolve_constructor_name(element)


def local_variable_declaration(element):
    assigned_expression = element.find("expression")
    if assigned_expression is not None:
        declaration_type = element.env.get_type_for_declaration_site(element)
        assigned_expression_type = assigned_expression.attrib["type"]
        error_if(not element.env.is_assignable(declaration_type,
                                            assigned_expression_type),
              "Cannot assign type \"" + assigned_expression_type +
              "\" to \"" + declaration_type + "\"")
    element.attrib["type"] = "DANGER"


@bubble_or_resolve_child_type
def bubble_or_resolve(element):
    if "type" in element.attrib:
        return
    error_if(True, "Bubble_or_resolve wrong number of children. " +
                   element.tag)


def assignment(element):
    left_hand_side_type = element.find("left_hand_side").attrib["type"]
    assignment_expression_type = element[-1].attrib["type"]
    error_if(not element.env.is_assignable(left_hand_side_type,
                                        assignment_expression_type),
          "Cannot assign '%s' to '%s'" %
          (assignment_expression_type, left_hand_side_type))
    element.attrib["type"] = left_hand_side_type


def reference_type(element):
    name_string = collect_token_text(element)
    canonical_name = element.env.canonicalize_name(name_string)
    element.attrib["type"] = canonical_name


def array_creation_expression(element):
    base_name = collect_token_text(element[1])
    if element.find(".//dim_expr") is not None:
        base_name += "[]"
    if element.find(".//dim_expr/expression") is not None:
        type_str = element.find(".//dim_expr/expression").attrib["type"]
        error_if(not is_integral_primitive(type_str),
              "dim_expr require integral type")
    element.attrib["type"] = element.env.canonicalize_name(base_name)


def array_access(element):
    if element[0].tag == "name":
        name = name_to_str(element[0])
        decl_site = element.env.get_declaration_site_for_variable_name(name,
                                                                       element[0])
        type_name = element.env.get_type_for_declaration_site(decl_site)
        element.declaration = decl_site
    else:
        type_name = element[0].attrib["type"]
    error_if(not isarray(type_name), "Array access on non-array type.")
    element.attrib["type"] = type_name[:-2]

    index_expression_type = element[-2].attrib["type"]
    error_if(not is_integral_primitive(index_expression_type),
          "Cannot index into array with non-integral expression.")


def control_flow_statement(element):
    error_if(element.find("./expression").attrib["type"] != "boolean",
          "Control Flow expression must have boolean type")
    element.attrib["type"] = ""


def constructor_declaration(element):
    return_statements = element.findall(".//return_statement")
    for return_statement in return_statements:
        return_statement_type = return_statement.attrib["type"]
        error_if(return_statement_type != "", "Void method returns a value.")
    element.attrib["type"] = ""


def typecheck(element):
    """Takes an abstract syntax element which has Environments associated with
    it and typechecks it. Raises JoosSyntaxException if the subtree based at
    the element does not typecheck."""

    for child in element:
        typecheck(child)

    switch = {
        "if_then_statement": control_flow_statement,
        "while_statement": control_flow_statement,
        "while_statement_no_short_if": control_flow_statement,
        "for_statement": control_flow_statement,
        "for_statement_no_short_if": control_flow_statement,
        "primary_no_new_array": bubble_or_resolve,
        "assignment_expression": bubble_or_resolve,
        "shift_expression": bubble_or_resolve,
        "array_creation_expression": array_creation_expression,
        "left_hand_side": bubble_or_resolve,
        "assignment": assignment,
        "local_variable_declaration": local_variable_declaration,
        "field": local_variable_declaration,
        "additive_expression": additive_expression,
        "and_expression": binary_expression("boolean"),
        "boolean_literal": assign_simple_type("boolean"),
        "character_literal": assign_simple_type("char"),
        "class_instance_creation_expression": class_instance_creation,
        "conditional_and_expression": binary_expression("boolean"),
        "conditional_or_expression": binary_expression("boolean"),
        "equality_expression": equality_expression,
        "exclusive_or_expression": binary_expression("boolean"),
        "expression": bubble_or_resolve,
        "field_access": field_access,
        "inclusive_or_expression": binary_expression("boolean"),
        "integer_literal": assign_simple_type("int"),
        "method": method,
        "constructor_declaration": constructor_declaration,
        "method_invocation": method_invocation,
        "multiplicative_expression": binary_expression("int"),
        "null_literal": assign_simple_type("null"),
        "relational_expression": relational_expression,
        "return_statement": return_statement,
        "string_literal": assign_simple_type("java.lang.String"),
        "unary_expression": unary_expression,
        "cast_expression": cast_expression,
        "unary_expression_not_plus_minus": unary_expression,
        "reference_type": reference_type,
        "array_access": array_access,
    }

    if element.tag in switch:
        switch[element.tag](element)
    elif len(element) == 1:
        element.attrib["type"] = element[0].attrib["type"]
    else:
        element.attrib["type"] = ""


def class_qualified_name_for_field(field):
    class_name = field.env.findclass("this").get("name")
    field_name = name_to_str(field.find(".//variable"))
    return class_name + "." + field_name


def static_declaration(declaration):
    return "static" in modifiers(declaration)


def check_field_initializers(tree):
    #Check the rules specified in Section 8.3.2.3 of the Java Language
    #Specification regarding forward references. The initializer of a
    #non-static field must not use (i.e. read) by simple name (i.e. without an
    #explicit this) itself or a non-static field declared later in the same
    #class.

    #The declaration of a member needs to appear before it is used only if the
    #member is an instance (respectively static) field of a class or interface
    #C and all of the following conditions hold:

    #The usage occurs in an instance (respectively static) variable initializer
    #of C or in an instance (respectively static) initializer of C.

    #The usage is not on the left hand side of an assignment.
    #C is the innermost class or interface enclosing the usage.
    fields = tree.findall(".//field")
    for x in xrange(len(fields)):
        field = fields[x]
        forward_references = fields[x:]
        forward_reference_names = []
        for forward_reference in forward_references:
            forward_reference_names.append(
                name_to_str(forward_reference.find(".//variable")))

        potential_elements = set()
        expression_element = field.find("expression")
        if expression_element is not None:
            for child in expression_element.findall(".//name"):
                child_name = name_to_str(child).split(".")[0]
                if child_name in forward_reference_names:
                    potential_elements.add(child)
            valid_references = field.findall(".//left_hand_side/name")
            valid_references += \
                field.findall(".//class_instance_creation_expression/name")
            for child in valid_references:
                for subchild in child.getiterator():
                    potential_elements.discard(subchild)
            error_if(len(potential_elements),
                  "Forward reference not allowed in initializer.")

        if static_declaration(field):
            for name in field.findall(".//name"):
                if hasattr(child, "declaration") and isvariable(child.declaration):
                    field.env.get_declaration_site_for_variable_name(name_to_str(name),name)

if __name__ == '__main__':
    import warnings
    warnings.filterwarnings('ignore', category=DeprecationWarning)

    files = sys.argv[1:]
    sys.exit(typecheck_files(files))
