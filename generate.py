#!/usr/bin/env python2.6

import typechecker
from util import CurrentFile, Testing, JoosSyntaxException, modifiers, \
    collect_token_text, classof, argument_list_for_declaration, \
    enclosing_method, printall, find_type_decl, to_file, name_to_str, error_if, \
    isvariable, JoosSyntaxException, collect_debug_text, argument_list_for_declaration, \
    argument_list, isarray, is_primitive
import os
from elementtree.ElementTree import dump
import sys
import re

true = -1
false = 0
this = -2

class counters(object):
    mega_vtable_members = 0
    label_number = 0

class method_list(object):
    method_list = []
    class_list = []

def init_globals():
    counters.mega_vtable_members = 0
    counters.label_number = 0
    method_list.method_list = []
    method_list.class_list = []

def new_label_no():
    counters.label_number += 1
    return counters.label_number

def vtable_name_for_class(clazz):
    return "_vtable_" + mangle_class_name(clazz.get("canonical_name"))

def reserve_nulls(count):
    return "times " + str(count) + " dd 0\n"

def mega_vtable_for_class(class_declaration):
    assembly = vtable_name_for_class(class_declaration) + ":\n"
    assembly +=  "dd {type_tag}\n".format(type_tag=class_declaration.type_tag)

    zero_run_length = 0
    for method in method_list.method_list:
        name = method.get("name")
        args = argument_list_for_declaration(method.env, method)
        vtable_method = class_declaration.env.find_method_by_name(name, args)
        if vtable_method and vtable_method.find("block"):
            if zero_run_length > 0:
                assembly += reserve_nulls(zero_run_length)
                zero_run_length = 0;

            fn_name = mangle_fn_name(vtable_method)
            assembly += "dd " + fn_name + "\n"
        else:
            zero_run_length += 1
    assembly += reserve_nulls(zero_run_length)
    return assembly

def instanceof_table(trees):
    assembly = """
section .data
__instanceof_table:
"""
    rows = []
    for lhs in method_list.class_list:
        entries = []
        for rhs in method_list.class_list:
            if lhs.env.is_classes_subtype(lhs, rhs):
                entries.append(true)
            else:
                entries.append(false)
        row_name = lhs.get("canonical_name")
        rows.append("dd " + ", ".join(map(lambda x: "{0:>2}".format(str(x)), entries)) + " ; " + row_name)
    return assembly + "\n".join(rows) + "\n\n"

def check_and_generate(files):
    init_globals() # reset global state
    try:
        out = open("output/out.s", "w")

        trees = typechecker.check_files(files)
        initializer_list = []

        mega_vtable_offset = 1
        type_tag = 0
        string_literal_index = 0
        for tree in trees:
            clazz = find_type_decl(tree)
            clazz.type_tag = type_tag
            method_list.class_list += [clazz]
            type_tag += 1
            methods = tree.findall(".//method") + tree.findall(".//constructor_declaration") + \
                    tree.findall(".//abstract_method")
            for method in methods:
                method.mega_vtable_offset = mega_vtable_offset
                mega_vtable_offset += 1
                method_list.method_list += [method]
                if "static" in modifiers(method):
                    slot = -2
                else:
                    slot = -3
                for param in method.findall(".//param"):
                    param.slot = slot
                    slot -= 1

            counters.mega_vtable_members = mega_vtable_offset

            for string_literal in tree.findall(".//string_literal"):
                string_literal.index = string_literal_index
                string_literal_index += 1

        out.write( instanceof_table(trees) )

        for tree in trees:
            CurrentFile.name = tree.filename
            CurrentFile.mangled_name = CurrentFile.name.replace(".", "_").replace("$", "_").replace("/", "_")
            CurrentFile.static_slot = 0

            for this in tree.findall(".//tok_this"):
                this.slot = -2


            generate(tree)
            to_file(tree, tree.filename + ".xml")

            out.write( "section .data\n" )
            for clazz in tree.findall(".//class"):
                out.write( mega_vtable_for_class(clazz) )

            out.write( "section .text\n" )
            initializer_name = "static_init_" + CurrentFile.mangled_name
            out.write( """
; global {initializer_name}
{initializer_name}:
push ebp
mov ebp, esp
sub esp, {frame_size}
""".format(initializer_name=initializer_name,
                                  frame_size=CurrentFile.static_slot * 4))
            initializer_list.append(initializer_name)

            for field in tree.findall(".//field"):
                if "static" in modifiers(field):
                    mangled_name = mangle_field_name(field)
                    out.write( """
; initializing {mangled_name}
{field_assembly}
mov eax, {mangled_name}
mov ebx, {assigned_value}
mov DWORD [eax], ebx
""".format(mangled_name=mangled_name,
                                 field_assembly=field.assembly,
                                 assigned_value=stack_slot_to_operand(field.slot)))

            out.write( """
leave
ret
; done global static initialization
""")

            for constructor in tree.findall(".//constructor_declaration"):
                out.write( constructor.assembly + "\n")

            for method in tree.findall(".//method"):
                if method.find("block") is not None:
                    out.write( method.assembly + "\n" )

            out.write( "\nsection .data\n" )
            for string_literal in tree.findall(".//string_literal"):
                string_value = string_literal.get("value")
                expanded_value = expand_string_literal(string_value)
                out.write( "\n; string literal " + string_value + "\n")
                out.write( "__string_literal_" + str(string_literal.index) + ":\n" )
                out.write( "dd _vtable_java_lang_$Array_ ; vtable pointer\n" )
                out.write( "dd -3 ; type tag for char\n" )
                out.write( "dd " + str(len(expanded_value)) + " ; string length\n" )
                for character in expanded_value:
                    out.write( "dd " + str(hex(ord(character))) + "\n" )
                out.write( "" )

            out.write( "\nsection .bss\n" )
            for field in tree.findall(".//field"):
                if "static" in modifiers(field):
                    mangled_name = mangle_field_name(field)
                    out.write( """{mangled_name} resb 4""".format(mangled_name=mangled_name) + "\n")

        out.write( "section .text\n" )
        out.write( "; prelude\n" )
        out.write( "extern __malloc\n" )
        out.write( "extern __debexit\n" )
        out.write( "extern __exception\n" )
        out.write( "extern NATIVEjava.io.OutputStream.nativeWrite\n" )
        out.write( "global _start\n" )
        out.write( "_start:\n" )
        out.write( "call install_segv_handler\n" )

        for initializer in initializer_list:
            out.write( "call " + initializer + "\n")

        class_name = mangle_class_name(find_type_decl(
                trees[1]).get("canonical_name"))
        out.write( "call " + class_name + "test_\n" )
        out.write( "mov ebx, eax\n" )
        out.write( "mov eax, 1\n" )
        out.write( "int 0x80 ; invoke exit(1)\n" )
        out.write( "; end prelude\n" )
        out.write("""
%define __NR_signal 48
%define SIGSEGV     11
global install_segv_handler
install_segv_handler:
  mov eax, __NR_signal
  mov ebx, SIGSEGV
  mov ecx, __exception
  int 0x80
  ret
""")

        return 0
    except JoosSyntaxException, e:
        if Testing.testing:
            return 42
        else:
            out.write( "\n" + e.msg + "\n" )
            raise

