NODE_COLORS = {
    # Module Level
    'Module': 'lightblue',
    'Interactive': 'lightblue',
    'Expression': 'lightblue',
    'FunctionType': 'lightblue',
    # Statements
    'FunctionDef': '#90ee90',
    'AsyncFunctionDef': '#90ee90',
    'ClassDef': '#90ee90',
    'Return': '#90ee90',
    'Delete': '#90ee90',
    'Assign': '#90ee90',
    'AugAssign': '#90ee90',
    'AnnAssign': '#90ee90',
    'For': '#90ee90',
    'AsyncFor': '#90ee90',
    'While': '#90ee90',
    'If': '#90ee90',
    'With': '#90ee90',
    'AsyncWith': '#90ee90',
    'Match': '#90ee90',
    'Raise': '#90ee90',
    'Try': '#90ee90',
    'TryStar': '#90ee90',
    'Assert': '#90ee90',
    'Import': '#90ee90',
    'ImportFrom': '#90ee90',
    'Global': '#90ee90',
    'Nonlocal': '#90ee90',
    'Expr': '#90ee90',
    'Pass': '#90ee90',
    'Break': '#90ee90',
    'Continue': '#90ee90',
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
    'List': 'lightgrey',
    'Tuple': 'lightgrey',
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
    'If': '#90ee90',
    'For': '#90ee90',
    'While': '#90ee90',
    'Try': '#90ee90',
    'With': '#90ee90',
    'Match': '#90ee90',
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

LEGEND = [
    ("Module Level", 'Module'),
    ("Statement", 'FunctionDef'),
    ("Expression", 'BinOp'),
    ("Name/Constant", 'Name'),
    ("<B>Operator</B><BR/>(arithmetic,<BR/>bitwise,<BR/>comparison,<BR/>boolean,<BR/>unary)", 'Add'),
    ("<B>Container/Context</B><BR/>(lists,<BR/>dicts,<BR/>sets,<BR/>tuples,<BR/>Load/Store/Del)", 'List'),
]

_missing_node_types = set()

def get_node_color(node_type):
    if node_type not in NODE_COLORS:
        if node_type not in _missing_node_types:
            print(f"[viz_config] Missing color for node type: {node_type}")
            _missing_node_types.add(node_type)
    return NODE_COLORS.get(node_type, "white") 