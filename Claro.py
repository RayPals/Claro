import sys
from typing import List, Dict, Tuple
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

class ClaroError(Exception):
    """Base error class for Claro interpreter"""
    def __init__(self, message, line_number):
        self.message = message
        self.line_number = line_number
        super().__init__(self.message)

class InvalidStatementError(ClaroError):
    """Error for invalid statements"""
    pass

class MissingArgumentError(ClaroError):
    """Error for missing arguments"""
    pass

def parse_code(code: str) -> List[str]:
    """Parse the code into lines"""
    return [line.strip() for line in code.split('\n') if line.strip()]

def execute_line(line: str, variables: Dict[str, str], line_number: int, output: List[str], context: Dict) -> None:
    """Execute a single line of code"""
    print(f"Executing line {line_number}: {line}")
    words = line.split()
    try:
        stmt_type = StmtType[words[0].upper()]
    except KeyError:
        raise InvalidStatementError(f"Invalid statement type: {words[0]}", line_number)

    if stmt_type == StmtType.PRINT:
        if len(words) < 2:
            raise MissingArgumentError(f"PRINT statement requires an argument", line_number)
        arg = words[1]
        if arg.isdigit():
            output.append(str(int(arg)))
        else:
            output.append(variables.get(arg, arg))

    elif stmt_type == StmtType.VARIABLE:
        if len(words) < 3:
            raise MissingArgumentError("VARIABLE statement requires a name and a value", line_number)
        name = words[1]
        value = ' '.join(words[2:])
        variables[name] = value

    elif stmt_type == StmtType.IF:
        if len(words) < 2:
            raise MissingArgumentError("IF statement requires a condition", line_number)
        condition = ' '.join(words[1:])
        context['if_condition'] = eval(condition, {}, variables)
        context['in_if_block'] = True
        context['if_block_executed'] = False

    elif stmt_type == StmtType.ELSE:
        if not context.get('in_if_block'):
            raise InvalidStatementError("ELSE without IF", line_number)
        context['in_else_block'] = True

    elif stmt_type == StmtType.WHILE:
        if len(words) < 2:
            raise MissingArgumentError("WHILE statement requires a condition", line_number)
        condition = ' '.join(words[1:])
        context['while_condition'] = condition
        context['while_start'] = line_number

    elif stmt_type == StmtType.END:
        if context.get('in_if_block'):
            context['in_if_block'] = False
            context['in_else_block'] = False
        elif context.get('in_else_block'):
            context['in_else_block'] = False
        elif context.get('while_condition'):
            if eval(context['while_condition'], {}, variables):
                context['while_end'] = line_number
            else:
                context.pop('while_condition', None)
                context.pop('while_start', None)
                context.pop('while_end', None)

    elif stmt_type == StmtType.INPUT:
        if len(words) < 2:
            raise MissingArgumentError("INPUT statement requires a variable name", line_number)
        var_name = words[1]
        user_input = input(f"Enter value for {var_name}: ")
        variables[var_name] = user_input

def execute_code(code: List[str]) -> Tuple[Dict[str, str], List[str]]:
    """Execute the given code"""
    variables = {}
    output = []
    context = {}
    i = 0
    while i < len(code):
        try:
            execute_line(code[i], variables, i+1, output, context)
            if 'while_end' in context:
                i = context['while_start'] - 1
                context.pop('while_end', None)
            i += 1
        except ClaroError as e:
            print(f"Error at line {i+1}: {e}")
            break
        except Exception as e:
            print(f"Error at line {i+1}: {e}")
            break
    return variables, output

def execute_file(file_path: str) -> None:
    with open(file_path, 'r') as file:
        code = file.read()
    lines = parse_code(code)
    variables, output = execute_code(lines)
    print("\n".join(output))

def interactive_mode() -> None:
    print("Entering interactive mode (type 'exit' to quit)")
    variables = {}
    output = []
    context = {}
    while True:
        try:
            line = input("> ")
            if line.lower() == 'exit':
                break
            execute_line(line, variables, 0, output, context)
            print("\n".join(output))
            output.clear()
        except ClaroError as e:
            print(f"Error: {e.message}")
        except Exception as e:
            print(f"Error: {e}")

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
    print("Claro Interpreter Version 1.0")

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
