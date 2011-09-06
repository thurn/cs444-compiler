#!/usr/bin/env python2.6
#TODO: Convert Environment to a bnch of subclasses
#TODO: Have Environment constructor recurse directly
#TODO: remove the need for add_superclass_methods/fields by constructing
#      environments on-demand
#TODO: fields from superclasses aren't necessarily handled properly?
#TODO: Rename findlocal vs find_nonlocal
#TODO: name variables <variable> <tok_identifier>
#TODO: Move methods from env to somewhere else

from util import error_if, JoosSyntaxException, add_dict, is_primitive, \
    is_integral_primitive, CurrentFile, isarray, find_type_decl, \
    argument_list_for_declaration, Testing, modifiers, name_to_str, \
    is_abstract, all_with_modifier, return_type, type_string, isvariable, \
    is_method, is_static_context, statisicity_mismatch, is_class, printall
from parse import parse
from lexer import lex
from elementtree import ElementTree
import sys


class Environment(object):
    """Environment object used for looking up variables, methods, classes, etc.

    Is paired with a part of the AST - generally a compilation_unit, class,
    method, etc."""

    def __init__(self, tree, parent, trees, name_to_class):
        self.initialize(parent, tree)

        if tree.tag == "compilation_unit":
            self.initialize_compilation_unit_environment(name_to_class, tree,
                                                         trees)
        elif tree.tag == "class" or tree.tag == "interface":
            self.initialize_class_or_interface_environment(tree)

        elif tree.tag == "method" or tree.tag == "abstract_method":
            self.initalize_method_environment(tree)

        elif tree.tag == "constructor_declaration":
            self.initialize_constructor_environment(tree)

    def initialize_constructor_environment(self, tree):
        for decl in tree.findall(".//param"):
            name = decl.find(".//variable//tok_identifier").text
            error_if(name in self.formal_parameters,
                  "Method has two args with same name.")
            self.formal_parameters[name] = decl
        self.methods["$", ()] = tree
        tree.slot = 0

    def initalize_method_environment(self, tree):
        for decl in tree.findall(".//param"):
            name = decl.find(".//variable//tok_identifier").text
            error_if(name in self.formal_parameters,
                  "Method has two args with same name.")
            self.formal_parameters[name] = decl
        self.methods["$", ()] = tree
        tree.slot = 0

    def add_field_declarations_to_environment(self, tree):
        for field in tree.findall(".//field"):
            name = field.find(".//variable//tok_identifier")
            error_if(name.text in self.fields,
                  "Two fields cannot share the same name.")
            self.fields[name.text.strip()] = field

    def add_constructor_declarations_to_environments(self, tree):
        for ctor in tree.findall(".//constructor_declaration"):
            name = ctor.get("name")
            error_if(name != tree.get("name"), "Wrong constructor name.")
            args = argument_list_for_declaration(self, ctor)
            error_if(args in self.constructors,
                  "Duplicate constructors not allowed.")
            self.constructors[args] = ctor

    def add_method_declarations_to_environment(self, tree):
        for method in tree.findall(".//method") + tree.findall(
                ".//abstract_method"):
            name = method.get("name")
            args = argument_list_for_declaration(self, method)
            error_if((name, args) in self.methods,
                  "Duplicate methods not allowed.")
            self.methods[name, args] = method
        self.tree.superclass = self.__superclass(self.tree)

    def initialize_class_or_interface_environment(self, tree):
        self.fields["this"] = self.tree

        self.add_field_declarations_to_environment(tree)
        self.add_constructor_declarations_to_environments(tree)
        self.add_method_declarations_to_environment(tree)

        implemented_interface_names = [self.findclass(name_to_str(x)) for x in
              tree.findall(".//implements/name")]
        extended_interface_names = [self.findclass(name_to_str(x)) for x in
              tree.findall(".//extends_interfaces/name")]

        self.tree.interfaces = implemented_interface_names + \
                               extended_interface_names

    def add_single_type_import_statements(self, pkg, this_clazz, tree, trees):
        import_names = [name_to_str(x) for x in tree.findall(".//import/name")]
        for fullname in import_names:
            name = fullname[fullname.rfind(".") + 1:]
            error_if(name in self.classes_this and
                  not fullname == pkg + "." + this_clazz.get("name"),
                  "Single-type imports clash with class defined in file.")
            error_if(name in self.classes_single and
                  not self.__findclass(fullname, trees) ==
                      self.classes_single[name],
                  "Two single-type import decls clash with each other.")
            self.classes_single[name] = self.__findclass(fullname, trees)

    def add_import_star_statements(self, imported, tree, trees):
        star_import_names = [name_to_str(x) for x in
                             tree.findall(".//star_import/name")]

        star_import_names += ["java.lang"]
        for fullname in star_import_names:
            if fullname not in imported:
                imported += [fullname]
                tmp = find_all_in_package(fullname, trees)
                used = [name_to_str(x) for x in
                        tree.findall(".//name")] + ["Object"]
                for key in tmp:
                    if key not in self.classes_single:  # and key in used:
                        error_if(key in self.classes_star and key in used,
                              "Ambiguous class %s" % key)
                        self.classes_star[key] = tmp[key]

    def initialize_compilation_unit_environment(self, name_to_class, tree,
                                                trees):
        pkg = ""

        if tree.find(".//package//name"):
            pkg = name_to_str(tree.find(".//package//name"))

        self.package_name = pkg
        this_clazz = find_type_decl(tree)
        self.classes_this[this_clazz.get("name")] = this_clazz
        self.classes_this["this"] = this_clazz
        self.classes_package = find_all_in_package(pkg, trees)

        self.add_single_type_import_statements(pkg, this_clazz, tree, trees)

        imported = []
        self.add_import_star_statements(imported, tree, trees)
        add_dict(find_all_in_package(pkg, trees), self.classes_package)
        add_dict(name_to_class, self.classes_fully_qualified)

    def initialize(self, parent, tree):
        self.package_name = None
        self.classes_this = {}
        self.classes_single = {}
        self.classes_star = {}
        self.classes_package = {}
        self.classes_fully_qualified = {}
        self.fields = {}
        self.methods = {}
        self.constructors = {}
        self.local_variables = {}
        self.formal_parameters = {}
        self.parent = parent
        self.tree = tree
        self.tree.env = self

    def find_package_name(self):
        if self.package_name is not None:
            return self.package_name
        else:
            return self.parent.find_package_name()

    def find_constructor(self, args):
        if args in self.constructors:
            return self.constructors[args]
        elif self.parent:
            return self.parent.find_constructor(args)
        else:
            return None

    def get_current_class_name(self):
        return self.findclass("this").get("canonical_name")

    def check_path_for_protected(self, path):

        if len(path) == 1:
            # Impossible to violate protected with a 1 length path
            return

        for x in range(0, len(path) - 1):
            previous_path_element = path[x]
            current_path_element = path[x + 1]

            if not "protected" in modifiers(current_path_element):
                continue
            if self.find_package_name() == \
                    current_path_element.env.find_package_name():
                continue

            current_class_name = self.get_current_class_name()
            current_path_element_class_name = \
                current_path_element.env.get_current_class_name()

            if previous_path_element.tag == "class":
                error_if(not self.is_subtype(current_class_name,
                                          current_path_element_class_name),
                      "must be a subtype to access a proteced static member")

            else:
                previous_path_element_type = \
                    self.canonicalize_name(type_string(previous_path_element))
                error_if(not self.is_subtype(previous_path_element_type,
                                          current_class_name),
                      "must invoke on a subtype to access a protected member")
                error_if(not self.is_subtype(current_class_name,
                                          current_path_element_class_name),
                      "Cannot invoke protected member in subtype")

    def check_path_for_static(self, path):
        static_context = is_static_context(self.tree)
        for path_index in xrange(len(path)):
            path_element = path[path_index]
            if isvariable(path_element) or is_method(path_element):
                if not path_index:
                    if path_element.tag in ["field", "method"]:
                        error_if(is_static_context(path_element),
                              "Non-static access to static member.")
                        error_if(statisicity_mismatch(static_context,
                                                      is_static_context(path_element)),
                              "Direct statisicity mismatch.")
                elif path_index > 0:
                    previous_element = path[path_index - 1]
                    if is_class(previous_element):
                        error_if(not is_static_context(path_element),
                              "Cannot access non-static from static context.")
                    elif isvariable(previous_element):
                        error_if(is_static_context(path_element),
                              "Cannot access static from non-static context.")

    def get_declaration_path_for_name(self, name, args = None):
        try:
            return self.__get_declaration_site_for_name(name, "Variable", path=True)
        except JoosSyntaxException :
            try:
                if args is not None:
                    return self.__get_declaration_site_for_name(name, "Method", arglist=args, path=True)
                else:
                    return []
            except JoosSyntaxException :
                return []

    def get_declaration_site_for_class_name(self, name):
        if isarray(name):
            return self.findclass("java.lang.$Array")
        error_if(self.findclass(name) is None,
                 "No class %s found" % name)
        return self.findclass(name)

    def get_declaration_site_for_constructor_name(self, name, args):
        class_declaration = self.get_declaration_site_for_class_name(name)
        constructor_declaration = class_declaration.env.find_constructor(args)
        error_if(constructor_declaration is None,
                 "No constructor for class %s with args %s found." %
                 (name, str(args)))
        return constructor_declaration

    def get_declaration_site_for_variable_name(self, name, annotate):
        annotate.declaration = self.__get_declaration_site_for_name(name, "Variable")
        return annotate.declaration

    def get_declaration_site_for_method_name(self, name, args):
        return self.__get_declaration_site_for_name(name, "Method", args)

    def __get_declaration_site_for_name(self, name, type="All", arglist=(), path = False):
        def get_declaration_site_for_name_internal(env,
                                                   name,
                                                   type,
                                                   arglist,
                                                   canBeClass=True):
            qualified_parts = name.split(".")

            if len(qualified_parts) == 1:

                path = []
                if type == "Variable":
                    path += [env.find_nonlocal(name)]
                if type == "Method":
                    path += [env.find_method_by_name(name, arglist)]

                path = [x for x in path if x][:1]
                error_if(not path,
                      "Could not find %s %s" % (type, name))
            else:
                path = []
                rhs = None  # Initialize
                for x in range(1, len(qualified_parts) + 1):

                    lhs = ".".join(qualified_parts[:x])
                    rhs = ".".join(qualified_parts[x:])

                    if env.find_nonlocal(lhs) is not None:
                        path = [env.find_nonlocal(lhs)]
                        break

                    elif env.find_method_by_name(lhs, arglist) is not None and rhs == "":
                        path = [env.find_method_by_name(lhs, arglist)]
                        break

                    # resolving LHS is a Class
                    elif canBeClass and env.findclass(lhs) is not None:
                        path = [env.findclass(lhs)]
                        break

                error_if(len(path) == 0,
                      "Cannot find declaration for %s %s" % (type, name))
                if isvariable(path[-1]) or (path[-1].tag == "method" and rhs):
                    if isarray(type_string(path[-1])):
                        new_env = env.findclass("java.lang.$Array").env
                    else:
                        if isarray(type_string(path[-1])):
                            new_env = env.findclass("java.lang.$Array").env
                        else:
                            error_if(is_primitive(type_string(path[-1])),
                                  "Method called on primitive.")
                            new_env = path[-1].env.findclass(
                                type_string(path[-1])).env
                else:
                    new_env = path[-1].env
                path += get_declaration_site_for_name_internal(new_env,
                                                               rhs,
                                                               type,
                                                               arglist,
                                                               False)

            return path

        retval = get_declaration_site_for_name_internal(self,
                                                        name,
                                                        type,
                                                        arglist)

        self.check_path_for_static(retval)
        self.check_path_for_protected(retval)
        if path:
            return retval
        return retval[-1]

    def canonicalize_name(self, simple_name):
        if is_primitive(simple_name) or simple_name in ["void", "null"]:
            return simple_name
        elif simple_name[-2:] == "[]":
            return self.canonicalize_name(simple_name[:-2]) + "[]"
        return self.findclass(simple_name).get("canonical_name")

    def get_type_for_declaration_site(self, element):
        decl_type_string = type_string(element)
        if (is_primitive(decl_type_string) or
            isarray(decl_type_string) or
            decl_type_string == "void"):
            return decl_type_string
        return self.findclass(decl_type_string).get("canonical_name")

    def add_superclass_fields(self):
        """Ensures superclass fields are inherited properly."""
        if hasattr(self, "fields_numbered"):
            return
        self.fields_numbered = True
        superclazz = self.tree
        max_field_offset = 0
        while superclazz is not superclazz.superclass:
            superclazz = superclazz.superclass
            if hasattr(superclazz.env, "fields_numbered"):
                pass
            else:
                superclazz.env.add_superclass_fields()
            for field in superclazz.findall(".//field"):
                max_field_offset = max(field.field_offset, max_field_offset)

        for field in self.fields:
            if field == "this":
                continue
            max_field_offset = max_field_offset + 1
            self.fields[field].field_offset = max_field_offset
        self.tree.num_fields = max_field_offset

    def add_method_from_parent_class(self, method):
        name = method.get("name")
        args = argument_list_for_declaration(method.env, method)
        if (name, args) in self.methods:
            # If this method is already defined
            error_if("final" in modifiers(method),
                     "Cannot override final methods.")
            error_if("static" in modifiers(self.methods[name, args]),
                     "Cannot override a method with a static methods.")
            error_if("static" in modifiers(method),
                     "Cannot override a static method.")

            error_if("protected" in modifiers(self.methods[name, args])
                     and "public" in modifiers(method),
                     "A protected method must not override a public method.")

            error_if((return_type(self.methods[name, args]) !=
                      return_type(method)),
                     "An overriding method cannot have a different return " +
                     "type from what it is overriding")
        else:
            error_if(is_abstract(method) and "abstract"
            not in modifiers(self.tree),
                     "Must override abstract method.")
            self.methods[name, args] = method

    def add_method_from_parent_interface(self, method):
        name = method.get("name")
        args = argument_list_for_declaration(method.env, method)
        error_if((name, args) not in self.methods and
                 "abstract" not in modifiers(self.tree) and
                 "class" == self.tree.tag,
                 "Must override interface methods")
        if ((name, args) in self.methods and
            "protected" in modifiers(self.methods[name, args]) and
            "public" in modifiers(method)):
            concrete_method = self.methods[name, args]
            if (concrete_method.find(".//block") is None and
                concrete_method not in self.tree.findall(".//method")):
                self.methods[name, args] = method
            else:
                error_if(True,
                         "A protected method canot override a public method.")
        if (name, args) in self.methods:
            error_if((return_type(self.methods[name, args]) !=
                      return_type(method)),
                     "An overriding method cannot have a different return " +
                     "type from what it is overriding")
        else:
            self.methods[name, args] = method

    def add_superclass_methods(self):
        """Ensures superclass methods are not overriden improperly."""
        if self.tree.superclass == self.tree:
            return  # This is java.lang.Object

        for method in class_methods(self.tree.superclass):
            self.add_method_from_parent_class(method)

        for method in interface_methods(self.tree):
            self.add_method_from_parent_interface(method)

    def findclass(self, name):
        """Returns the class with name 'name'."""
        search_order = [self.classes_this, self.classes_single,
                self.classes_package, self.classes_star,
                self.classes_fully_qualified]
        for search in search_order:
            if name in search:
                return search[name]
        if self.parent:
            return self.parent.findclass(name)
        return None

    def findlocal(self, name):
        """Returns the declaration of the local variable with name 'name'."""
        if name in self.local_variables:
            return self.local_variables[name]
        if name in self.formal_parameters:
            return self.formal_parameters[name]
        if self.parent:
            return self.parent.findlocal(name)
        return None

    def find_nonlocal(self, name):
        """Returns the declaration of the variable with name 'name' checking
           fields as well as local variables."""
        if name in self.local_variables:
            return self.local_variables[name]
        if name in self.formal_parameters:
            return self.formal_parameters[name]
        if name in self.fields:
            return self.fields[name]
        if hasattr(self.tree, "superclass") and self.tree.superclass != self.tree:
            if self.tree.superclass.env.find_nonlocal(name):
                return self.tree.superclass.env.find_nonlocal(name)
        if self.parent:
            return self.parent.find_nonlocal(name)
        return None

    def find_method_by_name(self, name, args):
        if (name, args) in self.methods:
            return self.methods[name, args]

        if self.parent is not None:
            return self.parent.find_method_by_name(name, args)

        return None

    def can_be_cast(self, from_type, to_type):
        return self.are_identity_comparable(from_type, to_type)

    def are_identity_comparable(self, obj1, obj2):
        """Returns whether obj1 and obj2 can occur in an == expression."""
        if obj1 == "null" or obj2 in ["null", "void", "void"]:
            return True
        if is_integral_primitive(obj1) ^ is_integral_primitive(obj2):
            return False
        if is_integral_primitive(obj1) and is_integral_primitive(obj2):
            return True
        if is_primitive(obj1) and obj1 == obj2:
            return True
        if self.is_subtype(obj1, obj2) or self.is_subtype(obj2, obj1):
            return True

        return False

    def is_primitive_assignable(self, lhs, rhs):
        if is_integral_primitive(lhs) and is_integral_primitive(rhs):
            if lhs == "byte" and rhs in ["char", "int", "short"]:
                return False
            if lhs == "short" and (rhs == "int" or rhs == "char"):
                return False
            if lhs == "char" and (rhs == "byte" or rhs == "int"):
                return False
            return True
        if lhs == rhs:
            return True
        return False

    def is_assignable(self, lhs, rhs):
        if lhs == "void":
            return False
        if lhs == rhs:
            return True
        can_assign_arrays_to = ["java.lang.Object", "java.io.Serializable",
                                "java.lang.Cloneable"]
        if lhs in can_assign_arrays_to and isarray(rhs):
            return True
        if isarray(lhs) and isarray(rhs):
            lhs = lhs[:-2]
            rhs = rhs[:-2]
            if lhs == rhs:
                return True
            if is_primitive(lhs) or is_primitive(rhs):
                return False
            return self.is_assignable(lhs, rhs)
        if isarray(rhs):
            return False
        if rhs == "null" and not is_primitive(lhs):
            return True

        if is_primitive(lhs) or is_primitive(rhs):
            return self.is_primitive_assignable(lhs, rhs)
        else:
            if rhs == "null":
                return True
            return self.is_supertype(lhs, rhs)

    def is_subtype(self, obj1, obj2):
        """Returns whether obj1 is a subclass of obj2."""

        assert not is_primitive(obj1)
        assert not is_primitive(obj2)

        if isarray(obj1) and isarray(obj2):
            obj1 = obj1[:-2]
            obj2 = obj2[:-2]
        elif isarray(obj1):
            if obj2 == "java.lang.Object":
                return True
            else:
                return False

        obj1 = self.findclass(obj1)
        obj2 = self.findclass(obj2)
        return self.is_classes_subtype(obj1, obj2)

    def is_classes_subtype(self, obj1, obj2):
        if obj1 is obj2:
            return True
        if obj1 == "null" and not is_primitive(obj2):
            return True
        for clazz in [obj1.superclass] + obj1.interfaces:
            if clazz is obj2:
                return True
            if clazz is not self.findclass("java.lang.Object"):
                if self.is_classes_subtype(clazz, obj2):
                    return True
        return False


    def is_supertype(self, obj1, obj2):
        return self.is_subtype(obj2, obj1)

    def __superclass(self, clazz):
        """For a given 'class' subtree and environment, returns the 'class'
        referring to the class's supertype.  Used to assign the superclass of a
        tree."""
        if clazz.find(".//extends//name") is not None:
            c_name = name_to_str(clazz.find(".//extends//name"))
            if clazz.env.findclass(c_name) is not None:
                error_if(clazz.env.findclass(c_name).tag != "class",
                      "Must not extend an interface class.")
                error_if(clazz == clazz.env.findclass(c_name),
                          "Class cannot extend itself")
                error_if("final" in modifiers(clazz.env.findclass(c_name)),
                      "Cannot extend a final class.")
                return clazz.env.findclass(c_name)
            else:
                error_if(True, "Must extend an existing class.")
        return clazz.env.findclass("java.lang.Object")

    def __findclass(self, fullname, trees):
        """Returns the 'class' object for the class.

        Fullname: fully qualified name of a class
        pkg: package to look in
        trees: set of ASTs to look in

        """
        name = fullname[fullname.rfind(".") + 1:]
        pkg = fullname[:fullname.rfind(".")]
        for tree in trees:
            clazz = find_type_decl(tree)
            if clazz is None:
                continue
            if name == clazz.get("name"):
                package_name = ""
                if tree.find(".//package/name") is not None:
                    package_name = name_to_str(tree.find(".//package/name"))
                if ((package_name == "" and fullname == name) or
                    (package_name == "java.lang" and fullname == name) or
                    pkg == package_name or
                    fullname[:len(fullname) - len(name) - 1] == package_name):
                    return clazz
        error_if(True, "No class to import / Class Not Found.")


