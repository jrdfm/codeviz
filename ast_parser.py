import ast
import json
from typing import Any, Dict, List, Optional, Union
from ast_handlers import ASTNodeHandler, ast_to_dict

def parse_code(code: str) -> dict:
    """
    Parse Python code to an AST dictionary.

    Args:
        code (str): A string containing valid Python code.

    Returns:
        dict: A nested dictionary representation of the AST, or an error message if parsing fails.
    """
    try:
        tree = ast.parse(code)
        return ast_to_dict(tree)
    except SyntaxError as e:
        return {"error": f"SyntaxError: {e}"}

