#!/usr/bin/env python2.6
#TODO: Figure out why all the simplify_names are necessary
#TODO: Remove extra elements from simplify_stars
#TODO: Is find_toplevel necessary?

import elementtree as et
import weed
import util


def simplify_tree(tree):
    """Performs simplifications on an parse tree.

    Takes a partially simplified parse tree. Destructively simplifies it
    further in the sections which this module is responsible for."""

    #tree = et.ElementTree.XML(xml_tree)
    remove_from_tree(tree, "tok_comma")
    simplify_names(tree)
    simplify_stars(tree, "argument_list", False)
    simplify_expression(tree, "expression")

    #return

    simplify_stars(tree, "modifiers", True)
    simplify_stars(tree, "class_body_declaration")
    simplify_stars(tree, "block_statement")

    simplify_expression(tree, "assignment_expression")

    # 19.8.4 - 19.11
    remove_from_tree(tree, "interface_member_declaration_star")
    remove_from_tree(tree, "block_statement_star")
    remove_from_tree(tree, "block_statement")
    remove_from_tree(tree, "interface_member_declaration")
    remove_from_tree(tree, "class_or_interface_type")
    simplify_stars(tree, "extends_interfaces")
    remove_from_tree(tree, "local_variable_declaration_statement")
    remove_from_tree(tree, "statement_without_trailing_substatement")
    remove_from_tree(tree, "statement_expression")
    remove_from_tree(tree, "statement_no_short_if")
    remove_from_tree(tree, "expression_statement")
    remove_from_tree(tree, "assignment_operator")
    remove_from_tree(tree, "statement")

    simplify_stars(tree, "params", False)

    #  Types
    remove_from_tree(tree, "literal")
    remove_from_tree(tree, "numeric_type")
    remove_from_tree(tree, "integral_type")
    remove_from_tree(tree, "class_type")
    remove_from_tree(tree, "interface_type")
    remove_from_tree(tree, "array_type")
    remove_from_tree(tree, "type_declaration")
    remove_from_tree(tree, "type_declaration_star")

    #  Packages and Imports
    remove_from_tree(tree, "tok_package")
    remove_from_tree(tree, "tok_semicolon")
    simplify_imports(tree)
    remove_from_tree(tree, "tok_class")
    remove_from_tree(tree, "tok_extends")
    simplify_interfaces(tree)

    #  Classes and Interfaces
    remove_from_tree(tree, "tok_l_brace")
    remove_from_tree(tree, "tok_r_brace")
    remove_from_tree(tree, "class_member_declaration")
    remove_from_tree(tree, "class_body_declaration")
    remove_from_tree(tree, "class_body_declaration_star")
    name_element(tree, "class_declaration", True)
    name_element(tree, "interface_declaration", True)

    #  Fields
    remove_from_tree(tree, "variable_initializer")
    remove_from_tree(tree, "variable_declarator")
    remove_from_tree(tree, "variable_declarators")

    #  Methods
    remove_from_tree(tree, "method_declarator")
    remove_from_tree(tree, "method_header")
    remove_from_tree(tree, "method_body")
    name_element(tree, "method")
    name_element(tree, "abstract_method")
    remove_from_tree(tree, "method_declarator")
    remove_from_tree(tree, "constructor_declarator")
    name_element(tree, "constructor_declaration")

    simplify_if_then_else(tree)

    simplify_decimal_literals(tree)
    simplify_bool_literals(tree)
    weed.check_literals(tree)  # hack around some Java evilness

    simplify_parenthesized_expressions(tree)
    coalesce_expressions(tree)

    # Prettier Tag Names
    rename_tags(tree)
    simplify_void_return_types(tree)
    simplify_string_and_character_literals(tree)
    simplify_null_literals(tree)

    weed.check_casts(tree)
    simplify_cast_expressions(tree)
    return tree


def simplify_cast_expressions(tree):
    """
    If a <cast> block contains an <expresion> block, removes the <expression>
    and replaces it with its children.
    """
    for elem in tree.findall(".//cast_expression/expression"):
        parent = get_parent(tree, elem)
        pivot_children(tree, parent, elem)