find_all_in_package_cache = {}


def find_all_in_package(packagename, trees):
    """Returns all classses in packagename."""
    global find_all_in_package_cache
    if packagename in find_all_in_package_cache:
        return find_all_in_package_cache[packagename]
    retn = {}
    prefix = False
    for tree in trees:
        clazz = find_type_decl(tree)
        if clazz is None:
            continue
        if tree.find(".//package/name") is not None:
            package_name = name_to_str(tree.find(".//package/name"))
            if package_name == packagename:
                retn[clazz.get("name")] = clazz
            elif (packagename == package_name[:len(packagename)]
                  and package_name[len(packagename)] == "."):
                prefix = True
        elif packagename == "":
            retn[clazz.get("name")] = clazz
    error_if(not prefix and len(retn.keys()) == 0,
             "No class in %s" % packagename)
    find_all_in_package_cache[packagename] = retn
    return retn


def class_methods(clazz):
    """Returns all methods declared in a 'clazz' subtree and it's parents."""
    methods = clazz.findall(".//method") + interface_methods(clazz)
    superclazz = clazz.superclass
    if superclazz == clazz:
            return methods
    classes = [clazz, superclazz]
    methods += superclazz.findall(".//method")
    while superclazz != superclazz.superclass:
        superclazz = superclazz.superclass
        error_if(superclazz in classes, "Cycle in class extensions")
        classes += [superclazz]
        methods += superclazz.findall(".//method") + \
                   interface_methods(superclazz)
    return methods


