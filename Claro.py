import sys
from typing import List, Dict, Tuple, Any
from enum import Enum
import textwrap

class StmtType(Enum):
    """Statement types"""
    PRINT = 'PRINT'
    VARIABLE = 'VARIABLE'
    IF = 'IF'
    ELSE = 'ELSE'
    WHILE = 'WHILE'
    END = 'END'
    INPUT = 'INPUT'
    FUNC = 'FUNC'
    CALL = 'CALL'
    LIST = 'LIST'
    DICT = 'DICT'
    STRING = 'STRING'
    COMMENT = 'COMMENT'
    TRY = 'TRY'
    EXCEPT = 'EXCEPT'
    FINALLY = 'FINALLY'
    BREAK = 'BREAK'
    CONTINUE = 'CONTINUE'
    FILE = 'FILE'
    FOR = 'FOR'
    IMPORT = 'IMPORT'

class ClaroError(Exception):
    """Base error class for Claro interpreter"""
    def __init__(self, message, line_number):
        self.message = f"Error on line {line_number}: {message}"
        self.line_number = line_number
        super().__init__(self.message)

class InvalidStatementError(ClaroError):
    """Error for invalid statements"""
    pass

class MissingArgumentError(ClaroError):
    """Error for missing arguments"""
    pass

class FunctionDefinitionError(ClaroError):
    """Error for function definitions"""
    pass

functions = {}
break_loop = False
continue_loop = False

def parse_code(code: str) -> List[str]:
    """Parse the code into lines"""
    return [line.strip() for line in code.split('\n') if line.strip() and not line.strip().startswith('#')]

def evaluate_expression(expression: str, variables: Dict[str, Any]) -> Any:
    """Evaluate an expression."""
    try:
        return eval(expression, {}, variables)
    except Exception as e:
        raise ClaroError(f"Error evaluating expression: {expression}", 0)

def parse_function_signature(signature: str) -> Tuple[str, List[str]]:
    parts = signature.split()
    if len(parts) < 2:
        raise FunctionDefinitionError(f"Invalid function signature: {signature}", 0)
    func_name = parts[1]
    params = parts[2:]
    return func_name, params