def rename_tags(tree):
    """Gives AST elements some more human-friendly names.

    Arguments:
        tree: The AST to modify."""
    rename_tag(tree, "class_declaration", "class")
    rename_tag(tree, "interface_declaration", "interface")
    rename_tag(tree, "package_declaration", "package")
    rename_tag(tree, "p_super", "extends")
    rename_tag(tree, "interfaces", "implements")
    rename_tag(tree, "if_then_else_statement", "if_then_statement")
    rename_tag(tree, "if_then_else_statement_no_short_if", "if_then_statement")
    rename_tag(tree, "while_statement_no_short_if", "while_statement")
    rename_tag(tree, "for_statement_no_short_if", "for_statement")


def simplify_void_return_types(tree):
    """Given the current AST, converts methods returning 'void' to have
    it enclosed in <type> tags."""
    pass
    for element in (tree.findall(".//method") +
                   tree.findall(".//abstract_method")):
        void = element.find("tok_void")
        if void is not None:
            element.remove(void)
            tok_void_tag = et.ElementTree.Element("tok_void")
            type_tag = et.ElementTree.Element("type")
            tok_void_tag.text = "void"
            type_tag.append(tok_void_tag)
            element.append(type_tag)


def simplify_names(tree):
    """Flattens <name> blocks into simple identifier lists.

    Arguments:
        tree: The parse tree to modify"""
    for name in find_toplevel(tree, "name"):
        identifiers = name.findall(".//tok_identifier")
        name.clear()
        for ident in identifiers:
            name.append(ident)
            if ident != identifiers[-1]:
                dot = et.ElementTree.Element("tok_dot")
                dot.text = "."
                name.append(dot)


def name_element(tree, tag, canonicalize=False):
    """Gives elements a name= attribute as their name.

    Searches for tags with the specified tag name. Takes the first identifier
    under the tag and uses the text of that element as the name= atribute of
    the tag.

    Arguments:
        tree: The parse tree to modify
        tag: The name of the tag to name specified as a string"""
    for tag in tree.findall(".//" + tag):
        found = tag.find("tok_identifier")
        if found is None:
            found = tag.find("./simple_name")
            name = util.name_to_str(found)
        else:
            name = found.text
        tag.set("name", name)
        tag.remove(found)
        if canonicalize:
            if tree.find("package_declaration") is None:
                tag.set("canonical_name", tag.get("name"))
            else:
                tag.set("canonical_name",
                        util.name_to_str(tree.find("package_declaration")) +
                        "." + tag.get("name"))


def simplify_interfaces(tree):
    """Flattens <interfaces> blocks into name lists.

    All contents inside <interfaces> tags will be reduced to a
    series of <name> tags.

    Arguments:
        tree: The parse tree to modify"""
    for interface in find_toplevel(tree, "interfaces"):
        identifiers = interface.findall(".//name")
        interface.clear()
        for ident in identifiers:
            interface.append(ident)


def simplify_imports(tree):
    """Flattens import productions into <import> and <star_import>.

    All content instead a top-level <imports> tag will be
    transformed into a list of <import> or <star_import> tags, respectively
    meaning single type imports and on-demand imports.

    Arguments:
        tree: The parse tree to modify."""
    for imp in find_toplevel(tree, "imports"):
        simple_imports = imp.findall(".//single_type_import_declaration")
        star_imports = imp.findall(".//star_import")
        imp.clear()
        for simp in simple_imports:
            imp.append(simp)
        for string in star_imports:
            imp.append(string)
    rename_tag(tree, "imports", "imports")
    rename_tag(tree, "single_type_import_declaration", "import")
    rename_tag(tree, "star_import", "star_import")
    remove_from_tree(tree, "tok_import")
    stars = tree.findall(".//star_import")
    for star in stars:
        star.remove(star.find("tok_dot"))
        star.remove(star.find("tok_star"))


def rename_tag(tree, oldname, newname):
    """Renames a tag.

    Arguments:
        tree: An ElementTree to act on
        oldname: The old tag name
        newname: The name to change oldname to."""
    for tag in tree.findall(".//" + oldname):
        if tag.tag == oldname:
            tag.tag = newname


def remove_from_tree(tree, name):
    """Removes instances of an XML tag.

    Destructively modifies the specified tree to remove all occurences of the
    specified tag and replace them with their children.

    Arguments:
        tree: An ElementTree to remove tag instances from
        name: The name of the tag to remove from the tree"""
    for element in tree.findall(".//" + name):
        parent = get_parent(tree, element)
        pivot_children(tree, parent, element)