def interface_methods(clazz):
    """Returns all methods declared in interfaces the class implements."""
    methods = []
    if clazz.tag == "class":
        iface_supers = clazz.interfaces
    else:
        iface_supers = [clazz]

    found_ifaces = []
    while iface_supers:
        cur_clazz = iface_supers[0]
        error_if(cur_clazz is None, "Class not defined.")
        iface_supers = iface_supers[1:]
        if cur_clazz not in found_ifaces:
            methods += cur_clazz.findall(".//abstract_method")
            tmp = [cur_clazz.env.findclass(name_to_str(x)) for x in
                             cur_clazz.findall(".//extends_interfaces/name")]
            iface_supers += tmp

        found_ifaces += [cur_clazz]

    return methods


def build_block_environments(block, parent, trees, name_to_class):
    """Builds environments for 'block' and other nodes inside methods."""
    if block.tag in ["compilation_unit", "class", "interface", "method",
                     "abstract_method", "constructor_declaration", "block", "field"]:
        env = Environment(block, parent, trees, name_to_class)
    else:
        env = parent

    for statement in block:

        if statement.tag == "local_variable_declaration":
            name = statement.find("./variable//tok_identifier").text
            Environment(statement, env, trees, name_to_class)
            error_if(env.findlocal(name) is not None,
                  "Two local variables %s cannot have the same scope ." % name)
            statement.env.local_variables[name] = statement
            env = statement.env


        elif (statement.tag == "for_statement" or
              statement.tag == "for_statement_no_short_if"):

            if statement.find("./for_init/local_variable_declaration"):
                name = statement.find(
                        "./for_init//variable//tok_identifier").text
                error_if(env.findlocal(name) is not None,
                      "Two local variables %s have the same scope ." % name)
                for_body = statement.find("./block")
                fe = Environment(statement, env, trees, name_to_class)
                fe.local_variables[name] = statement.find(
                        "./for_init/local_variable_declaration")
                if for_body is not None:
                    build_block_environments(for_body,
                                             fe,
                                             trees,
                                             name_to_class)

        else:
            build_block_environments(statement, env, trees, name_to_class)


