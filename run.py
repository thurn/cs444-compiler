import sys
import os
import util

RUN = "generate.py"
VERSION = "6.0"

if __name__ == "__main__":
    test_case = sys.argv[1]
    stdlib = util.all_files_in_dir("test_cases/stdlib/" + VERSION + "/")
    if test_case.endswith(".java"):
        args = stdlib + [test_case]
    else:
        afid = util.all_files_in_dir(test_case)
        if len(afid) == 0:
            print "No files under directory " + test_case
            exit()
        args = stdlib + afid
    os.system("python " + RUN + " " + " ".join(args))
