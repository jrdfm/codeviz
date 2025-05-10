#!/usr/bin/env python
from graphviz import Digraph
from viz_config import NODE_COLORS, LEGEND

def generate_dot(ast_dict, name='ast', graph_attrs=None, node_attrs=None, edge_attrs=None, legend_mode='full') -> Digraph:
    """
    Convert AST dictionary to Graphviz DOT using HTML-like labels.
    - Skips container nodes with only one non-empty child list.
    - Uses dashed style for true containers with >1 non-empty child list.
    - Line numbers are shown in smaller font under the main label.
    - Adds a color legend at the bottom of the graph.
    """
    dot = Digraph(name=name, format='png')
    dot.attr('node', shape='box', fontname='Consolas', margin='0,0.2', fontsize='10', fixedsize='false', width='1')
    dot.attr('graph', **(graph_attrs or {'rankdir': 'TB', 'ranksep': '0.25', 'nodesep': '0.25', 'compound': 'true'}))
    dot.attr('edge', **(edge_attrs or {'fontname': 'Consolas', 'fontsize': '10'}))
    
    node_counter = [0]
    CONTAINER_FIELDS = {'body', 'args', 'arguments', 'keywords', 'bases', 'decorator_list', 'orelse', 'targets', 'values', 'elts', 'items', 'handlers', 'finalbody', 'test', 'iter', 'ifs'}
    # Added more common fields to CONTAINER_FIELDS to ensure they are processed by list logic if needed.

    PRIMARY_CLUSTER_NODE_TYPES = {
        'Module', 'FunctionDef', 'AsyncFunctionDef', 'ClassDef',
        'For', 'AsyncFor', 'While', 'If', 'With', 'AsyncWith',
        'Try', 'TryStar', 'ExceptHandler'
    }

    def get_unique_id():
        node_counter[0] += 1
        return f"node_{node_counter[0]}"

    def get_node_color(node_type: str) -> str:
        return NODE_COLORS.get(node_type, 'white')

    def format_label_for_node(node_dict):
        t = node_dict['type']
        raw_line_text = "" # Store raw line string like "ln#: 1-5"
        if node_dict.get('lineno', ''):
            raw_line_text = f"l#: {node_dict.get('lineno', '')}"
            if node_dict.get('end_lineno') and node_dict.get('end_lineno') != node_dict.get('lineno'):
                raw_line_text += f"-{node_dict.get('end_lineno')}"
        
        main_label_content = "" # This will be built by the type-specific logic below

        if t == 'FunctionDef': main_label_content = f"<B>FunctionDef</B><BR/>name: {node_dict.get('name', '')}"
        elif t == 'AsyncFunctionDef': main_label_content = f"<B>AsyncFunctionDef</B><BR/>name: {node_dict.get('name', '')}"
        elif t == 'ClassDef': main_label_content = f"<B>ClassDef</B><BR/>name: {node_dict.get('name', '')}"
        elif t == 'arg': main_label_content = f"arg: {node_dict.get('arg', '')}"
        elif t == 'Return': main_label_content = f"<B>Return</B>"
        elif t == 'BinOp':
            op = node_dict.get('op', '');
            if isinstance(op, dict) and 'type' in op: op = op['type']
            main_label_content = f"<B>BinOp</B><BR/>op: {op}"
        elif t == 'Name':
            ctx_value = node_dict.get('ctx')
            ctx_type_str = ''
            if isinstance(ctx_value, dict) and 'type' in ctx_value:
                ctx_type_str = ctx_value['type']
            elif isinstance(ctx_value, str) and ctx_value in ['Load', 'Store', 'Del', 'Param']:
                ctx_type_str = ctx_value
            name_id_str = node_dict.get('id', '')
            ctx_suffix_html = ''
            if ctx_type_str == 'Load': ctx_suffix_html = " <FONT POINT-SIZE='8' COLOR='lightskyblue'>[Load]</FONT>"
            elif ctx_type_str == 'Store': ctx_suffix_html = " <FONT POINT-SIZE='8' COLOR='steelblue'>[Store]</FONT>"
            elif ctx_type_str == 'Del': ctx_suffix_html = " <FONT POINT-SIZE='8' COLOR='firebrick'>[Del]</FONT>"
            elif ctx_type_str == 'Param': ctx_suffix_html = " <FONT POINT-SIZE='8' COLOR='darkorange'>[Param]</FONT>"
            main_label_content = f"Name: {name_id_str}{ctx_suffix_html}"
        elif t == 'Constant': main_label_content = f"Constant: {node_dict.get('value', '')}"
        elif t in NODE_COLORS: main_label_content = t 
        else: main_label_content = t

        if raw_line_text: # If there is line number information
            return f"<<TABLE BORDER='0' CELLBORDER='0' CELLSPACING='0' CELLPADDING='0'><TR><TD ALIGN='LEFT'>{main_label_content}</TD></TR><TR><TD ALIGN='LEFT'><FONT POINT-SIZE='7' COLOR='grey60'>{raw_line_text}</FONT></TD></TR></TABLE>>"
        else:
            return f"<{main_label_content}>"

    def format_label_for_cluster(node_dict):
        t = node_dict['type']
        raw_line_text_cluster = ""
        if node_dict.get('lineno', ''):
            raw_line_text_cluster = f"l#: {node_dict.get('lineno', '')}"
            if node_dict.get('end_lineno') and node_dict.get('end_lineno') != node_dict.get('lineno'):
                raw_line_text_cluster += f"-{node_dict.get('end_lineno')}"
        
        main_cluster_label_text = ""
        if t == 'Module': main_cluster_label_text = "Module"
        elif t == 'FunctionDef': main_cluster_label_text = f"FunctionDef: {node_dict.get('name', '')}"
        elif t == 'AsyncFunctionDef': main_cluster_label_text = f"AsyncFunctionDef: {node_dict.get('name', '')}"
        elif t == 'ClassDef': main_cluster_label_text = f"ClassDef: {node_dict.get('name', '')}"
        else: main_cluster_label_text = t # Default cluster label is just the type

        if raw_line_text_cluster:
            return f"<<TABLE BORDER='0' CELLBORDER='0' CELLSPACING='0' CELLPADDING='0'><TR><TD ALIGN='LEFT'>{main_cluster_label_text}</TD></TR><TR><TD ALIGN='LEFT'><FONT POINT-SIZE='7' COLOR='grey60'>{raw_line_text_cluster}</FONT></TD></TR></TABLE>>"
        else:
            return f"<{main_cluster_label_text}>"

    def is_container_field(field):
        return field in CONTAINER_FIELDS

    def add_legend(main_dot_graph: Digraph, legend_data_list, get_color_func_internal, anchor_for_positioning) -> None:
        html_table_rows = []
        for label_text, node_type_legend in legend_data_list:
            color_hex = get_color_func_internal(node_type_legend)
            html_table_rows.append(
                f'<TR><TD WIDTH="15" HEIGHT="15" FIXEDSIZE="TRUE" BGCOLOR="{color_hex}"> </TD> ' \
                f'<TD ALIGN="LEFT"><FONT POINT-SIZE="7">{label_text}</FONT></TD></TR>'
            )
        
        html_table_string = ''
        if html_table_rows:
            html_table_string = '<' + \
                                '<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="1" CELLPADDING="1">' + \
                                ''.join(html_table_rows) + \
                                '</TABLE>' + '>'

        if not html_table_string: return # Don't create legend if table is empty

        legend_cluster_name = 'cluster_html_legend'
        with main_dot_graph.subgraph(name=legend_cluster_name) as legend_cluster:
            legend_cluster.attr(label=html_table_string,
                                labelloc='b', # b=bottom, c=center, t=top
                                labeljust='r', # r=right, c=center, l=left
                                style='invis', # Makes the cluster bounding box invisible
                                group='legend_group' # Try to group it with the anchor
                                )
            # Add a single invisible node inside the cluster to give it an anchor point for its label
            # and for connecting to the main graph anchor.
            internal_legend_node = f'legend_internal_node_{get_unique_id()}' # Requires get_unique_id to be accessible
            legend_cluster.node(internal_legend_node, style='invis', shape='point', width='0.001', height='0.001')
            
            # Connect this cluster's internal node to the overall graph anchor attempt to pull it down
            if anchor_for_positioning:
                main_dot_graph.edge(anchor_for_positioning, internal_legend_node, style='invis', constraint='false') 

    def _add_nodes_recursive(current_digraph_obj, ast_node, parent_id_for_edge=None):
        if not isinstance(ast_node, dict) or 'type' not in ast_node or not isinstance(ast_node['type'], str):
            return None

        node_type = ast_node['type']

        if node_type in PRIMARY_CLUSTER_NODE_TYPES:
            outer_cluster_name = f"cluster_{node_type.lower()}_{get_unique_id()}"
            with current_digraph_obj.subgraph(name=outer_cluster_name) as outer_cluster:
                outer_cluster.attr(label=format_label_for_cluster(ast_node),
                                   style='filled', fillcolor=get_node_color(node_type),
                                   rankdir='TB', ranksep='0.35', nodesep='0.35')
                
                # Process fields within this outer cluster
                for field, value in ast_node.items():
                    if field in ['type', 'lineno', 'col_offset', 'end_lineno', 'end_col_offset', 'ctx']: continue
                    if value is None: continue

                    if field == 'body' and isinstance(value, list): # Special handling for 'body' of primary cluster types
                        filtered_body_items = [v for v in value if v is not None]
                        if filtered_body_items:
                            nested_body_cluster_name = f"cluster_body_{node_type.lower()}_{get_unique_id()}"
                            with outer_cluster.subgraph(name=nested_body_cluster_name) as nested_body_cluster:
                                nested_body_cluster.attr(label='body', style='filled,dashed', fillcolor='#f8f8f8', # Reverted label to 'body'
                                                         rankdir='TB', ranksep='0.25', nodesep='0.25')
                                for item in filtered_body_items:
                                    _add_nodes_recursive(nested_body_cluster, item, None)
                    # Handle other fields (non-'body', or 'body' if not a list like in an empty module)
                    elif isinstance(value, list):
                        filtered_list_items = [v for v in value if v is not None]
                        if filtered_list_items:
                            # Standard list field handling (e.g. args, orelse, targets, decorator_list)
                            # These are added to the outer_cluster.
                            # For single items in a container field, connect directly to parent_id (which is None here, so effectively just adds to cluster)
                            if is_container_field(field) and len(filtered_list_items) == 1:
                                _add_nodes_recursive(outer_cluster, filtered_list_items[0], None) # Add to outer_cluster, no specific parent node needed inside cluster for this item
                            else:
                                # Multi-item list or non-container list: create a field_box within outer_cluster
                                field_box_id = get_unique_id()
                                fb_is_container_look = is_container_field(field) # len > 1 implied or not a container
                                fb_style = 'filled,dashed' if fb_is_container_look else 'filled'
                                fb_color = '#f8f8f8' if fb_is_container_look else 'white'
                                outer_cluster.node(field_box_id, label=f'<{field}>', style=fb_style, fillcolor=fb_color, shape='box')
                                # No edge from cluster boundary to field_box_id needed.
                                for item in filtered_list_items:
                                    _add_nodes_recursive(outer_cluster, item, field_box_id) # Items connect to field_box_id
                    elif isinstance(value, dict) and 'type' in value:
                        # Single child dict (e.g. 'test' of If, 'iter' of For)
                        _add_nodes_recursive(outer_cluster, value, None) # Add to outer_cluster, no specific parent node needed
            return # Primary cluster processing is done

        # ---- For all OTHER node types (NOT in PRIMARY_CLUSTER_NODE_TYPES) ----
        # This is for nodes like Assign, Expr, Name, Constant, BinOp, Call, etc.
        # Also for container-like nodes that are not primary clusters (e.g. an 'arguments' field box)

        # Skip logic for simple non-primary-cluster containers (e.g. an 'args' list with one arg, if 'args' is not a primary cluster type)
        is_true_container_type = node_type not in NODE_COLORS and node_type in CONTAINER_FIELDS
        if is_true_container_type:
            non_empty_child_lists = []
            for field_check, value_check in ast_node.items():
                if field_check in ['type', 'lineno', 'col_offset', 'end_lineno', 'end_col_offset', 'ctx']: continue
                if value_check is None: continue
                if isinstance(value_check, list):
                    filtered_check = [v_chk for v_chk in value_check if v_chk is not None]
                    if filtered_check: non_empty_child_lists.append((field_check, filtered_check))
            
            if len(non_empty_child_lists) == 1 and len(ast_node) <= 3: 
                field_skip, filtered_skip = non_empty_child_lists[0]
                if len(filtered_skip) == 1:
                    return _add_nodes_recursive(current_digraph_obj, filtered_skip[0], parent_id_for_edge)

        # Draw the current ast_node (non-primary-cluster type)
        node_id = get_unique_id()
        _label = format_label_for_node(ast_node) # Use the original detailed label for individual nodes
        _color = get_node_color(node_type)
        _style = 'filled'
        if is_true_container_type: # This node itself is a simple container box (e.g. 'arguments')
             _color = '#f8f8f8' 
             _style = 'filled,dashed'
        current_digraph_obj.node(node_id, label=_label, style=_style, fillcolor=_color, shape='box')

        if parent_id_for_edge:
            current_digraph_obj.edge(parent_id_for_edge, node_id)

        # Process fields for this non-primary-cluster node
        for field, value in ast_node.items():
            if field in ['type', 'lineno', 'col_offset', 'end_lineno', 'end_col_offset', 'ctx']: continue
            if value is None: continue

            if isinstance(value, list):
                filtered_list_items = [v for v in value if v is not None]
                if filtered_list_items:
                    if is_container_field(field) and len(filtered_list_items) == 1:
                         _add_nodes_recursive(current_digraph_obj, filtered_list_items[0], node_id)
                    else:
                        field_box_id = get_unique_id()
                        fb_is_container_look = is_container_field(field)
                        fb_style = 'filled,dashed' if fb_is_container_look else 'filled'
                        fb_color = '#f8f8f8' if fb_is_container_look else 'white'
                        current_digraph_obj.node(field_box_id, label=f'<{field}>', style=fb_style, fillcolor=fb_color, shape='box')
                        current_digraph_obj.edge(node_id, field_box_id)
                        for item in filtered_list_items:
                            _add_nodes_recursive(current_digraph_obj, item, field_box_id)
            elif isinstance(value, dict) and 'type' in value:
                _add_nodes_recursive(current_digraph_obj, value, node_id)
        return node_id

    _add_nodes_recursive(dot, ast_dict, None) # Initial call

    if legend_mode == 'full':
        bottom_anchor_name = f'bottom_anchor_{name}'
        dot.node(bottom_anchor_name, style='invis', height='0.01', width='0.01', label='', group='legend_group')
        add_legend(dot, LEGEND, get_node_color, bottom_anchor_name)
    
    return dot

# The global add_legend function is now REMOVED from here, as its definition is moved inside generate_dot. 