def build_environments(tree, trees, name_to_class):
    """Builds environment for AST tree."""
    build_block_environments(tree, None, trees, name_to_class)


def check_types(tree):
    """Checks for type and other errors in tree."""
    toks = tree.findall(".//package//tok_identifier")
    name = ""

    for ident in range(0, len(toks)):
        name += toks[ident].text
        error_if(name in tree.env.classes_fully_qualified and
              name.find(".") != -1,
                  "Package prefix conflicts with class name.")
        if ident < len(toks) - 1:
            name += "."

    clazz = find_type_decl(tree)
    if clazz is None:
        return

    for _ in all_with_modifier(clazz, "method", "abstract"):
        error_if("abstract" not in modifiers(clazz),
              "Abstract methods must be in abstract classes.")

    for it in clazz.findall(".//implements/name") + clazz.findall(
            ".//extends/name") + clazz.findall(
            ".//extends_interfaces/name"):
        name = name_to_str(it)
        error_if(clazz.env.findclass(name) is None,
              "No class %s defined." % name)

    for type_use in clazz.findall(".//type") + clazz.findall(
            ".//class_instance_creation_expression/name"):
        name = ""
        toks = type_use.findall(".//tok_identifier")

        for ident in range(0, len(toks)):
            name += toks[ident].text
            if ident < len(toks) - 1:
                error_if(tree.env.findclass(name),
                      "Prefixes of fully qualified type resolves to type.")
            name += "."

        if type_use.find(".//name") is not None:
            clazz_name = name_to_str(type_use.find(".//name"))
            error_if(not clazz.env.findclass(clazz_name),
                  "Type " + clazz_name + " doesn't exist.")

    for i_type in clazz.findall(".//implements/name"):
        i_name = name_to_str(i_type)
        error_if(clazz.env.findclass(i_name) is not None and
              clazz.env.findclass(i_name).tag != "interface",
              "Must implement an interface class.")

    for c_type in clazz.findall(".//extends_interfaces/name"):
        c_name = name_to_str(c_type)
        error_if(clazz.env.findclass(c_name).tag != "interface",
              "Must extend an interface class.")
        error_if(clazz == clazz.env.findclass(c_name),
              "Class cannot extend itself")

    for inf in tree.findall(".//implements/name"):
        name = name_to_str(inf)
        error_if(clazz.env.findclass(name).tag != "interface",
              "%s is not an interface." % name)

    for clz in tree.findall(".//class_type/name") + tree.findall(
            ".//implements/name"):
        name = name_to_str(clz)
        error_if((tree.env.findclass(name) is None) or
              (tree.env.findclass(
                      name).tag == "class"),
              "%s is not an interface." % name)


