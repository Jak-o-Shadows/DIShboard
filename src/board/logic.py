
from pprint import pprint


def _parse_node(nodes, loc):
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
    # @Recursive serialization of filter nodes, SPEC_FILTER_DIS_PARSER_SERIALIZER, code_impl
    if node["type"] == "group":
        type_str = "type"
    else:
        type_str = "fieldset"
    url_parts = [f"{type_str}={node['type']}"]
    for key, value in node["data"].items():
        url_parts.append(f"{key}={value}")

    for child in node.get("children", []):
        url_parts.extend(_stringify_node(child))

    return url_parts

def dis_filter_schema_to_url(schema):
    # @Convert boolean tree to URL string, SPEC_FILTER_DIS_URL_SCHEMA, code_impl
    # TODO: There is boudn to be a safe way of doing this, that properly escapes characters and the like
    url_parts = _stringify_node(schema)
    return "?" + "&".join(url_parts)