def expand_string_literal(original_string):
    return original_string.decode("string_escape")

def bubble_stack_slot(function):
    def result(subtree):
        if len(subtree) == 1:
            if hasattr(subtree[0], "assembly"):
                subtree.assembly = subtree[0].assembly
            if hasattr(subtree[0], "memory_location"):
                subtree.memory_location = subtree[0].memory_location
            if hasattr(subtree[0], "slot"):
                subtree.slot = subtree[0].slot
            elif hasattr(subtree[0], "declaration") and hasattr(subtree[0].declaration, "slot"):
                subtree.slot = subtree[0].declaration.slot
        else:
            function(subtree)
    return result

def concat_child_assembly(function):
    def result(subtree):
        assembly = ""
        function(subtree)
        for child in subtree:
            if hasattr(child, "assembly"):
                assembly += child.assembly + "\n"

        if not hasattr(subtree, "assembly"):
            subtree.assembly = assembly
        else:
            subtree.assembly = "%s%s" % (assembly, subtree.assembly)
    return result

def lhs_address(subtree):
    if hasattr(subtree, "memory_location"):
        return "DWORD [ebx]"
    return stack_slot_to_operand(subtree.slot)

@concat_child_assembly
def assignment(subtree):
    subtree.slot = generate_new_stack_slot(subtree) #subtree[0].slot
    if hasattr(subtree[0], "memory_location"):
        subtree.memory_location = subtree[0].memory_location
        subtree.assembly = """
; assign {dbg}
mov eax, {value}
mov ebx, {memory_dst}
mov DWORD [ebx], eax
mov {value_dst}, eax
mov {value_dst2}, eax
; end assign
""".format(dbg=collect_debug_text(subtree),
           value=stack_slot_to_operand(subtree[-1].slot),
           memory_dst=stack_slot_to_operand(subtree.memory_location),
           value_dst=stack_slot_to_operand(subtree.slot),
           value_dst2=stack_slot_to_operand(subtree[0].slot))

def empty_statement(subtree):
    subtree.assembly = ""

def generate_new_stack_slot(subtree):
    method = enclosing_method(subtree)
    if method:
        method.slot += 1
        return method.slot

    CurrentFile.static_slot += 1
    return CurrentFile.static_slot

def stack_slot_to_operand(offset):
    return "DWORD [ebp - %s]" % (offset*4)


def instanceof_assembly(value_slot, destination_slot, type_subtree,
                        debug_string, isarray = False):
    rhs_type = type_subtree.env.findclass(name_to_str(type_subtree))
    label_no = new_label_no()
    zero_case = "EQUALITY_ZERO_" + str(label_no)
    one_case = "EQUALITY_ONE_" + str(label_no)
    final = "EQUALITY_FINAL_" + str(label_no)


    #TODO: arrays
    if rhs_type is None or isarray:
        return """
;instanceof_array {dbg}
mov eax, {lhs}
sub eax, 0
jz .{false_case}
mov ebx, [eax]
mov ebx, [ebx]

sub ebx, 0
jz .{array_case}
jmp .{false_case}
.{array_case}:
mov eax, [eax + 4]
sub eax, {type_tag_rhs}
jnz .{false_case}
mov {result}, {true}
jmp .{final}
.{false_case}:
mov {result}, {false}
.{final}:
;end instanceof
""".format(lhs=stack_slot_to_operand(value_slot),
           dbg=debug_string,
           array_case=zero_case,
           false_case=one_case,
           type_tag_rhs=type_tag_of_subtree(type_subtree, True),
           result=stack_slot_to_operand(destination_slot),
           true=true,
           final=final,
           false=false)

    else:
        return """
; instanceof {dbg}
mov eax, {lhs}
sub eax, 0
jz .{zero_case} ; check for null
mov eax, [eax] ; deference to object
mov eax, [eax] ; dereference to vable

mov ecx, {number_of_classes}
imul ecx
add eax, {type_tag}

mov eax, [__instanceof_table + eax]
sub eax, -1
jz .{one_case}
.{zero_case}:
mov {result}, {false}
jmp .{final_location}
.{one_case}:
mov {result}, {true}
.{final_location}:
""".format(
        dbg=debug_string,
        type_tag = str(rhs_type.type_tag * 4),
        lhs=stack_slot_to_operand(value_slot),
        zero_case=zero_case,
        one_case=one_case,
        result=stack_slot_to_operand(destination_slot),
        true=true,
        false=false,
        final_location=final,
        number_of_classes = str(len(method_list.class_list) * 4))


