#!/usr/bin/env python2.6
#TODO: remove bit_complement from working.cfg


import re
import sys
from Token import Token
from util import error_if, JoosSyntaxException


#List of tokens that are allowed in java and dissallowed in Joos
disallowed_tokens = ["switch", "case", "throw", "synchronized", "volatile",
                     "default", "do", "break", "continue", "catch", "try",
                     "finally", "t_throws", "goto", "double", "float", "long",
                     "strictfp", "transient", "colon", "bit_complement",
                     "minus_minus", "plus_plus", "floating_point_literal",
                     "question", "hex_integer_literal"]

#List of keyword and operator tokens in Java
tokens = {
    ">>>": "unsigned_shift_right",
    ">>>=": "unsigned_shift_right_assign",
    ">>=": "signed_shift_right_assign",
    "<<=": "shift_left_assign",
    "<=": "lteq",
    "!=": "neq",
    "*=": "star_assign",
    "/=": "div_assign",
    "-=": "minus_assign",
    "++": "plus_plus",
    "&=": "bit_and_assign",
    "--": "minus_minus",
    "^=": "bit_xor_assign",
    "||": "or",
    "<<": "shift_left",
    "|=": "bit_or_assign",
    ">=": "gteq",
    "+=": "plus_assign",
    "==": "eq",
    "%=": "mod_assign",
    ">>": "signed_shift_right",
    "&&": "and",
    "{": "l_brace",
    "%": "mod",
    "&": "bit_and",
    "}": "r_brace",
    ")": "r_parenthese",
    "!": "complement",
    "?": "question",
    "<": "lt",
    ".": "dot",
    "^": "bit_xor",
    "(": "l_parenthese",
    ">": "gt",
    "=": "assign",
    "-": "minus",
    "/": "div",
    ";": "semicolon",
    "*": "star",
    "|": "bit_or",
    ",": "comma",
    "[": "l_bracket",
    "~": "bit_complement",
    "+": "plus",
    "]": "r_bracket",
    ":": "colon",
    "new": "new",
    "default": "default",
    "abstract": "abstract",
    "false": "false",
    "goto": "goto",
    "private": "private",
    "const": "const",
    "import": "import",
    "package": "package",
    "throw": "throw",
    "continue": "continue",
    "null": "null",
    "boolean": "boolean",
    "byte": "byte",
    "for": "for",
    "public": "public",
    "transient": "transient",
    "do": "do",
    "instanceof": "instanceof",
    "true": "true",
    "static": "static",
    "protected": "protected",
    "int": "int",
    "return": "return",
    "case": "case",
    "implements": "implements",
    "super": "t_super",
    "while": "while",
    "double": "double",
    "strictfp": "strictfp",
    "synchronized": "synchronized",
    "void": "void",
    "switch": "switch",
    "final": "final",
    "char": "char",
    "native": "native",
    "throws": "t_throws",
    "finally": "t_finally",
    "class": "class",
    "extends": "extends",
    "else": "else",
    "interface": "interface",
    "try": "try",
    "catch": "catch",
    "short": "short",
    "volatile": "volatile",
    "float": "float",
    "long": "long",
    "if": "if",
    "this": "this",
    "break": "break",
}
tokens_keys = list(reversed(sorted(tokens.keys(),
                                   key=lambda x: len(x))))


#Regexes to identify other tokens in java
tokens_res = {
    r"[a-zA-Z_]([a-zA-Z0-9_])*": "identifier",

    (r"'([^\\\"']|\\b|\\t|\\n|\\f|\\r|\\\'|\\\"|" +
     r"\\\\|\\(([0-7])([0-7])?|([0-3])([0-7])([0-7])))'"): "character_literal",

    (r"\"([^\\\"]|\\b|\\t|\\n|\\f|\\r|\\\'|\\\"|" +
     r"\\\\|\\(([0-7])([0-7])?|([0-3])([0-7])([0-7])))*\""): "string_literal",

    "(0(x|X)([0-9a-fA-F])+)(l|L)?": "hex_integer_literal",

    "(([0-9])+\\.([0-9])*((e|E) ([+]|[-])?([0-9])+)?(f|F|d|D)?)|(\\.([0-9])+"
    + "((e|E) ([+]|[-])?([0-9])+)?(f|F|d|D)?)|(([0-9])+((e|E) ([+]|[-])?"
    + "([0-9])+)(f|F|d|D)?)|(([0-9])+((e|E) ([+]|[-])?([0-9])+)?(f|F|d|D))":
    "floating_point_literal",

    "(0|([1-9])([0-9])*)(l|L)?": "decimal_integer_literal",
}


def updatePosForToken(value, row, col):
    """Updates the row and column information for a given token by checking
    it for newlines - used for /* comments and blank tokens."""
    while value.find("\n") != -1:
        col = 1
        row += 1
        value = value[value.find("\n") + 1:]
    col += len(value)
    return row, col


def findToken(lex_str, row, col):
    """Uses the hash maps above to identify a token.  Used for non-comment,
    non-blank tokens."""
    longest_match = None
    # Search through keywords/ops for a match
    for key in tokens_keys:
        if lex_str[:len(key)] == key and (not longest_match or
                                          len(longest_match[1])
                                          < len(key)):
            longest_match = (tokens[key], key)

    #Try to find a longer match using regex tokens
    for key in tokens_res.keys():
        match = re.match(key, lex_str)
        if match and (not longest_match or
                      len(longest_match[1]) < len(match.group(0))):
            longest_match = (tokens_res[key], match.group(0))
    return longest_match and Token(longest_match[0], longest_match[1], row,
                                   col)


def lex(lex_str):
    col, row = 1, 1
    token_list = [Token("BOF", "", 0, 0)]
    while len(lex_str):
        if lex_str[:2] == "//":  # Single-line comment
            i = lex_str.find("\n")
            if i != -1:
                lex_str = lex_str[i:]
            else:  # unterminated // comment(should be fine)
                lex_str = ""
        elif lex_str[:2] == "/*":  # Multi-line comment
            i = lex_str.find("*/")
            if i != -1:
                (row, col) = updatePosForToken(lex_str[:i + 2], row, col)
                lex_str = lex_str[i + 2:]
            else:  # unterminated /* comment
                error_if(True, "Syntax error, Unterminated /* comment")
        elif re.match("\s+", lex_str):  # Whitespace: Don't generate a token
            whitespace = lex_str[:len(re.match("\s+", lex_str).group(0))]
            (row, col) = updatePosForToken(whitespace, row, col)
            lex_str = lex_str[len(whitespace):]
        else:
            token = findToken(lex_str, row, col)

            # Error-check tokens to ensure they are valid
            error_if(token is None, "Invalid token at line %i: %s"
            % (row, lex_str[:lex_str.find('\n')]))

            error_if(token.type in disallowed_tokens,
                  "Invalid token type %s at line %i: %s"
                  % (token.type, row, token.value))

            value = token.value
            if token.type == "decimal_integer_literal" and (
            re.match(".*[Ll]", token.value) or int(value) > 2 ** 31):
                error_if(True,
                      "decimal_integer_literal too large at line %i: %s" %
                      (row, token.value))
            token_list += [token]
            col += len(token.value)
            lex_str = lex_str[len(token.value):]
    return token_list + [Token("EOF", "", 0, 0)]


def lex_file(filename):
    return lex(open(filename).read())


### Code for testing and calling only the lexer
def check(stream):
    try:
        lex(stream.read())
        return 0
    except JoosSyntaxException:
        return 42

if __name__ == '__main__':
    sys.exit(check(open(sys.argv[1])))
