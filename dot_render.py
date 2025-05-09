from graphviz import Digraph
from viz_config import NODE_COLORS, LEGEND

def generate_dot(ast_dict, name='ast', graph_attrs=None, node_attrs=None, edge_attrs=None) -> Digraph:
    """
    Convert AST dictionary to Graphviz DOT using HTML-like labels.
    - Skips container nodes with only one non-empty child list.
    - Uses dashed style for true containers with >1 non-empty child list.
    - Line numbers are shown in smaller font under the main label.
    - Adds a color legend at the bottom of the graph.
    """
    dot = Digraph(name=name, format='png')
    dot.attr('node', **(node_attrs or {'shape': 'box', 'fontname': 'Consolas', 'margin': '0.1,0.05'}))
    dot.attr('graph', **(graph_attrs or {'rankdir': 'TB', 'ranksep': '0.75'}))
    dot.attr('edge', **(edge_attrs or {'fontname': 'Consolas', 'fontsize': '10'}))
    node_counter = [0]
    CONTAINER_FIELDS = {'body', 'args', 'arguments', 'keywords', 'bases', 'decorator_list', 'orelse', 'targets', 'values', 'elts', 'items'}
    def get_unique_id():
        node_counter[0] += 1
        return f"node_{node_counter[0]}"
    def get_node_color(node_type: str) -> str:
        return NODE_COLORS.get(node_type, 'white')
    def format_label(node):
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
        if is_true_container and len(non_empty_lists) == 1 and len(node) <= 3:
            field, filtered = non_empty_lists[0]
            if len(filtered) == 1:
                return add_nodes(filtered[0], parent_id)
        node_id = get_unique_id()
        label = format_label(node)
        color = get_node_color(node['type'])
        style = 'filled'
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
    add_legend(dot, LEGEND, get_node_color)
    return dot

def add_legend(dot: Digraph, legend_data, get_color_func) -> None:
    anchor_id = 'legend_anchor'
    dot.node(anchor_id, label='', shape='point', width='0.01', height='0.01', style='invis')
    with dot.subgraph(name='cluster_legend') as legend:
        legend.attr(label='Legend', fontsize='16', fontname='Consolas', style='dashed')
        legend.attr('node', shape='box', width='1', height='0.3', style='filled', fontname='Consolas')
        for label, node_type in legend_data:
            color = get_color_func(node_type)
            legend.node(f'legend_{node_type}', label=f"<{label}>", fillcolor=color)
        legend.attr(rank='same')
        for i in range(len(legend_data) - 1):
            legend.edge(f'legend_{legend_data[i][1]}', f'legend_{legend_data[i+1][1]}', style='invis')
    dot.attr(rank='same')
    dot.edge(anchor_id, f'legend_{legend_data[0][1]}', style='invis', constraint='false') 