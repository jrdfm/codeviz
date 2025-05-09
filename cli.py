import argparse
from ast_parser import parse_code
from dot_render import generate_dot

def main():
    parser = argparse.ArgumentParser(
        description="Python AST Parser\n\n"
                    "Examples:\n"
                    "  python cli.py example.py\n"
                    "  python cli.py example.py -o output_ast\n\n"
                    "Input: A valid Python file (e.g., example.py).\n"
                    "Output: A Graphviz DOT file or PNG (if -o is specified).",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("file", help="Python file to parse")
    parser.add_argument("-o", "--output", 
                        help="Output file name (without extension)",
                        required=False)
    args = parser.parse_args()

    try:
        with open(args.file) as f:
            code = f.read().strip()
    except FileNotFoundError:
        print(f"Error: The file '{args.file}' does not exist.")
        exit(1)
    except IOError as e:
        print(f"Error: Unable to read the file '{args.file}'. {e}")
        exit(1)

    if not code:
        print("Error: The input file is empty.")
        exit(1)

    ast_dict = parse_code(code)
    if "error" in ast_dict:
        print(f"Error: {ast_dict['error']}")
        exit(1)

    dot = generate_dot(ast_dict)
    if args.output:
        try:
            dot.render(args.output, cleanup=True)
        except Exception as e:
            print(f"Error: Failed to render the output file. {e}")
            exit(1)
    else:
        print(dot.source)

if __name__ == "__main__":
    main() 