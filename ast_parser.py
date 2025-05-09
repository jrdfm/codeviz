import ast
import json
import argparse
from graphviz import Digraph
from typing import Any, Dict, List, Optional, Union

# Color scheme for different node types for visualization
NODE_COLORS = {
    # Module Level
    'Module': 'lightblue',
    'Interactive': 'lightblue',
    'Expression': 'lightblue',
    'FunctionType': 'lightblue',
    
    # Statements
    'FunctionDef': 'lightgreen',
    'AsyncFunctionDef': 'lightgreen',
    'ClassDef': 'lightgreen',
    'Return': 'lightgreen',
    'Delete': 'lightgreen',
    'Assign': 'lightgreen',
    'AugAssign': 'lightgreen',
    'AnnAssign': 'lightgreen',
    'For': 'lightgreen',
    'AsyncFor': 'lightgreen',
    'While': 'lightgreen',
    'If': 'lightgreen',
    'With': 'lightgreen',
    'AsyncWith': 'lightgreen',
    'Match': 'lightgreen',
    'Raise': 'lightgreen',
    'Try': 'lightgreen',
    'TryStar': 'lightgreen',
    'Assert': 'lightgreen',
    'Import': 'lightgreen',
    'ImportFrom': 'lightgreen',
    'Global': 'lightgreen',
    'Nonlocal': 'lightgreen',
    'Expr': 'lightgreen',
    'Pass': 'lightgreen',
    'Break': 'lightgreen',
    'Continue': 'lightgreen',
    
    # Expressions
    'BoolOp': 'lightyellow',
    'NamedExpr': 'lightyellow',
    'BinOp': 'lightyellow',
    'UnaryOp': 'lightyellow',
    'Lambda': 'lightyellow',
    'IfExp': 'lightyellow',
    'Dict': 'lightyellow',
    'Set': 'lightyellow',
    'ListComp': 'lightyellow',
    'SetComp': 'lightyellow',
    'DictComp': 'lightyellow',
    'GeneratorExp': 'lightyellow',
    'Await': 'lightyellow',
    'Yield': 'lightyellow',
    'YieldFrom': 'lightyellow',
    'Compare': 'lightyellow',
    'Call': 'lightyellow',
    'FormattedValue': 'lightyellow',
    'JoinedStr': 'lightyellow',
    'Attribute': 'lightyellow',
    'Subscript': 'lightyellow',
    'Starred': 'lightyellow',
    'List': 'lightyellow',
    'Tuple': 'lightyellow',
    'Slice': 'lightyellow',
    
    # Names and Constants
    'Name': 'lightpink',
    'Constant': 'lightpink',
    
    # Operators (arithmetic, bitwise, matrix)
    'Add': 'orange',
    'Sub': 'orange',
    'Mult': 'orange',
    'Div': 'orange',
    'FloorDiv': 'orange',
    'Mod': 'orange',
    'Pow': 'orange',
    'LShift': 'orange',
    'RShift': 'orange',
    'BitOr': 'orange',
    'BitXor': 'orange',
    'BitAnd': 'orange',
    'MatMult': 'orange',
    # Comparison Operators
    'Eq': 'orange',
    'NotEq': 'orange',
    'Lt': 'orange',
    'LtE': 'orange',
    'Gt': 'orange',
    'GtE': 'orange',
    'Is': 'orange',
    'IsNot': 'orange',
    'In': 'orange',
    'NotIn': 'orange',
    # Boolean Operators
    'And': 'orange',
    'Or': 'orange',
    # Unary Operators
    'Invert': 'orange',
    'Not': 'orange',
    'UAdd': 'orange',
    'USub': 'orange',
    # Control Flow
    'If': 'plum',
    'For': 'plum',
    'While': 'plum',
    'Try': 'plum',
    'With': 'plum',
    'Match': 'plum',
    # Containers
    'List': 'lightgrey',
    'Dict': 'lightgrey',
    'Set': 'lightgrey',
    'Tuple': 'lightgrey',
    # Contexts
    'Load': 'lightgrey',
    'Store': 'lightgrey',
    'Del': 'lightgrey',
}

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