def instanceof_expression(subtree):
    lhs_location = subtree[0].slot
    subtree.slot = generate_new_stack_slot(subtree)
    subtree.assembly = instanceof_assembly(lhs_location, subtree.slot,
                                           subtree[2],
                                           collect_debug_text(subtree))


# TODO: Handle instanceof properly.
@bubble_stack_slot
@concat_child_assembly
def comparison_expression(subtree):
    if subtree[1].tag == "tok_instanceof":
        instanceof_expression(subtree)
        return
    label_no = new_label_no()
    zero_case = "EQUALITY_ZERO_" + str(label_no)
    one_case = "EQUALITY_ONE_" + str(label_no)
    final = "EQUALITY_FINAL_" + str(label_no)

    lhs_location = subtree[0].slot
    rhs_location = subtree[2].slot
    subtree.slot = generate_new_stack_slot(subtree)
    jump_if_zero_location = one_case
    jump = ""
    cmp_expression = ""
    if collect_token_text(subtree[1]) == "==":
        jump = "JZ"
    elif subtree[1].tag == "tok_gt":
        jump = "JG"
    elif subtree[1].tag == "tok_lt":
        jump = "JL"
    elif subtree[1].tag == "tok_lteq":
        jump = "JLE"
    elif subtree[1].tag== "tok_gteq":
        jump = "JGE"
    elif collect_token_text(subtree[1]) == "!=":
        jump = "JNZ"

    subtree.assembly = """
; equality expression
mov eax, {lhs}
mov ebx, {rhs}
sub eax, ebx
{jump} .{jump_if_zero_location}
.{zero_case}:
mov {result}, {false}
JMP .{final_location}
.{one_case}:
mov {result}, {true}
.{final_location}:
;end equality expression
""".format(lhs=stack_slot_to_operand(lhs_location),
           rhs=stack_slot_to_operand(rhs_location),
           result=stack_slot_to_operand(subtree.slot),
           cmp_expression=cmp_expression,
           jump_if_zero_location=jump_if_zero_location,
           final_location=final,
           zero_case=zero_case,
           one_case=one_case,
           jump=jump,
           false=false,
           true=true
           )

@bubble_stack_slot
def bubble(_):
    pass

@bubble_stack_slot
@concat_child_assembly
def multiplicative_expression(subtree):
    lhs_location = subtree[0].slot
    rhs_location = subtree[2].slot
    new_stack_slot = generate_new_stack_slot(subtree)
    operator_type = collect_token_text(subtree[1])
    result = operator = ""
    if operator_type == "*":
        operator = "imul"
        result = "eax"
        check = ""
    elif operator_type == "/":
        operator = "idiv"
        result = "eax"
        label_no = new_label_no()
        check = """
sub ebx, 0
jne .{okay_label}
call __exception
.{okay_label}:
""".format(okay_label="DIV0_CHECK_"+str(label_no))
    elif operator_type == "%":
        operator = "idiv"
        result = "edx"
        check = ""
    else:
        error_if(True, "Unknown argument to mulitplicative expression")
    subtree.assembly = """
; multiplicative {dbg}
mov edx, {lhs}
mov eax, edx
sar edx, 31
mov ebx, {rhs}
{check}
{op} ebx
mov {nss}, {result}
; end multiplicative
""".format(
            nss=stack_slot_to_operand(new_stack_slot),
            lhs=stack_slot_to_operand(lhs_location),
            rhs=stack_slot_to_operand(rhs_location),
            result=result,
            check=check,
            op=operator,
            imul_part= operator=="imul" and ", edx" or "",
            dbg=collect_debug_text(subtree))
    subtree.slot = new_stack_slot

@concat_child_assembly
def local_variable_declaration(subtree):
    subtree.slot = generate_new_stack_slot(subtree)
    subtree.assembly = """
; local variable declaration {dbg}
mov eax, {source}
mov {dest}, eax
; end local variable declaration
""".format(dbg=collect_debug_text(subtree),
        dest = stack_slot_to_operand(subtree.slot),
        source = stack_slot_to_operand(subtree.find("expression").slot))

def empty_expression(subtree):
    value = subtree.get("value")
    if value == "True":
        value = true
    elif value == "False":
        value = false
    error_if(value is None, "None in empty expression!")
    new_stack_slot = generate_new_stack_slot(subtree)
    subtree.assembly = """
; empty expr {dbg}
mov {nss}, {val}
; end empty expr
""".format(nss=stack_slot_to_operand(new_stack_slot),
                           val=value,
                           dbg=collect_debug_text(subtree))
    subtree.slot = new_stack_slot

@concat_child_assembly
def return_statement(subtree):
    method = enclosing_method(subtree)
    if method.tag == "constructor_declaration":
        subtree.assembly = """
; return from constructor
mov eax, {this}
leave
ret
""".format(this=stack_slot_to_operand(this))
        return

    expression = subtree.find("expression")
    subtree.assembly = """
leave
ret
; end return statement
"""
    if expression is not None:
        child_slot = expression.slot
        subtree.assembly = """
mov eax, {child_slot}
{return_assembly}
""".format(child_slot=stack_slot_to_operand(child_slot),
           return_assembly=subtree.assembly)