def execute_line(line: str, variables: Dict[str, Any], line_number: int, output: List[str], lines: List[str]) -> int:
    global break_loop, continue_loop
    print(f"Executing line {line_number}: {line}")
    words = line.split()
    try:
        stmt_type = StmtType[words[0].upper()]
    except KeyError:
        raise InvalidStatementError(f"Invalid statement type: {words[0]}", line_number)

    if stmt_type == StmtType.PRINT:
        if len(words) < 2:
            raise MissingArgumentError(f"PRINT statement requires an argument", line_number)
        arg = ' '.join(words[1:])
        output.append(str(evaluate_expression(arg, variables)))

    elif stmt_type == StmtType.VARIABLE:
        if '=' not in line:
            raise MissingArgumentError("VARIABLE statement requires a name and a value separated by '='", line_number)
        name, value = line.split('=', 1)
        name = name.split()[1].strip()
        value = value.strip()
        variables[name] = evaluate_expression(value, variables)

    elif stmt_type == StmtType.IF:
        if len(words) < 2:
            raise MissingArgumentError("IF statement requires a condition", line_number)
        condition = ' '.join(words[1:])
        if evaluate_expression(condition, variables):
            return line_number
        else:
            return find_corresponding_else_or_end(line_number, lines)

    elif stmt_type == StmtType.WHILE:
        if len(words) < 2:
            raise MissingArgumentError("WHILE statement requires a condition", line_number)
        condition = ' '.join(words[1:])
        start_line = line_number
        while evaluate_expression(condition, variables):
            line_number = execute_block(start_line, lines, variables, output)
            if break_loop:
                break_loop = False
                break
            if continue_loop:
                continue_loop = False

    elif stmt_type == StmtType.INPUT:
        if len(words) < 2:
            raise MissingArgumentError("INPUT statement requires a variable name", line_number)
        var_name = words[1]
        variables[var_name] = input(f"{var_name}: ")

    elif stmt_type == StmtType.FUNC:
        func_name, params = parse_function_signature(' '.join(words))
        functions[func_name] = (params, [])
        i = line_number + 1
        while i < len(lines) and not lines[i].startswith('END'):
            functions[func_name][1].append(lines[i])
            i += 1
        if i >= len(lines) or not lines[i].startswith('END'):
            raise FunctionDefinitionError(f"Function '{func_name}' not properly closed with END", line_number)
        return i

    elif stmt_type == StmtType.CALL:
        if len(words) < 2:
            raise MissingArgumentError("CALL statement requires a function name", line_number)
        func_name = words[1]
        args = [evaluate_expression(arg, variables) for arg in words[2:]]
        if func_name not in functions:
            raise ClaroError(f"Function '{func_name}' not defined", line_number)
        func_params, func_lines = functions[func_name]
        if len(args) != len(func_params):
            raise ClaroError(f"Function '{func_name}' expected {len(func_params)} arguments, got {len(args)}", line_number)
        local_vars = variables.copy()
        local_vars.update(dict(zip(func_params, args)))
        for func_line in func_lines:
            execute_line(func_line, local_vars, line_number, output, func_lines)
        variables.update(local_vars)

    elif stmt_type == StmtType.LIST:
        if len(words) < 3:
            raise MissingArgumentError("LIST statement requires a name and values", line_number)
        name = words[1]
        values = evaluate_expression(' '.join(words[2:]), variables)
        if not isinstance(values, list):
            raise ClaroError(f"LIST statement requires a list of values", line_number)
        variables[name] = values

    elif stmt_type == StmtType.DICT:
        if len(words) < 3:
            raise MissingArgumentError("DICT statement requires a name and key-value pairs", line_number)
        name = words[1]
        pairs = ' '.join(words[2:])
        variables[name] = evaluate_expression(f"{{{pairs}}}", variables)

    elif stmt_type == StmtType.STRING:
        if len(words) < 3:
            raise MissingArgumentError("STRING statement requires a name and a value", line_number)
        name = words[1]
        value = ' '.join(words[2:])
        variables[name] = value

    elif stmt_type == StmtType.FILE:
        if len(words) < 3:
            raise MissingArgumentError("FILE statement requires an operation, file path and optional content", line_number)
        operation = words[1]
        file_path = words[2]
        if operation.upper() == 'READ':
            with open(file_path, 'r') as file:
                content = file.read()
            variables[file_path] = content
        elif operation.upper() == 'WRITE':
            if len(words) < 4:
                raise MissingArgumentError("WRITE operation requires content", line_number)
            content = ' '.join(words[3:])
            with open(file_path, 'w') as file:
                file.write(content)
        else:
            raise ClaroError(f"Invalid file operation: {operation}", line_number)

    elif stmt_type == StmtType.TRY:
        try_block = []
        except_block = []
        finally_block = []
        i = line_number + 1
        while i < len(lines) and not lines[i].startswith('END'):
            if lines[i].startswith('EXCEPT'):
                break
            try_block.append(lines[i])
            i += 1
        while i < len(lines) and not lines[i].startswith('FINALLY') and not lines[i].startswith('END'):
            if not lines[i].startswith('EXCEPT'):
                except_block.append(lines[i])
            i += 1
        while i < len(lines) and not lines[i].startswith('END'):
            if not lines[i].startswith('FINALLY'):
                finally_block.append(lines[i])
            i += 1
        if i >= len(lines) or not lines[i].startswith('END'):
            raise ClaroError("TRY block not properly closed with END", line_number)
        try:
            for try_line in try_block:
                execute_line(try_line, variables, line_number, output, lines)
        except ClaroError as e:
            for except_line in except_block:
                execute_line(except_line, variables, line_number, output, lines)
        finally:
            for finally_line in finally_block:
                execute_line(finally_line, variables, line_number, output, lines)
        return i

    elif stmt_type == StmtType.BREAK:
        break_loop = True
        return len(lines)

    elif stmt_type == StmtType.CONTINUE:
        continue_loop = True
        return len(lines)

    elif stmt_type == StmtType.COMMENT:
        pass  # Do nothing for comments

    elif stmt_type == StmtType.ELSE:
        return find_corresponding_end(line_number, lines)

    elif stmt_type == StmtType.END:
        return line_number

    elif stmt_type == StmtType.FOR:
        if len(words) < 4 or words[2] != 'IN':
            raise MissingArgumentError("FOR loop requires a variable, 'IN', and an iterable", line_number)
        var_name = words[1]
        iterable = evaluate_expression(' '.join(words[3:]), variables)
        if not hasattr(iterable, '__iter__'):
            raise ClaroError(f"'{iterable}' is not iterable", line_number)
        start_line = line_number
        for item in iterable:
            variables[var_name] = item
            line_number = start_line + 1
            while line_number < len(lines):
                if lines[line_number].strip().upper() == 'END':
                    break
                line_number = execute_line(lines[line_number], variables, line_number, output, lines)
                if break_loop:
                    break
                if continue_loop:
                    continue_loop = False
        return find_corresponding_end(start_line, lines)

    elif stmt_type == StmtType.IMPORT:
        if len(words) < 2:
            raise MissingArgumentError("IMPORT statement requires a module name", line_number)
        module_name = words[1]
        try:
            module = __import__(module_name)
            variables[module_name] = module
        except ImportError:
            raise ClaroError(f"Failed to import module: {module_name}", line_number)

    return line_number + 1

