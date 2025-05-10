import sys
from ast_parser import parse_code
from dot_render import generate_dot

def main():
    # Simple Python function as a string
    code = """
def greet(name):
    print(f'Hello, {name}')
"""
    ast_dict = parse_code(code)
    dot = generate_dot(ast_dict)
    print(dot.source)
    # Save to PNG
    dot.render('debug_ast', format='png', cleanup=True)
    print("Saved PNG as debug_ast.png")

if __name__ == "__main__":
    main() 