def generate_dot(ast_dict, name='ast', graph_attrs=None, node_attrs=None, edge_attrs=None) -> Digraph:
    """
    Convert AST dictionary to Graphviz DOT using HTML-like labels.
    - Skips container nodes with only one non-empty child list.
    - Uses dashed style for true containers with >1 non-empty child list.
    - Line numbers are shown in smaller font under the main label.
    - Adds a color legend at the bottom of the graph.

    Args:
        ast_dict (dict): The AST dictionary to visualize.
        name (str): The name of the Graphviz graph.
        graph_attrs (dict): Attributes for the graph (e.g., rankdir, ranksep).
        node_attrs (dict): Attributes for the nodes (e.g., shape, fontname).
        edge_attrs (dict): Attributes for the edges (e.g., fontname, fontsize).
    """
    dot = Digraph(name=name, format='png')
    dot.attr('node', **(node_attrs or {'shape': 'box', 'fontname': 'Consolas', 'margin': '0.1,0.05'}))
    dot.attr('graph', **(graph_attrs or {'rankdir': 'TB', 'ranksep': '0.75'}))
    dot.attr('edge', **(edge_attrs or {'fontname': 'Consolas', 'fontsize': '10'}))
    
    node_counter = [0]
    CONTAINER_FIELDS = {'body', 'args', 'arguments', 'keywords', 'bases', 'decorator_list', 'orelse', 'targets', 'values', 'elts', 'items'}
    
    LEGEND = [
        ("Module Level", 'Module'),
        ("Statement", 'FunctionDef'),
        ("Expression", 'BinOp'),
        ("Name/Constant", 'Name'),
        ("<B>Operator</B><BR/>(arithmetic,<BR/>bitwise,<BR/>comparison,<BR/>boolean,<BR/>unary)", 'Add'),
        ("Control Flow", 'If'),
        ("<B>Container/Context</B><BR/>(lists,<BR/>dicts,<BR/>sets,<BR/>tuples,<BR/>Load/Store/Del)", 'List'),
    ]
    
    def get_unique_id():
        node_counter[0] += 1
        return f"node_{node_counter[0]}"
    
    def get_node_color(node_type: str) -> str:
        return NODE_COLORS.get(node_type, 'white')
    
    def format_label(node):
        """
        Build an HTML-like label for a node, with line number in smaller font.
        """
        t = node['type']
        line_info = ""
        if node.get('lineno', ''):
            line_str = f"line: {node.get('lineno', '')}"
            if node.get('end_lineno') and node.get('end_lineno') != node.get('lineno'):
                line_str += f"-{node.get('end_lineno')}"
            line_info = f'<BR/><FONT POINT-SIZE="10">{line_str}</FONT>'
        if t == 'FunctionDef':
            label = f"<B>FunctionDef</B><BR/>name: {node.get('name', '')}{line_info}"
        elif t == 'arg':
            label = f"arg: {node.get('arg', '')}{line_info}"
        elif t == 'Return':
            label = f"<B>Return</B>{line_info}"
        elif t == 'BinOp':
            op = node.get('op', '')
            if isinstance(op, dict) and 'type' in op:
                op = op['type']
            label = f"<B>BinOp</B><BR/>op: {op}{line_info}"
        elif t == 'Name':
            ctx = node.get('ctx', '')
            if isinstance(ctx, dict) and 'type' in ctx:
                ctx = ctx['type']
            label = f"Name: {node.get('id', '')}"
            if ctx and ctx != 'Load':
                label += f"<BR/>ctx: {ctx}"
            label += line_info
        elif t == 'Constant':
            label = f"Constant: {node.get('value', '')}{line_info}"
        elif t in NODE_COLORS:
            label = t + line_info
        else:
            label = t + line_info
        return f"<{label}>"
    
    def is_container_field(field):
        return field in CONTAINER_FIELDS
    
    def add_nodes(node, parent_id=None):
        if not isinstance(node, dict) or 'type' not in node or not isinstance(node['type'], str):
            return None
        # For container nodes, count non-empty child lists
        is_true_container = node['type'] not in NODE_COLORS and node['type'] in CONTAINER_FIELDS
        non_empty_lists = []
        for field, value in node.items():
            if field in ['type', 'lineno', 'col_offset', 'end_lineno', 'end_col_offset']:
                continue
            if value is None:
                continue
            if isinstance(value, list):
                filtered = [v for v in value if v is not None]
                if filtered:
                    non_empty_lists.append((field, filtered))
        # If this is a container node with only one non-empty child list, skip it
        if is_true_container and len(non_empty_lists) == 1 and len(node) <= 3:  # type + 1 field + maybe docstring
            field, filtered = non_empty_lists[0]
            if len(filtered) == 1:
                return add_nodes(filtered[0], parent_id)
        node_id = get_unique_id()
        label = format_label(node)
        color = get_node_color(node['type'])
        style = 'filled'
        # Only use dashed for true containers with >1 non-empty child list
        if is_true_container and len(non_empty_lists) > 1:
            color = '#f8f8f8'
            style = 'filled,dashed'
        dot.node(node_id, label=label, style=style, fillcolor=color, shape='box')
        if parent_id:
            dot.edge(parent_id, node_id)
        for field, value in node.items():
            if field in ['type', 'lineno', 'col_offset', 'end_lineno', 'end_col_offset']:
                continue
            if value is None:
                continue
            if isinstance(value, list):
                filtered = [v for v in value if v is not None]
                if filtered:
                    if is_container_field(field) and len(filtered) == 1:
                        add_nodes(filtered[0], node_id)
                    else:
                        subgraph_id = get_unique_id()
                        sub_is_container = is_container_field(field) and len(filtered) > 1
                        sub_style = 'filled,dashed' if sub_is_container else 'filled'
                        sub_color = '#f8f8f8' if sub_is_container else 'white'
                        dot.node(subgraph_id, label=f'<{field}>', style=sub_style, fillcolor=sub_color, shape='box')
                        dot.edge(node_id, subgraph_id)
                        for item in filtered:
                            add_nodes(item, subgraph_id)
            elif isinstance(value, dict) and 'type' in value:
                add_nodes(value, node_id)
        return node_id

    add_nodes(ast_dict)
    # Add a color legend at the top right
    add_legend(dot, LEGEND, get_node_color)
    return dot