@bubble_stack_slot
@concat_child_assembly
def expression(subtree):
    if not len(subtree):
        empty_expression(subtree)


def method_declaration_asm(assembly, mangled_name, subtree, prefix=""):
    return """
{method_name}:

push ebp
mov ebp, esp
sub esp, {frame_size}
{prefix}
{asm}
; end method decl
""".format(method_name=mangled_name, asm=assembly,
                            frame_size=subtree.slot * 4, prefix=prefix)

def method(subtree):
    mangled_name = mangle_fn_name(subtree)
    method_block = subtree.find("block")
    if method_block is not None:
        subtree.assembly = method_declaration_asm(method_block.assembly,
                                                  mangled_name, subtree)
        subtree.assembly += """
leave
ret
; end method {name}
""".format(name=mangled_name)

@bubble_stack_slot
@concat_child_assembly
def field(subtree):
    if "static" in modifiers(subtree):
        for sub in subtree:
            if hasattr(sub, "slot"):
                subtree.slot = sub.slot
                return


def constructor_declaration(subtree):
    mangled_name = mangle_fn_name(subtree)
    constructor_body = subtree.find("constructor_body")
    error_if(constructor_body is None, "No constructor body")

    superclass = subtree.env.findclass("this").superclass
    superclass_mangled_name = mangle_class_name(superclass.get("canonical_name"))
    superclass_constructor = superclass_mangled_name + mangle_class_name(superclass.get("name"))

    fields = subtree.env.findclass("this").findall(".//field")
    field_initializers = ""
    for field in fields:
        if "static" not in modifiers(field) and field.find("expression") is not None:
            if not hasattr(field.find("expression"), "assembly"):
                generate(field.find("expression"))
            field_initializers += field.find("expression").assembly + "\n"
            field_initializers += """
; field_initializer
mov eax, DWORD [ebp + 8] ; this -> eax
add eax, {field_location}
mov ebx, {value}
mov DWORD [eax], ebx
; end_field_initializer
""".format(field_location=field.env.find_nonlocal(collect_token_text(field.find("variable"))).field_offset * 4,
                                 value=stack_slot_to_operand(field.find("expression").slot))

    chained_constructor_call = """
;initialize fields
{field_initializers}
; call superclass default constructor
push DWORD [ebp + 8]
call {superclass_constructor}
""".format(superclass_constructor=superclass_constructor, field_initializers=field_initializers)
    this_class = subtree.env.findclass("this")
    if this_class.get("canonical_name") == "java.lang.Object":
        chained_constructor_call = field_initializers

    subtree.assembly = method_declaration_asm(constructor_body.assembly,
            mangled_name, subtree, chained_constructor_call)
    subtree.assembly += """
mov eax, {this_ptr}
leave
ret
; end constructor {name}
""".format(this_ptr=stack_slot_to_operand(this),
           name=mangled_name)

def binary_operator_assembly(lhs_slot, rhs_slot, op, destination_slot,
                             debug_string):
    return """
; begin {dbg}
mov eax, {lhs}
mov ebx, {rhs}
{op} eax, ebx
mov {destination}, eax
; end {dbg}
""".format(dbg=debug_string,
           lhs=stack_slot_to_operand(lhs_slot),
           op=op,
           rhs=stack_slot_to_operand(rhs_slot),
           destination=stack_slot_to_operand(destination_slot))

def string_encoder_for_type(type_name):
    if is_primitive(type_name) or type_name == "java.lang.String":
        return "java_lang_String_valueOf_" + mangle_class_name(type_name)
    return "java_lang_String_valueOf_java_lang_Object_"

def generate_promotion_to_string(subtree):
    subtree_type = subtree.get("type")

    string_encoder = string_encoder_for_type(subtree_type)
    promoted_slot = generate_new_stack_slot(subtree)
    promotion_assembly = """
; promotion from {subtree_type} to java.lang.String
push {subtree_slot}
call {string_encoder}
mov {promoted_slot}, eax
""".format(subtree_type=subtree_type,
           subtree_slot=stack_slot_to_operand(subtree.slot),
           string_encoder=string_encoder,
           promoted_slot=stack_slot_to_operand(promoted_slot))
    return (promoted_slot, promotion_assembly)

@bubble_stack_slot
@concat_child_assembly
def additive_expression(subtree):
    lhs_slot = subtree[0].slot
    rhs_slot = subtree[2].slot
    result_slot = generate_new_stack_slot(subtree)

    lhs_type = subtree[0].get("type")
    rhs_type = subtree[2].get("type")
    if "java.lang.String" in [lhs_type, rhs_type]:
        (lhs_slot, lhs_assembly) = generate_promotion_to_string(subtree[0])
        (rhs_slot, rhs_assembly) = generate_promotion_to_string(subtree[2])
        assembly = """
; string additive expression
{lhs_assembly}
{rhs_assembly}

mov eax, {lhs_slot}
mov ebx, {rhs_slot}

push ebx
push eax
call java_lang_String_concat_java_lang_String_
mov {result_slot}, eax
""".format(lhs_assembly=lhs_assembly,
           rhs_assembly=rhs_assembly,
           rhs_slot=stack_slot_to_operand(rhs_slot),
           lhs_slot=stack_slot_to_operand(lhs_slot),
           result_slot=stack_slot_to_operand(result_slot))
        subtree.assembly = assembly
        subtree.slot = result_slot
        return

    operator_type = collect_token_text(subtree[1])
    operator = ""
    if operator_type == "+":
        operator = "add"
    elif operator_type == "-":
        operator = "sub"
    else:
        error_if(True, "Unknown additive_expression operator_type")

    subtree.assembly = binary_operator_assembly(lhs_slot, rhs_slot,
                                                operator, result_slot,
                                                collect_debug_text(subtree))
    subtree.slot = result_slot


