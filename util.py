#!/usr/bin/env python2.6
"""
But from the West has come no word,
And on the Hither Shore
No tidings Elven-folk have heard
Of Amroth evermore.
"""

import os
import xml
import xml.dom.minidom
import elementtree.ElementTree

class JoosSyntaxException(BaseException):

    def __init__(self, message):
        self.msg = message


class CurrentFile(object):
    name = None
    mangled_name = None
    static_slot = 0


class Testing(object):
    testing = False


def error_if(condition, msg):
    if condition:
        #if not Testing.testing:
            #print "FILE: " + str(CurrentFile.name)
        raise JoosSyntaxException(msg)


def onein(options, lst):
    """Returns True if at least one of the items in 'options' is in lst"""
    for option in options:
        if option in lst:
            return True
    return False


def allin(options, lst):
    for option in options:
        if option not in lst:
            return False
    return True


def all_files_in_dir(rootdir):
    fileList = []
    for root, subFolders, files in os.walk(rootdir):
        for f in files:
            if (os.path.join(root, f).find(".java") != -1
            and os.path.join(root, f).find(".xml") == -1
            and os.path.join(root, f).find("#") == -1):
                fileList.append(os.path.join(root, f))
    return fileList


def add_dict(from_, to):
    for key in from_:
        to[key] = from_[key]


def add_asm_to_tree(tree):
    for child in tree:
        add_asm_to_tree(child)
    if hasattr(tree, "slot"):
        tree.set("slot", str(tree.slot))
    if hasattr(tree, "memory_location"):
        tree.set("memory_location", str(tree.memory_location))
    if hasattr(tree, "assembly"):
        tree.set("assembly", tree.assembly)
    if hasattr(tree, "field_offset"):
        tree.set("field_offset", str(tree.field_offset))
    if hasattr(tree, "superclass"):
        tree.set("superclass", str(tree.superclass.get("canonical_name")))

def to_file(tree, out="output.xml"):
    add_asm_to_tree(tree)
    if isinstance(tree, elementtree.ElementTree.ElementTree):
        tree = tree.find("/")
    string = elementtree.ElementTree.tostring(tree)
    code = xml.dom.minidom.parseString(string)
    pretty = code.toprettyxml()
    f = open(out, 'w')
    for line in pretty.split("\n"):
        if not line.isspace():
            f.write(line + "\n")


def test_typecheck(filename="Object.java"):
    import typechecker
    import environment
    environment.cached_environments = {}
    environment.cached_trees = {}
    # stdlib = all_files_in_dir("test_cases/stdlib/6.0")
    trees = typechecker.check_files([filename])
    to_file(trees[-1])


def is_primitive(type_name):
    return is_integral_primitive(type_name) or type_name == "boolean"


def is_integral_primitive(type_name):
    return type_name in ["char", "byte", "int", "short"]


def isarray(type_name):
    return type_name[-2:] == "[]"


def printall(locals, dump=False):
    for k, v in locals.items():
        if k == "self":
            continue
        if str(v).startswith("<Element") and dump:
            string = elementtree.ElementTree.tostring(v)
            code = xml.dom.minidom.parseString(string)
            v = code.toprettyxml()
            v = "\n".join([x for x in v.split("\n") if
                           x != "" and not x.isspace()])
        print str(k) + ": '" + str(v) + "'"


def isvariable(el):
    return el.tag in ["local_variable_declaration", "field", "param"]


def classof(elem):
    return elem.env.findclass("this").get("canonical_name")


def same_staticisity(el1, el2):
    error_if(is_static_context(el1) != is_static_context(el2),
          "Staticisity error")


def is_method(el):
    return el.tag in ["method"]


def is_class(el):
    return el.tag in ["class"]


def statisicity_mismatch(s1, s2):
    if s1:
        if not s2:
            return True
    return False

_is_static_context = {}


def is_static_context(el):
    if el in _is_static_context:
        return _is_static_context[el]
    if "static" in modifiers(el):
        _is_static_context[el] = True
        return True
    if el.env.tree != el:
        _is_static_context[el] = is_static_context(el.env.tree)
    if el.env.parent:
        _is_static_context[el] = is_static_context(el.env.parent.tree)
    else:
        _is_static_context[el] = False
    return _is_static_context[el]


def modifiers(element):
    """Returns a list of string modifiers given something with modifiers. """
    if element is None:
        return []
    if element.tag != "modifiers":
        element = element.find("modifiers")
    if element is None:
        return []
    return [x.tag[4:] for x in element.getchildren()]


def is_protected(element):
    return "protected" in modifiers(element)


def return_type(element):
    """Gets the return type of a method element."""
    return collect_token_text(element.find("type"))


def all_with_modifier(tree, tag, modifier):
    return tree.findall(".//" + tag + "/modifiers/tok_" + modifier)


def is_abstract(element):
    """Takes a method_declaration or abstract_method_declaration element and
    returns true if it corresponds to an abstract or interface method."""
    if element.tag == "abstract_method":
        return True
    if element.tag == "method":
        return "abstract" in modifiers(element)
    return False


def name_to_str(name):
    """ Given a 'name' subtree, returns the string representation."""
    if name is None:
        return ""
    name_ = []
    for tok in name.findall(".//tok_identifier"):
        name_ += [tok.text]
    return ".".join([x.strip() for x in name_])


def collect_token_text(tree, sep=""):
    """Concatenates all tokens in 'tree' and returns the text."""
    if tree is not None:
        if tree.tag[:3] == "tok":
            return tree.text
        ret = []
        for child in tree:
            ret.append(collect_token_text(child))
        return sep.join(ret)

def collect_debug_text(tree):
    """Concatenates all tokens and values in 'tree' and returns the text."""
    sep = " "
    ret = []
    if tree is None:
        return ""
    if isinstance(tree, list):
        for node in tree:
            ret.append(collect_debug_text(node))
    else:
        if tree.tag[:3] == "tok":
            return tree.text
        elif tree.get("value"):
            return str(tree.get("value"))
        for child in tree:
            ret.append(collect_debug_text(child))
    return sep.join(ret)


def isconst(expr):
    return expr.find(".//tok_identifier") is None


def type_string(element):
    type_element = element.find("type")
    type_string_return = collect_token_text(type_element)
    if not type_string_return:
        return "void"
    return type_string_return


def is_simple_name(name_element):
    """Takes a name element and returns True if it contains only one
        identifier."""
    return len(name_element.findall(".//tok_identifier")) == 1


def package(element):
    """Returns the package an element is in"""
    return element.env.find_package_name()


def find_type_decl(tree):
    clazz = tree.find(".//class")
    if not clazz:
        clazz = tree.find(".//interface")
    return clazz


def argument_list(element):
    argument_list_element = element.find("argument_list")
    if argument_list_element is not None:
        return tuple([x.attrib["type"] for x in argument_list_element])
    return tuple()


def argument_list_for_declaration(env, method):
    args = []
    for arg in method.findall(".//param/type"):
        arg_text = collect_token_text(arg)
        if is_primitive(arg_text) or arg_text.find("[") != -1:
            args += [arg_text]
        else:
            args += [env.findclass(arg_text).get("canonical_name")]

    return tuple(args)

def enclosing_method(tree):
    return tree.env.find_method_by_name("$", ())