def find_toplevel(tree, name):
    """Finds all of the top-level elements with the given name

    In the example <name>foo<name>bar</name></name>, there is only one
    top-level name element, the one containing 'foo'.

    Arguments:
        tree: An ElementTree to search
        name: The name of the tag to search for
    Returns:
        A list of Element objects, the top-level elements by this name."""
    elements = tree.findall(".//" + name)
    result = []
    for element in elements:
        toplevel = True
        parent = get_parent(tree, element)
        while parent is not None:
            if parent.tag == name:
                toplevel = False
            parent = get_parent(tree, parent)
        if toplevel:
            result.append(element)
    return result


_parents = {}


def get_parent(tree, element):
    """Returns the parent of the specified element in the tree.

    Arguments:
        element: An Element instance to get the parent of
        tree: An ElementTree instance
    Returns:
        An element representing the parent element."""
    if tree not in _parents:
        # Implementation of parent-finding as per the suggestion in the
        # ElementTree documentation.
        _parents[tree] = dict((c, p) for p in tree.getiterator() for c in p)
    if element in _parents[tree]:
        return _parents[tree][element]
    else:
        return None


def pivot_children(tree, parent, child):
    """Given a parent element and a child, take all of the children of the
    child and insert them at the same index (in order) in the parent that the
    child originally resided at."""
    insert_index = 0
    children = list(parent)
    for i in xrange(len(children)):
        if children[i] is child:
            insert_index = i
            break

    parent.remove(child)
    del _parents[tree][child]
    for subchild in reversed(list(child)):
        parent.insert(insert_index, subchild)
        _parents[tree][subchild] = parent


def remove_literal_wrappers(expression):
    for x in range(0, len(expression.getchildren())):
        child = expression.getchildren()[x]
        if (len(child.getchildren()) == 1 and
            (child.getchildren()[0].tag == "integer_literal" or
             child.getchildren()[0].tag == "boolean_literal")
            and not child.tag in ["argument_list"]):

            subchild = child.getchildren()[0]
            expression.remove(child)
            expression.insert(x, subchild)
        remove_literal_wrappers(child)


def simplify_child(expression):
    if expression.tag.startswith("tok_"):
        return expression
    parent = expression
    children = expression.getchildren()
    while (len(children) == 1 and children[0].getchildren() and
           children[0].tag != 'expression'):
        parent = children[0]
        children = children[0].getchildren()
    for child in children:
        simplify_child(child)
    if expression != parent:
        expression.clear()
        expression.append(parent)


def simplify_expression(tree, name):
    expressions = tree.findall(".//" + name)
    for expression in expressions:
        simplify_child(expression)
        remove_literal_wrappers(expression)


def simplify_string_and_character_literals(tree):
    for el in (tree.findall(".//tok_character_literal") +
              tree.findall(".//tok_string_literal")):
        val = el.text
        if val is None:
            continue
        el.clear()
        el.set("value", val[1:-1])  # Strip delimiters
        if el.tag == "tok_character_literal":
            el.set("type", "char")
            escaped_value = el.get("value").decode("string_escape")
            el.set("value", str(ord(escaped_value[0])))
        else:
            el.set("type", "java.lang.String")
        el.tag = el.tag[4:]  # Strip tok_ from names


def simplify_decimal_literals(tree):
    for el in tree.findall(".//integer_literal"):
        if el.find("tok_decimal_integer_literal") is not None:
            val = str(int(el.find("tok_decimal_integer_literal").text))
            el.clear()
            el.set("value", val)
            el.set("type", "int")
        elif el.find("tok_octal_integer_literal") is not None:
            val = str(int(el.find("tok_octal_integer_literal").text, 16))
            el.clear()
            el.set("value", val)
            el.set("type", "int")
        else:
            # TODO: Figure out why this breaks everything
            pass


def simplify_bool_literals(tree):
    for el in tree.findall(".//boolean_literal"):
        if el.find(".//tok_true") is not None:
            el.clear()
            el.set("value", "True")
            el.set("type", "boolean")
        else:
            el.clear()
            el.set("value", "False")
        el.set("type", "boolean")


def simplify_null_literals(tree):
    for el in tree.findall(".//null_literal"):
        el.clear()
        el.set("value", "0")