def add_legend(dot: Digraph, legend_data: List[tuple], get_color_func) -> None:
    """
    Add a color legend to the Graphviz DOT graph.

    Args:
        dot (Digraph): The Graphviz DOT graph object.
        legend_data (List[tuple]): Legend categories and their representative node types/colors.
        get_color_func (callable): Function to get the color for a node type.
    """
    anchor_id = 'legend_anchor'
    dot.node(anchor_id, label='', shape='point', width='0.01', height='0.01', style='invis')
    with dot.subgraph(name='cluster_legend') as legend:
        legend.attr(label='Legend', fontsize='16', fontname='Consolas', style='dashed')
        legend.attr('node', shape='box', width='1', height='0.3', style='filled', fontname='Consolas')
        for label, node_type in legend_data:
            color = get_color_func(node_type)
            legend.node(f'legend_{node_type}', label=f"<{label}>", fillcolor=color)
        # Arrange legend nodes in a row
        legend.attr(rank='same')
        for i in range(len(legend_data) - 1):
            legend.edge(f'legend_{legend_data[i][1]}', f'legend_{legend_data[i+1][1]}', style='invis')
    # Set rank=same for anchor and first legend node, and connect with invisible edge
    dot.attr(rank='same')
    dot.edge(anchor_id, f'legend_{legend_data[0][1]}', style='invis', constraint='false')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Python AST Parser\n\n"
                    "Examples:\n"
                    "  python ast_parser.py example.py\n"
                    "  python ast_parser.py example.py -o output_ast\n\n"
                    "Input: A valid Python file (e.g., example.py).\n"
                    "Output: A Graphviz DOT file or PNG (if -o is specified).",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("file", help="Python file to parse")
    parser.add_argument("-o", "--output", 
                    help="Output file name (without extension)",
                    required=False)
                    
    args = parser.parse_args()

    with open(args.file) as f:
        code = f.read().strip()
    
    if not code:
        print("Error: The input file is empty.")
        exit(1)
    
    ast_dict = parse_code(code)
    if "error" in ast_dict:
        print(f"Error: {ast_dict['error']}")
        exit(1)
    
    dot = generate_dot(ast_dict)
    if args.output:
        dot.render(args.output, cleanup=True)
    else:
        print(dot.source)