@bubble_stack_slot
def lazy_and_expression(subtree):
    label_no = new_label_no()
    subtree.slot = generate_new_stack_slot(subtree)
    subtree.assembly = """
{lhs}
cmp {lhs_value}, {true}
jne .{false_label}
{rhs}
cmp {rhs_value}, {true}
jne .{false_label}
mov {dest}, {true}
jmp .{expr_end}
.{false_label}:
mov {dest}, {false}
.{expr_end}:
""".format(lhs = subtree[0].assembly,
                      rhs = subtree[2].assembly,
                      false_label = "lazy_and_false_" + str(label_no),
                      lhs_value = stack_slot_to_operand(subtree[0].slot),
                      rhs_value = stack_slot_to_operand(subtree[2].slot),
                      dest = stack_slot_to_operand(subtree.slot),
                      expr_end = "lazy_and_end_" + str(label_no),
                      false=false,
                      true=true)

@bubble_stack_slot
@concat_child_assembly
def eager_and_expression(subtree):
    error_if(subtree[1].tag != "tok_bit_and",
             "Unexpected structure to eager and expression")
    subtree.slot = generate_new_stack_slot(subtree)
    subtree.assembly = binary_operator_assembly(subtree[0].slot,
                                                subtree[2].slot,
                                                "and",
                                                subtree.slot,
                                                collect_debug_text(subtree))

@bubble_stack_slot
def lazy_or_expression(subtree):
    label_no = new_label_no()
    subtree.slot = generate_new_stack_slot(subtree)
    subtree.assembly = """
{lhs}
cmp {lhs_value}, {true}
je .{true_label}
{rhs}
cmp {rhs_value}, {true}
je .{true_label}
mov {dest}, {false}
jmp .{expr_end}
.{true_label}:
mov {dest}, {true}
.{expr_end}:
""".format(lhs = subtree[0].assembly,
                      rhs = subtree[2].assembly,
                      true_label = "lazy_or_false_" + str(label_no),
                      lhs_value = stack_slot_to_operand(subtree[0].slot),
                      rhs_value = stack_slot_to_operand(subtree[2].slot),
                      dest = stack_slot_to_operand(subtree.slot),
                      expr_end = "lazy_or_end_" + str(label_no),
                      false=false,
                      true=true)

@bubble_stack_slot
@concat_child_assembly
def eager_or_expression(subtree):
    error_if(subtree[1].tag != "tok_bit_or",
             "Unexpected structure to eager or expression")
    subtree.slot = generate_new_stack_slot(subtree)
    subtree.assembly = binary_operator_assembly(subtree[0].slot,
                                                subtree[2].slot,
                                                "or",
                                                subtree.slot,
                                                collect_debug_text(subtree))

@concat_child_assembly
def class_instance_creation(subtree):
    subtree.slot = generate_new_stack_slot(subtree)
    declaration_site = typechecker.resolve_constructor_name(subtree)
    size = (declaration_site.env.findclass("this").num_fields + 1) * 4
    # TODO: Initialize the vtable somehow
    constructor_name = mangle_fn_name(declaration_site)
    vtable_name = vtable_name_for_class(declaration_site.env.findclass("this"))
    pushes = push_arguments(subtree)
    return_slot = stack_slot_to_operand(subtree.slot)
    subtree.assembly = """
; invoke constructor {dbg}
mov eax, {size}
call __malloc
mov DWORD [eax], {vtable}
{pushes}
push eax
call {constructor}
mov {return_slot}, eax
; end invoke constructor
""".format(dbg=collect_debug_text(subtree), size=size,
           constructor=constructor_name,
           pushes="\n".join(pushes),
           return_slot=return_slot,
           vtable=vtable_name)

@concat_child_assembly
def method_invocation(subtree):
    method = subtree.declaration
    subtree.slot = generate_new_stack_slot(subtree)
    pushes = push_arguments(subtree)
    if "static" not in modifiers(method):
        if subtree[0].tag == "name":
            name(subtree[0], args=argument_list(subtree))
        pushes.append("push " + stack_slot_to_operand(subtree[0].slot))

    return_slot = stack_slot_to_operand(subtree.slot)
    if "native" in modifiers(method):
        call = "call " + mangle_native_fn_name(subtree.declaration)
        argument_slot = subtree.find("./argument_list").slot
        operand = stack_slot_to_operand(argument_slot)
        pushes = ["mov eax, {slot}".format(slot=operand)]
    elif "static" in modifiers(method):
        call = "call " + mangle_fn_name(subtree.declaration)
    else:
        call = """
mov eax, {this_ptr}
mov eax, [eax]
add eax, {method_offset}
mov eax, [eax]
call eax
""".format(this_ptr = stack_slot_to_operand(subtree[0].slot),
           method_offset = str(4 * method.mega_vtable_offset))

    subtree.assembly = """
; method invocation {dbg}
{push_arguments}
{call}
mov {return_slot}, eax
; end method invocation
""".format(dbg=collect_debug_text(subtree),
           call=call,
           push_arguments="\n".join(pushes),
           return_slot=return_slot)

@bubble_stack_slot
@concat_child_assembly
def bubble_stack_slot_and_concat_child_assembly(_):
    pass

