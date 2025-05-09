import ast
from typing import Any, Dict

class ASTNodeHandler:
    """
    Handler class for AST node processing.
    Provides static methods to extract relevant fields from AST nodes.
    """
    @staticmethod
    def get_node_attributes(node: ast.AST) -> Dict[str, Any]:
        """Get common attributes for all AST nodes."""
        return {
            "type": type(node).__name__,
            "lineno": getattr(node, 'lineno', None),
            "col_offset": getattr(node, 'col_offset', None),
            "end_lineno": getattr(node, 'end_lineno', None),
            "end_col_offset": getattr(node, 'end_col_offset', None)
        }
    @staticmethod
    def handle_constant(node: ast.Constant) -> Dict[str, Any]:
        """Handle Constant nodes."""
        return {
            **ASTNodeHandler.get_node_attributes(node),
            "value": node.value,
            "kind": type(node.value).__name__
        }
    @staticmethod
    def handle_name(node: ast.Name) -> Dict[str, Any]:
        """Handle Name nodes."""
        return {
            **ASTNodeHandler.get_node_attributes(node),
            "id": node.id,
            "ctx": node.ctx.__class__.__name__
        }
    @staticmethod
    def handle_binop(node: ast.BinOp) -> Dict[str, Any]:
        """Handle BinOp nodes."""
        return {
            **ASTNodeHandler.get_node_attributes(node),
            "op": node.op.__class__.__name__
        }
    @staticmethod
    def handle_joinedstr(node: ast.JoinedStr) -> Dict[str, Any]:
        """Handle JoinedStr nodes."""
        return {
            **ASTNodeHandler.get_node_attributes(node),
            "values": [ast_to_dict(value) for value in node.values]
        }
    @staticmethod
    def handle_formattedvalue(node: ast.FormattedValue) -> Dict[str, Any]:
        """Handle FormattedValue nodes."""
        return {
            **ASTNodeHandler.get_node_attributes(node),
            "value": ast_to_dict(node.value),
            "conversion": node.conversion,
            "format_spec": ast_to_dict(node.format_spec) if node.format_spec else None
        }
    @staticmethod
    def handle_unaryop(node: ast.UnaryOp) -> Dict[str, Any]:
        """Handle UnaryOp nodes."""
        return {
            **ASTNodeHandler.get_node_attributes(node),
            "op": node.op.__class__.__name__
        }
    @staticmethod
    def handle_compare(node: ast.Compare) -> Dict[str, Any]:
        """Handle Compare nodes."""
        return {
            **ASTNodeHandler.get_node_attributes(node),
            "ops": [op.__class__.__name__ for op in node.ops]
        }
    @staticmethod
    def handle_attribute(node: ast.Attribute) -> Dict[str, Any]:
        """Handle Attribute nodes."""
        return {
            **ASTNodeHandler.get_node_attributes(node),
            "attr": node.attr,
            "ctx": node.ctx.__class__.__name__
        }
    @staticmethod
    def handle_function_def(node: ast.FunctionDef) -> Dict[str, Any]:
        """Handle FunctionDef nodes."""
        return {
            **ASTNodeHandler.get_node_attributes(node),
            "name": node.name
        }
    @staticmethod
    def handle_class_def(node: ast.ClassDef) -> Dict[str, Any]:
        """Handle ClassDef nodes."""
        return {
            **ASTNodeHandler.get_node_attributes(node),
            "name": node.name
        }
    @staticmethod
    def handle_arg(node: ast.arg) -> Dict[str, Any]:
        """Handle arg nodes."""
        return {
            **ASTNodeHandler.get_node_attributes(node),
            "arg": node.arg
        }

def ast_to_dict(node) -> dict:
    """
    Recursively convert AST nodes to dictionaries.
    - Identifiers (name, id, arg) are left as strings.
    - Primitives are left as-is.
    - AST nodes are converted to dicts.
    """
    if not isinstance(node, ast.AST):
        return node  # Just return the value as-is (string, int, etc.)
    handler_name = f"handle_{type(node).__name__.lower()}"
    handler = getattr(ASTNodeHandler, handler_name, None)
    if handler:
        node_dict = handler(node)
    else:
        node_dict = ASTNodeHandler.get_node_attributes(node)
    for field, value in ast.iter_fields(node):
        if field in ['lineno', 'col_offset', 'end_lineno', 'end_col_offset']:
            continue
        if value is None:
            continue
        # For identifier fields, keep as string
        if field in ['name', 'id', 'arg']:
            node_dict[field] = value
            continue
        if isinstance(value, list):
            node_dict[field] = [ast_to_dict(v) for v in value]
        else:
            node_dict[field] = ast_to_dict(value)
    return node_dict 