def find_corresponding_else_or_end(start_line: int, lines: List[str]) -> int:
    """Find the corresponding ELSE or END statement"""
    nested_if_count = 0
    for i in range(start_line, len(lines)):
        words = lines[i].split()
        if words[0].upper() == 'IF':
            nested_if_count += 1
        elif words[0].upper() == 'END':
            if nested_if_count == 0:
                return i
            nested_if_count -= 1
        elif words[0].upper() == 'ELSE' and nested_if_count == 0:
            return i
    raise ClaroError("No corresponding ELSE or END found", start_line)

def find_corresponding_end(start_line: int, lines: List[str]) -> int:
    """Find the corresponding END statement"""
    nested_count = 0
    for i in range(start_line, len(lines)):
        words = lines[i].split()
        if words[0].upper() in ['IF', 'WHILE', 'FUNC', 'TRY', 'FOR']:
            nested_count += 1
        elif words[0].upper() == 'END':
            if nested_count == 0:
                return i
            nested_count -= 1
    raise ClaroError("No corresponding END found", start_line)

def execute_block(start_line: int, lines: List[str], variables: Dict[str, Any], output: List[str]) -> int:
    """Execute a block of code"""
    line_number = start_line + 1
    while line_number < len(lines):
        line = lines[line_number]
        if line.strip().upper() in ['END', 'ELSE']:
            break
        line_number = execute_line(line, variables, line_number, output, lines)
        if break_loop or continue_loop:
            break
    return line_number

def execute_code_ast(lines: List[str]) -> Tuple[Dict[str, Any], List[str]]:
    """Execute code represented as AST."""
    variables = {}
    output = []
    line_number = 0
    while line_number < len(lines):
        line = lines[line_number]
        try:
            line_number = execute_line(line, variables, line_number, output, lines)
        except ClaroError as e:
            print(e.message)
        except Exception as e:
            print(f"Unexpected error on line {line_number}: {e}")
            break
    return variables, output

def print_executed_code_ast(lines: List[str], variables: Dict[str, Any], output: List[str]) -> None:
    """Print executed code results."""
    print("Executed Code Output:")
    print("\n".join(output))
    print("\nVariables:")
    for name, value in variables.items():
        print(f"{name}: {value}")

def execute_file(file_path: str) -> None:
    with open(file_path, 'r') as file:
        code = file.read()
    lines = parse_code(code)
    variables, output = execute_code_ast(lines)
    print_executed_code_ast(lines, variables, output)

def interactive_mode() -> None:
    print("Entering interactive mode (type 'exit' to quit)")
    variables = {}
    output = []
    while True:
        try:
            line = input("> ")
            if line.lower() == 'exit':
                break
            execute_line(line, variables, 0, output, [])
            print("\n".join(output))
            output.clear()
        except ClaroError as e:
            print(e.message)
        except Exception as e:
            print(f"Unexpected error: {e}")

def print_help() -> None:
    print(textwrap.dedent("""
        Usage: claro.py [options]
        
        Options:
            -e <file>      Execute the code from the specified file
            -i             Enter interactive mode
            -h, --help     Show this help message
            --version      Show version information
    """))

def print_version() -> None:
    print("Claro Interpreter Version 3.0")

def main() -> None:
    if len(sys.argv) == 1:
        print_help()
        sys.exit(0)

    if len(sys.argv) < 2:
        print("Error: Missing command-line arguments")
        print_help()
        sys.exit(1)

    if sys.argv[1] == '-e':
        if len(sys.argv) != 3:
            print_help()
            sys.exit(1)
        execute_file(sys.argv[2])
    elif sys.argv[1] == '-i':
        interactive_mode()
    elif sys.argv[1] == '-h' or sys.argv[1] == '--help':
        print_help()
    elif sys.argv[1] == '--version':
        print_version()
    else:
        print("Error: Invalid option")
        print_help()
        sys.exit(1)

if __name__ == '__main__':
    main()