@bubble_stack_slot
@concat_child_assembly
def unary_expression(subtree):
    if subtree[0].tag == "tok_minus":
        # Unary minus
        subtree.slot = subtree[1].slot
        subtree.assembly = """
; Unary Minus {dbg}
neg {reg}
""".format(dbg=collect_debug_text(subtree),
           reg=stack_slot_to_operand(subtree.slot))

@bubble_stack_slot
@concat_child_assembly
def unary_expression_not_plus_minus(subtree):
    if subtree[0].tag == "tok_complement":
        # Unary boolean complement
        subtree.slot = subtree[1].slot
        subtree.assembly ="""
; Unary complement {dbg}
not {reg}
""".format(dbg=collect_debug_text(subtree),
                    reg=stack_slot_to_operand(subtree.slot))

@concat_child_assembly
def array_creation_expression(subtree):
    expr = subtree.find("dim_expr")
    subtree.slot = generate_new_stack_slot(subtree)
    subtree.assembly = """
mov eax, {expr_val}
mov ebx, 4
mov ecx, eax
imul ebx
add eax, 12
call __malloc
mov {dest}, eax
mov DWORD [eax], _vtable_java_lang_$Array_
mov DWORD [eax + 4], {type_tag}
mov DWORD [eax + 8], ecx
""".format(expr_val=stack_slot_to_operand(expr.slot),
           dest=stack_slot_to_operand(subtree.slot),
           type_tag=type_tag_of_subtree(subtree[1])
           )

def type_tag_of_subtree(subtree, if_array_then_contents = False):
    if isarray(collect_token_text(subtree)):
        if if_array_then_contents:
           subtree = subtree[0]
    if subtree.tag == "primitive_type":
        return  {"short" : -1,
                 "int": -2,
                 "char": -3,
                 "byte": -4,
                 "boolean": -5}[collect_token_text(subtree)]
    return subtree.env.findclass(name_to_str(subtree)).type_tag


@bubble_stack_slot
@concat_child_assembly
def dim_expr(subtree):
    subtree.slot = subtree[1].slot
    subtree.assembly = subtree[1].assembly

@concat_child_assembly
def array_access(subtree):
    subtree.slot = generate_new_stack_slot(subtree)
    subtree.memory_location = generate_new_stack_slot(subtree)
    subtree.assembly = """
; array access {dbg}
mov eax, {expression_value}
mov ebx, {array_pointer}

; array bounds check
mov edx, [ebx + 8]
cmp edx, eax
jle __exception

mov ecx, 4
imul ecx
add eax, 12
add eax, ebx
mov {memory_location}, eax
mov ebx, [eax]
mov {destination}, ebx
; done array access
""".format(dbg=collect_debug_text(subtree),
           expression_value=stack_slot_to_operand(subtree[2].slot),
           array_pointer=stack_slot_to_operand(subtree[0].slot),
           memory_location=stack_slot_to_operand(subtree.memory_location),
           destination=stack_slot_to_operand(subtree.slot))

@concat_child_assembly
def field_access(subtree):
    subtree.slot = generate_new_stack_slot(subtree)
    subtree.memory_location = generate_new_stack_slot(subtree)
    if "static" in modifiers(subtree.declaration):
        mangled_name = mangle_field_name(subtree)
        subtree.assembly = """
; static field access to {mangled_named}
mov eax, {mangled_name}
mov {memory_dst}, eax
mov {value_dst}, DWORD [eax]
""".format(mangled_name=mangled_name,
           memory_dst=stack_slot_to_operand(subtree.memory_location),
           value_dst=stack_slot_to_operand(subtree.slot))

    else:
        subtree.assembly = """
mov eax, {object_location}
mov ebx, [eax + {field_offset}]
mov {dest}, ebx
add eax, {field_offset}
mov {mem_loc}, eax
""".format(object_location=stack_slot_to_operand(subtree[0].slot),
           field_offset=subtree.declaration.field_offset * 4,
           dest=stack_slot_to_operand(subtree.slot),
           mem_loc=stack_slot_to_operand(subtree.memory_location))

def while_statement(subtree):
    body = subtree[-1].assembly
    label_no = new_label_no()
    while_start = "WHILE_" + str(label_no) + "_start"
    while_end = "WHILE_" + str(label_no) + "_end"
    subtree.assembly = """
; while statement begin
.{top_of_loop}:
; while statement check
{check_asm}
; while statement check end
cmp {lhs}, 0
jz .{bottom_of_loop}
;while statement body
{body}
;while statement body end
jmp .{top_of_loop}
.{bottom_of_loop}:
;while statement end
""".format(top_of_loop = while_start,
                           body = body,
                           bottom_of_loop = while_end,
                           lhs = stack_slot_to_operand(
                                   subtree.find("./expression").slot),
                           check_asm=subtree.find("expression").assembly)
    subtree.find("./expression").assembly = ""

def if_then_statement(subtree):
    condition_asm = subtree[2].assembly
    then_asm = subtree.find("then").assembly
    else_asm = subtree.find("else").assembly  # Empty string if no else block
    condition_slot = subtree[2].slot
    label_no = new_label_no()
    top_of_else_label = "ELSE_" + str(label_no) + "_top"
    bottom_of_else_label = "ELSE_" + str(label_no) + "_bottom"
    subtree.assembly = """
; begin if statement, test condition if ({dbg})
{condition_asm}
cmp {condition_slot}, 0
jz .{top_of_else_label}
; end if ({dbg}) condition check, begin then block
{then_asm}
jmp .{bottom_of_else_label}
; end if ({dbg}) then block, begin else block
.{top_of_else_label}:
{else_asm}
.{bottom_of_else_label}:
; end if ({dbg}) else block
""".format(dbg=collect_debug_text(subtree[2]),
           condition_asm=condition_asm,
           condition_slot=stack_slot_to_operand(condition_slot),
           bottom_of_else_label=bottom_of_else_label,
           then_asm=then_asm,
           top_of_else_label=top_of_else_label,
           else_asm=else_asm)

