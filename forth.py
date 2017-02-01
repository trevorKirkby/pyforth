from __future__ import print_function  #Lambda compatible print function.

def Float(s):  #Turns a string into a number if applicable.
	try: 
		if str(int(s)) == s:
			return True, int(s)
		else:
			return True, float(s)
	except ValueError:
		return False, s

stack = []

def swap():
	stack[-1], stack[-2] = stack[-2], stack[-1]

def rot():
	stack[-1], stack[-2], stack[-3] = stack[-2], stack[-3], stack[-1]

functions = {
			"." :    lambda: print(stack.pop()),
			".s":    lambda: print(" ".join([str(item) for item in stack])),
			"+":     lambda: stack.append(stack.pop()+stack.pop()),
			"-":     lambda: stack.append(stack.pop()-stack.pop()),
			"*":     lambda: stack.append(stack.pop()*stack.pop()),
			"/":     lambda: stack.append(stack.pop()/stack.pop()),
			"mod":   lambda: stack.append(stack.pop()%stack.pop()),
			"dup":   lambda: stack.append(stack[-1]),
			"swap":  swap,
			"rot":   rot,
			"drop":  lambda: stack.pop(),
			"nip":   lambda: stack.pop(-2),
			"tuck":  "swap over",
			"over":  lambda: stack.append(stack[-2]),
			"roll":  lambda: stack.append(stack.pop(-stack.pop())),
			"pick":  lambda: stack.append(stack[-stack.pop()])
			}

def run_line(line):
	if line == "": return
	if line == "quit": raise SystemExit
	function = 0
	function_name = ""
	words = line.split(" ")
	for word in words:
		if word == "\\": break
		if word == "": continue
		result = Float(word)
		if word == ":":
			if function:
				raise SyntaxError('":" is not applicable when the interpreter is already inside a : and ; block')
			function = 1
		elif word == ";":
			if function == 2:
				function_name = ""
				function = 0
			elif function == 1:
				raise SyntaxError('";" is not applicable when the interpreter is inside of a : and ; block that has not yet been named')
			else:
				raise SyntaxError('";" is not applicable when the interpreter is not inside of a : and ; block')
		elif function == 1:
			if result[0]: raise SyntaxError("A new function must be identified by a name, not a number")
			function_name = word
			functions[function_name] = ""
			function = 2
		elif function == 2:
			functions[function_name] += (" "+word)
		elif result[0]:
			stack.append(result[1])
		else:
			if word in functions.keys():
				func = functions[word]
				if type(func) == str:
					run_line(func)
				else:
					func()
			else:
				raise SyntaxError('"{}" is not recognized by the interpreter'.format(word))

if __name__ == "__main__":
	while True:
		try:
			run_line(raw_input(">>> "))
		except Exception, e:
			print(e)
		except KeyboardInterrupt:
			print("\nKeyboardInterrupt")