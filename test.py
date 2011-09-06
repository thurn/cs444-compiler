#!/usr/bin/env python2.6
import subprocess
import warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)

import glob
import os
import util
import sys
import random

import lexer
import parse
import environment
import typechecker
import static
import generate

util.Testing.testing = True
random_order = False

all_tests = []


def test(testfn, expected_value, globstr, skip_predicate, test_constructor):
    """Adds compiler tests to the test list.

    Arguments
        testfn: The function to invoke on each test input. Invoked with the
            constructed tests.
        expected_value: The return value you are expecting from testfn.
        globstr: The string you want to pass to glob.glob to locate tests.
        skip_predicate: If this function returns true when passed a path,
            skip that path.
        test_constructor: A function which takes a path from glob and
            converts it into the form testfn expects as input."""
    cases = glob.glob(globstr)
    if random_order:
        random.shuffle(cases)
    for test_case in cases:
        if skip_predicate(test_case):
            continue
        input = test_constructor(test_case)
        all_tests.append([testfn, input, expected_value, test_case])


def run_tests(proc_number, num_procs):
    """Runs the tests in the test list.

    Arguments:
        proc_number: The number of the process currently executing tests
        num_procs: The total number of processes executing tests."""
    count = 0
    for test_quad in all_tests:
        count += 1
        if count % num_procs != proc_number:
            continue
        testfn, input, expected_value, test_case = test_quad
        try:
            result = testfn(input)
            if result == expected_value:
                print ".",
                sys.stdout.flush()
            else:
                print """\n\nTest Case Failed: {case}, expected {expected},
                     got {got}""".format(case=test_case,
                                         expected=expected_value,
                                         got=result)
                exit()
        except util.JoosSyntaxException as jse:
            print "\n\nException in File: " + str(util.CurrentFile.name)
            print jse.msg, "\n\n"
            raise


def noskip(_):
    """Specifies that you do not want to skip any inputs."""
    return False


def no_constructor(input):
    """Specifies that you do not want a test constructor."""
    return input


def lexer_tests():
    test(lexer.check, 0, "test_cases/a1/J[0-9]*.java",
         noskip, open)
    test(lexer.check, 42, "test_cases/a1/Je*.java",
         noskip, open)


def parser_tests():
    def parse_check(filename):
        return parse.check(open(filename), filename)

    test(parse_check, 0, "test_cases/a2/J[0-9]*.java",
         noskip, no_constructor)
    test(parse_check, 42, "test_cases/a2/Je*.java",
         noskip, no_constructor)


def environment_tests():
    stdlib = util.all_files_in_dir("test_cases/stdlib/3.0/")
    test(environment.check, 0, "test_cases/a3/J[0-9]*",
         os.path.isdir, lambda x: [x] + stdlib)
    test(environment.check, 42, "test_cases/a3/Je*",
         os.path.isdir, lambda x: [x] + stdlib)
    test(environment.check, 0, "test_cases/a3/J[0-9]*",
         os.path.isfile, lambda x: util.all_files_in_dir(x) + stdlib)
    test(environment.check, 42, "test_cases/a3/Je*",
         os.path.isfile, lambda x: util.all_files_in_dir(x) + stdlib)


def typechecker_tests():
    stdlib = util.all_files_in_dir("test_cases/stdlib/4.0/")
    test(typechecker.typecheck_files, 0, "test_cases/a4/J[0-9]*",
         os.path.isdir, lambda x: [x] + stdlib)
    test(typechecker.typecheck_files, 0, "test_cases/a4/J[0-9]*",
         os.path.isfile, lambda x: util.all_files_in_dir(x) + stdlib)
    test(typechecker.typecheck_files, 42, "test_cases/a4/Je*",
         os.path.isdir, lambda x: [x] + stdlib)
    test(typechecker.typecheck_files, 42, "test_cases/a4/Je*",
         os.path.isfile, lambda x: util.all_files_in_dir(x) + stdlib)


def static_tests():
    stdlib = util.all_files_in_dir("test_cases/stdlib/5.0/")
    test(static.check, 0, "test_cases/a5/J[0-9]*",
         os.path.isdir, lambda x: [x] + stdlib)
    test(static.check, 42, "test_cases/a5/Je*",
         os.path.isdir, lambda x: [x] + stdlib)
    test(static.check, 0, "test_cases/a5/J[0-9]*",
         os.path.isfile, lambda x: util.all_files_in_dir(x) + stdlib)
    test(static.check, 42, "test_cases/a5/Je*",
         os.path.isfile, lambda x: util.all_files_in_dir(x) + stdlib)


def code_generation_tests():
    stdlib = util.all_files_in_dir("test_cases/stdlib/6.0/")

    def test_asm(filenames):
        environment.cached_environments = {}
        environment.cached_trees = {}
        generate.check_and_generate(filenames)
        subprocess.check_call(["nasm", "-O1", "-f", "elf", "-g", "-F",
                               "dwarf", "output/out.s"])
        subprocess.check_call(["ld", "-melf_i386", "-o", "main",
                               "output/out.o",
                               "test_cases/stdlib/6.0/runtime.o"])
        result = subprocess.call(["./main"])
        os.remove("main")
        os.remove("output/out.s")
        os.remove("output/out.o")
        return result

    test(test_asm, 123, "test_cases/a6/J[0-9]_*.java", os.path.isdir,
         lambda x: [x] + stdlib)
    test(test_asm, 123, "test_cases/a6/J[0-9]_*.java", os.path.isfile,
         lambda x: util.all_files_in_dir(x) + stdlib)
    test(test_asm, 13, "test_cases/a6/J[0-9]e*.java", os.path.isdir,
         lambda x: [x] + stdlib)
    test(test_asm, 13, "test_cases/a6/J[0-9]e*.java", os.path.isfile,
         lambda x: util.all_files_in_dir(x) + stdlib)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print "Use: 'test.py process_num num_procs test_case1 test_case2' etc."
    else:
        proc_num = int(sys.argv[1])
        num_procs = int(sys.argv[2])
        for fn in sys.argv[3:]:
            eval(fn)()
        run_tests(proc_num, num_procs)