def for_statement(subtree):
    for_init_asm = subtree.find("for_init").assembly
    for_test_asm = subtree[3].assembly
    for_test_slot = subtree[3].slot
    for_update_asm = ""
    if subtree.find("for_update") is not None:
        for_update_asm = subtree.find("for_update").assembly
    body_asm = subtree[-1].assembly
    label_no = new_label_no()
    top_of_loop_label = "FOR_" + str(label_no) + "_top"
    bottom_of_loop_label = "FOR_" + str(label_no) + "_bottom"
    debug_string = collect_debug_text(subtree[0:6])
    subtree.assembly = """
; begin {dbg} init
{for_init_asm}
.{top_of_loop_label}:
; begin {dbg} test
{for_test}
; end for statement test
cmp {for_test_slot}, 0
jz .{bottom_of_loop_label}
; {dbg} body
{body_asm}
; end for statement body, for statement update:
{for_update_asm}
jmp .{top_of_loop_label}
.{bottom_of_loop_label}:
; end for statement {dbg}
""".format(dbg=debug_string,
           for_init_asm=for_init_asm,
           top_of_loop_label=top_of_loop_label,
           for_test=for_test_asm,
           for_test_slot=stack_slot_to_operand(for_test_slot),
           bottom_of_loop_label=bottom_of_loop_label,
           body_asm=body_asm,
           for_update_asm=for_update_asm)


def string_literal(subtree):
    subtree.slot = generate_new_stack_slot(subtree)
    subtree.assembly = """
; loading __string_literal_{index}
mov eax, 8
call __malloc
mov DWORD [eax + 0], _vtable_java_lang_String_
push __string_literal_{index}
push eax
call java_lang_String_String_char__lbrace____rbrace___
mov {value_slot}, eax
""".format(index=subtree.index,
           value_slot=stack_slot_to_operand(subtree.slot))

# TODO: Proper cast expressions.
@bubble_stack_slot
@concat_child_assembly
def cast_expression(subtree):
    if subtree[1].tag == "name":
        expression_being_cast = subtree.find("unary_expression_not_plus_minus")
        cast_tree = subtree[1]
        #if element.find("dims"):
        #    cast_type += "[]"
    elif subtree[1].tag == "expression":
        # Expression case
        cast_tree = subtree[1]
        expression_being_cast = subtree[-1]
    elif subtree.find("dims") is not None:
        cast_tree = subtree[1]
        expression_being_cast = subtree[-1]
    else:
        # Primitive cast case
        subtree.slot = subtree[-1].slot
        if hasattr(subtree[-1], "memory_location"):
            subtree.memory_location = subtree[-1].memory_location
        return
    slot = generate_new_stack_slot(subtree)
    value_slot = expression_being_cast.slot
    debug_string = "ClassCastException check  " + \
            collect_debug_text(subtree) + \
            " with result in " + stack_slot_to_operand(slot)
    subtree.assembly = instanceof_assembly(value_slot, slot,
                                           cast_tree,
                                           debug_string,
                                           isarray = subtree.find("dims") is not None)
    valid_label = ".VALID_CAST_" + str(new_label_no())
    subtree.assembly += """
; Raise exception if instanceof check failed
mov eax, {test_slot}
sub eax, -1
jz {valid_label}
; check for null (can cast null to reference types)
mov eax, {lhs_slot}
sub eax, 0
jz {valid_label}
call __exception
{valid_label}:
""".format(lhs_slot=stack_slot_to_operand(value_slot),
        valid_label=valid_label,
           test_slot=stack_slot_to_operand(slot))
    subtree.slot = subtree[-1].slot
    if hasattr(subtree[-1], "memory_location"):
        subtree.memory_location = subtree[-1].memory_location

def generate(subtree):
    for child in subtree:
        generate(child)

    switch = {
        "argument_list": bubble_stack_slot_and_concat_child_assembly,
        "cast_expression": cast_expression,
        "additive_expression": additive_expression,
        "primary": bubble,
        "field_access": field_access,
        "primary_no_new_array": bubble,
        "array_creation_expression": array_creation_expression,
        "array_access": array_access,
        "multiplicative_expression": multiplicative_expression,
        "equality_expression": comparison_expression,
        "dim_expr": dim_expr,
        "relational_expression": comparison_expression,
        "expression": expression,
        "return_statement": return_statement,
        "method": method,
        "variable_initializer": bubble,
        "local_variable_declaration": local_variable_declaration,
        "integer_literal": empty_expression,
        "null_literal": empty_expression,
        "boolean_literal": empty_expression,
        "character_literal": empty_expression,
        "literal": bubble,
        "while_statement": while_statement,
        "left_hand_side": bubble,
        "empty_statement":empty_statement,
        "class_instance_creation_expression": class_instance_creation,
        "method_invocation": method_invocation,
        "constructor_declaration": constructor_declaration,
        "block": bubble_stack_slot_and_concat_child_assembly,
        "constructor_body": bubble_stack_slot_and_concat_child_assembly,
        "assignment": assignment,
        "assignment_expression": bubble,
        "name": name,
        "unary_expression": unary_expression,
        "unary_expression_not_plus_minus": unary_expression_not_plus_minus,
        "conditional_and_expression": lazy_and_expression,
        "and_expression": eager_and_expression,
        "conditional_or_expression": lazy_or_expression,
        "inclusive_or_expression": eager_or_expression,
        "exclusive_or_expression": bubble,
        "field": field,
        "then": bubble_stack_slot_and_concat_child_assembly,
        "else": bubble_stack_slot_and_concat_child_assembly,
        "if_then_statement": if_then_statement,
        "for_init": bubble_stack_slot_and_concat_child_assembly,
        "for_update": bubble_stack_slot_and_concat_child_assembly,
        "for_statement": for_statement,
        "string_literal": string_literal,
        "shift_expression": bubble,
    }

    if subtree.tag in switch:
        switch[subtree.tag](subtree)

