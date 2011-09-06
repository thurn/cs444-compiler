test: lexer-test parser-test env-test static-test typechecker-test

dual-test: d-lexer-test d-parser-test d-env-test d-static-test d-typechecker-test

quad-test: q-lexer-test q-parser-test q-env-test q-static-test q-typechecker-test

python = python

lexer-test: clean
	$(python) test.py 0 1 lexer_tests

d-lexer-test: clean
	$(python) test.py 0 2 lexer_tests &
	$(python) test.py 1 2 lexer_tests

q-lexer-test: clean
	$(python) test.py 0 4 lexer_tests &
	$(python) test.py 1 4 lexer_tests &
	$(python) test.py 2 4 lexer_tests &
	$(python) test.py 3 4 lexer_tests

parser-test: clean
	$(python) test.py 0 1 parser_tests

d-parser-test: clean
	$(python) test.py 0 2 parser_tests &
	$(python) test.py 1 2 parser_tests

q-parser-test: clean
	$(python) test.py 0 4 parser_tests &
	$(python) test.py 1 4 parser_tests &
	$(python) test.py 2 4 parser_tests &
	$(python) test.py 3 4 parser_tests

env-test: clean
	$(env-python) test.py 0 1 environment_tests

d-env-test: clean
	$(python) test.py 0 2 environment_tests &
	$(python) test.py 1 2 environment_tests

q-env-test: clean
	$(python) test.py 0 4 environment_tests &
	$(python) test.py 1 4 environment_tests &
	$(python) test.py 2 4 environment_tests &
	$(python) test.py 3 4 environment_tests

static-test: clean
	$(python) test.py 0 1 static_tests

d-static-test: clean
	$(python) test.py 0 2 static_tests &
	$(python) test.py 1 2 static_tests

q-static-test: clean
	$(python) test.py 0 4 static_tests &
	$(python) test.py 1 4 static_tests &
	$(python) test.py 2 4 static_tests &
	$(python) test.py 3 4 static_tests

typechecker-test: clean
	$(python) test.py 0 1 typechecker_tests

d-typechecker-test: clean
	$(python) test.py 0 2 typechecker_tests &
	$(python) test.py 1 2 typechecker_tests

q-typechecker-test: clean
	$(python) test.py 0 4 typechecker_tests &
	$(python) test.py 1 4 typechecker_tests &
	$(python) test.py 2 4 typechecker_tests &
	$(python) test.py 3 4 typechecker_tests

code-generation-test: clean
	$(python) test.py 0 1 code_generation_tests

d-code-generation-test: clean
	$(python) test.py 0 2 code_generation_tests &
	$(python) test.py 1 2 code_generation_tests

q-code-generation-test: clean
	$(python) test.py 0 4 code_generation_tests &
	$(python) test.py 1 4 code_generation_tests &
	$(python) test.py 2 4 code_generation_tests &
	$(python) test.py 3 4 code_generation_tests

lint:
	pychecker --only -m -f --changetypes *.py

pep8:
	pep8 --count *.py

clean:
	@rm -rf *.pyc
	@rm -rf lr1generation/jlalr/*.class
	@rm -rf err.log
	@rm -rf tmp.xml
	@rm -rf output.xml
	@rm -rf tmp
	@rm -rf cache/
	@rm -rf output.o
	@mkdir cache
