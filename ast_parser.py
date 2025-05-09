import ast
import json
import argparse
from graphviz import Digraph
from typing import Any, Dict, List, Optional, Union
from ast_handlers import ASTNodeHandler, ast_to_dict
from viz_config import NODE_COLORS, LEGEND
from dot_render import generate_dot

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