def push_arguments(subtree):
    pushes = []
    if "static" in modifiers(subtree):
        return pushes

    if subtree.find("./argument_list") is not None:
        for expr in subtree.find("./argument_list"):
            pushes.insert(0, push_to_stack(stack_slot_to_operand(expr.slot)))

    return pushes


def mangle_class_name(classname):
    return re.sub("\\.", "_", classname) + "_"


def mangle_fn_name(method_decl):
    name = mangle_class_name(classof(method_decl)) \
        + method_decl.get("name") + "_"
    for arg in argument_list_for_declaration(method_decl.env, method_decl):
        name += arg.replace("[", "__lbrace__").replace("]", "__rbrace__") + "_"
    return name.replace(".", "_")

def mangle_native_fn_name(method_decl):
    result = "NATIVE"
    result += mangle_class_name(classof(method_decl))
    result += method_decl.get("name")
    return result.replace("_", ".")


def mangle_field_name(field_decl):
    return mangle_class_name(classof(field_decl)) +\
           "_" + collect_token_text(field_decl.find("./variable")) + "_"


def push_to_stack(location):
    return """push %s""" % location


def get_all_classes(trees):
    return [tree.find(".//class") for tree in trees if tree.find(".//class")]


def get_static_fields(clazz):
    env = clazz.env
    return [env[field_name] for field_name in env.fields
            if "static" in modifiers(env[field_name])]


def get_nonstatic_fields(clazz):
    env = clazz.env
    return [env[field_name] for field_name in env.fields
            if "static" not in modifiers(env[field_name])]


def get_initializer(variable):
    return variable.find("./variable_initializer")

def name(subtree, args = None):
    #TODO: pathing
    #subtree.slot = subtree.declaration.slot
    try:
        path = subtree.env.get_declaration_path_for_name(name_to_str(subtree), args)
        if not path:
            return

        subtree.assembly = "; name {dbg}\n".format(dbg=collect_debug_text(subtree))
        if path[0].tag == "method" or path[0].tag == "abstract_method":
            subtree.slot = this
        if path[0].tag == "class":
            subtree.slot = generate_new_stack_slot(subtree)
            subtree.memory_location = generate_new_stack_slot(subtree)
            mangled_name = mangle_field_name(path[1])
            subtree.assembly += """
mov eax, {mangled_name}
mov ebx, DWORD [eax]
mov {memory_dst}, eax
mov {value_dst}, ebx
""".format(mangled_name=mangled_name,
                               memory_dst=stack_slot_to_operand(subtree.memory_location),
                               value_dst=stack_slot_to_operand(subtree.slot))
            path = path[1:]
        elif path[0].tag == "field":
                subtree.slot = generate_new_stack_slot(subtree)
                subtree.memory_location = generate_new_stack_slot(subtree)
                subtree.assembly += """
mov eax, DWORD [ebp + 8] ; this -> eax
mov ebx, [eax + {field_location}]
add eax, {field_location}
mov {mem_loc}, eax
mov {dest}, ebx
""".format(field_location=path[0].field_offset * 4,
           dest=stack_slot_to_operand(subtree.slot),
           mem_loc=stack_slot_to_operand(subtree.memory_location))
        elif path[0].tag == "local_variable_declaration" or path[0].tag == "param":
            if not hasattr(path[0], "slot"):
                return
            subtree.slot = generate_new_stack_slot(subtree)
            subtree.memory_location = generate_new_stack_slot(subtree)
            subtree.assembly += """
mov eax, {source}
mov {dest}, eax
mov ebx, ebp
sub ebx, {source_stack_slot}
mov {mem_loc}, ebx
""".format(source=stack_slot_to_operand(path[0].slot),
           source_stack_slot = path[0].slot * 4,
           mem_loc = stack_slot_to_operand(subtree.memory_location),
           dest=stack_slot_to_operand(subtree.slot))
        for child in path[1:]:
            if child.tag in ["method", "abstract_method"]:
                return
            former_slot = subtree.slot
            subtree.slot = generate_new_stack_slot(subtree)
            subtree.memory_location = generate_new_stack_slot(subtree)
            if not hasattr(subtree, "assembly"):
                subtree.assembly = ""
            subtree.assembly += """
mov eax, {former_location}
mov ebx, [eax + {field_location}]
add eax, {field_location}
mov {mem_loc}, eax
mov {dest}, ebx
""".format(former_location=stack_slot_to_operand(former_slot),
           field_location=child.field_offset * 4,
           dest=stack_slot_to_operand(subtree.slot),
           mem_loc=stack_slot_to_operand(subtree.memory_location))

    except JoosSyntaxException:
        pass

def create_globl_section(trees):
    asm = ""
    for tree in trees:
        for method in tree.findall(".//method") + \
                tree.findall(".//constructor_declaration"):
            asm += ".globl " + mangle_fn_name(method)
        for field in tree.findall(".//field"):
            if "static" in modifiers(field):
                asm += ".globl " + mangle_field_name(field)
                #TODO: something

if __name__ == '__main__':
    files = sys.argv[1:]
    sys.exit(check_and_generate(files))

