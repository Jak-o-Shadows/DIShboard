
import django.utils.http

####################### DIS Filter ###############################
"""Parse and serialize the URL representation of a DIS filter tree.

The URL format is a depth-first token stream. Group nodes declare how many
following nodes belong to them, while fieldset nodes represent leaf data.
"""

def _parse_node(nodes, loc):
    """Parse one node and its declared descendants from a token stream.

    Args:
        nodes: Tokenized filter nodes containing ``type`` and ``data``.
        loc: Index of the node to parse.

    Returns:
        The parsed node and the index of its last consumed token.

    Raises:
        ValueError: If a node declares more children than remain in the stream.
    """
    # @Recursive descent parser for DIS filter tree, SPEC_FILTER_DEPTH_FIRST_PARSING, code_impl
    current_node = nodes[loc]

    num_children = int(current_node["data"].get("c", 0))
    if num_children > 0:
        current_node["children"] = []
        child_nodes = range(loc + 1, loc + 1 + num_children)
        for child_loc in child_nodes:
            if child_loc >= len(nodes):
                raise ValueError(f"Expected {num_children} children for node at index {loc}, but only found {len(nodes) - loc - 1} remaining nodes.")
            child_node, loc = _parse_node(nodes, child_loc)
            current_node["children"].append(child_node)
        loc = child_loc

    return current_node, loc


def dis_filter_url_to_schema(url):
    """Convert URL query parameters into a nested DIS filter schema.

    Args:
        url: An iterable of ``(key, value)`` pairs from a filter query string.

    Returns:
        The root group node of the parsed filter schema. Nodes contain a
        ``type`` and ``data`` mapping, and group nodes may contain ``children``.

    Raises:
        ValueError: If the input has no nodes or does not start with a group.
    """

    # First step is to tokenize the URL into nodes.
    nodes = []
    current_node_data = {}
    current_node_type = None
    for key, value in url:
        match key:
            case "type" | "fieldset":
                if current_node_type is not None:
                    # Save the previous node before starting a new one
                    nodes.append({
                        "type": current_node_type,
                        "data": current_node_data,
                    })
                    current_node_data = {}
                current_node_type = value
                #print(f"Starting new node of type: {current_node_type}")
            case _:
                # It's a node data field
                current_node_data[key] = value
    # Save the last
    if current_node_type is not None:
        nodes.append({
            "type": current_node_type,
            "data": current_node_data,
        })

    if not nodes:
        raise ValueError("No nodes found in the URL schema.")

    if nodes[0]["type"] != "group":
        raise ValueError("Root node must be a group.")

    #for node_idx, node in enumerate(nodes):
    #    print(f"{node_idx} : {node}")

    # Step 2: Convert the nodes into the graph
    root, _ = _parse_node(nodes, 0)

    return root

def _stringify_node(node):
    """Serialize a filter node and its descendants into query components.

    Args:
        node: A filter schema node with ``type`` and ``data`` keys.

    Returns:
        A list of ``(key, value)`` pairs in depth-first order.
    """
    # @Recursive serialization of filter nodes, SPEC_FILTER_DIS_PARSER_SERIALIZER, code_impl
    if node["type"] == "group":
        type_str = "type"
    else:
        type_str = "fieldset"
    url_parts = [(type_str, node["type"])]
    url_parts.extend(node["data"].items())

    for child in node.get("children", []):
        url_parts.extend(_stringify_node(child))

    return url_parts

def dis_filter_schema_to_url(schema):
    """Convert a nested DIS filter schema into its URL query string.

    Args:
        schema: The root filter node to serialize.

    Returns:
        A query string beginning with ``?``.
    """
    # @Convert boolean tree to URL string, SPEC_FILTER_DIS_URL_SCHEMA, code_impl
    url_parts = _stringify_node(schema)
    return "?" + django.utils.http.urlencode(url_parts)