def check_hierarchy(tree):
    clazz = tree.find(".//class")

    if not clazz:
        clazz = tree.find(".//interface")

    ifaces = [clazz.env.findclass(name_to_str(x)) for x in
              clazz.findall(".//implements/name")]

    for i in range(0, len(ifaces)):
        error_if(ifaces[i] in ifaces[i + 1:],
              "Mention an interface more than once")
    if clazz.tag == "interface":
        check_cyclic(clazz, [])


def check_cyclic(iface, pifaces):
    error_if(iface in pifaces, "Cycle in interface")
    for eiface in [iface.env.findclass(name_to_str(x)) for x in
                   iface.findall(".//extends_interfaces/name")]:
        check_cyclic(eiface, pifaces + [iface])

cached_environments = {}
cached_trees = {}


def build_envs(files):
    """Lexes/Parses/does checking for all files in files."""
    global find_all_in_package_cache
    find_all_in_package_cache = {}
    trees = [ElementTree.ElementTree(file="Array.xml").getroot()]
    files = ["$Array.java"] + files
    trees[0].filename = "$Array.java"

    for f in files[1:]:
        if f in cached_trees:
            trees += [cached_trees[f]]
        else:
            CurrentFile.name = f
            tree = parse(lex(open(f).read()), f)
            cached_trees[f] = tree
            trees += [tree]
    name_to_class = {}

    for tree in trees:
        CurrentFile.name = tree.filename
        clazz = find_type_decl(tree)
        name = clazz.get("canonical_name")
        error_if(name in name_to_class, "Duplicate class defined.")
        if name.find(".") != -1:
            name_to_class[name] = clazz

    for x in range(0, len(trees)):
        CurrentFile.name = trees[x].filename
        if trees[x] not in cached_environments:
            build_environments(trees[x], trees, name_to_class)
            cached_environments[files[x]] = trees[x].env

    for tree in trees:
        CurrentFile.name = tree.filename
        clazz = find_type_decl(tree)
        clazz.env.add_superclass_methods()
        clazz.env.add_superclass_fields()
        check_types(tree)
        check_hierarchy(tree)

    return trees


def check(files):
    try:
        build_envs(files)
        return 0
    except JoosSyntaxException, e:
        if not Testing.testing:
            print e.msg
        return 42


if __name__ == '__main__':
    sys.exit(check(sys.argv[1:]))
