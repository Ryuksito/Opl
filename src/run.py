from src.interpreter import Interpreter, global_symbol_table
from src.lexer import Lexer
from src.parser import Parser
from src.models.context import Context

def run(fn, text):
	# Generate tokens
	lexer = Lexer(fn, text)
	tokens, error = lexer.make_tokens()
	if error: return None, error

	# Generate AST
	parser = Parser(tokens)
	ast = parser.parse()
	if ast.error: return None, ast.error

	# Run program
	interpreter = Interpreter()
	context = Context('<program>')
	context.symbol_table = global_symbol_table
	result = interpreter.visit(ast.node, context)

	return result.value, result.error

def run_interpreter():
	while True:
		text = input('opl >> ')
		if text == "EXIT": exit()   
		if text.strip() == "": continue
		result, error = run('<stdin>', text)

		if error:
			print(error.as_string())
		elif result:
			if len(result.elements) == 1:
				print('exit: ', repr(result.elements[0]))
			else:
				print('exit: ', repr(result))
				
def run_interpreter_with_file(file_path):
	text = F'RUN("{file_path}")'
	result, error = run('<stdin>', text)

	if error:
		print(error.as_string())
	elif result:
		if len(result.elements) == 1:
			print('exit: ', repr(result.elements[0]))
		else:
		    print('exit: ', repr(result))