expr_map = {"tok_plus": (lambda x, y: x + y, "integer_literal", "int"),
            "tok_div":  (lambda x, y: x / y, "integer_literal", "int"),
            "tok_mod":  (lambda x, y: x % y, "integer_literal", "int"),
            "tod_sub":  (lambda x, y: x - y, "integer_literal", "int"),
            "tok_star": (lambda x, y: x * y, "integer_literal", "int"),
            "tok_or":   (lambda x, y: x or y, "boolean_literal", "boolean"),
            "tok_and":  (lambda x, y: x and y, "boolean_literal", "boolean"),
            "tok_eq":   (lambda x, y: x == y, "boolean_literal", "boolean"),
            "tok_neq":  (lambda x, y: x != y, "boolean_literal", "boolean")
            }

INT_MAX = 2147483647
def within_valid_numeric_range(number):
    if number > INT_MAX:
        return False
    if number < (-INT_MAX - 1):
        return False
    return True

def coalesce_expressions(tree):
    #multiplicative_expression, additive_expression
    simplified = True
    while simplified:
        simplified = False
        for expr in (tree.findall(".//multiplicative_expression") +
                     tree.findall(".//additive_expression") +
                     tree.findall(".//equality_expression") +
                     tree.findall(".//conditional_or_expression") +
                     tree.findall(".//conditional_and_expression")):

            if (len(expr.getchildren()) == 3 and
                expr.getchildren()[0].get("value") and
                expr.getchildren()[2].get("value")):

                left = eval(expr.getchildren()[0].get("value"))
                right = eval(expr.getchildren()[2].get("value"))
                tag = expr.getchildren()[1].tag
                if tag in expr_map:
                    if(tag == "tok_div" and right == 0):
                        continue
                    reduced_value = expr_map[tag][0](left, right)
                    if within_valid_numeric_range(reduced_value):
                        expr.clear()
                        expr.set("value", str(expr_map[tag][0](left, right)))
                        expr.tag = expr_map[tag][1]
                        expr.set("type", str(expr_map[tag][2]))
                        simplified = True

        # Other simplifications to consider:
        # unary_expression
        # relational_expression, equality_expression
        # and_expression, exclusive_or_expression
        # inclusive_or_expression
        # conditional_and_expression
        # conditional_or_expression

        for expr in (tree.findall(".//expression") +
                     tree.findall(".//relational_expression")):
            if (len(expr.getchildren()) == 1 and
                expr.getchildren()[0].get("value") is not None):

                value = expr.getchildren()[0].get("value")
                type_string = expr.getchildren()[0].get("type")
                expr.clear()
                expr.set("value", value)
                expr.set("type", type_string)
                simplified = True


def simplify_repetition(tree, name):
    simplify_stars(tree, name)


def collect_list_el(subtree):
    els = subtree.getchildren()
    if len(els) == 0:
        return []
    if len(els) == 1:
        return els
    else:
        return collect_list_el(subtree.getchildren()[0]) + [
            subtree.getchildren()[1]]


def simplify_stars(tree, name, tokentext=False):
    subtrees = tree.findall(".//" + name)
    for subtree in subtrees:
        els = collect_list_el(subtree)
        subtree.clear()
        for el in els:
            if tokentext:
                subtree.append(el.getchildren()[0])
            else:
                subtree.append(el)
    return tree


def simplify_if_then_else(tree):
    for stmt in tree.findall(".//if_then_statement"):
        then = et.ElementTree.Element('then')
        else_ = et.ElementTree.Element('else')
        then.append(stmt.getchildren()[-1])
        stmt.remove(stmt.getchildren()[-1])
        stmt.append(then)
        stmt.append(else_)
    for stmt in (tree.findall(".//if_then_else_statement") +
                 tree.findall(".//if_then_else_statement_no_short_if")):
        then = et.ElementTree.Element('then')
        else_ = et.ElementTree.Element('else')

        then.append(stmt.getchildren()[-3])
        else_.append(stmt.getchildren()[-1])
        stmt.remove(stmt.getchildren()[-3])
        stmt.remove(stmt.getchildren()[-1])
        stmt.append(then)
        stmt.append(else_)


def simplify_parenthesized_expressions(tree):
    for expr in tree.findall(".//primary_no_new_array"):
        if (len(expr.getchildren()) == 3 and
            expr.getchildren()[0].tag == "tok_l_parenthese"):
            child = expr.getchildren()[1]
            expr.clear()
            expr.tag = child.tag
            if child.get("value"):
                expr.set("value", child.get("value"))
                expr.set("type", child.get("type"))
            for c in child.getchildren():
                expr.append(c)
