import pytest

import board.logic as logic

def print_tree(node, level=0):
    """# Pretty print the tree for debug purposes"""
    indent = "  " * level
    print(f"{indent}- {node['type']}: {node['data']}")
    for child in node.get("children", []):
        print_tree(child, level + 1)


def test_dis_filter_url_to_schema_and_back():

    query_str = "   ?type=group&op=AND&c=2 &fieldset=fa&fa_field1=field1_value&fa_field2=field2_value &type=group&op=OR&c=2 &fieldset=fb&fb_field1=field1_value&fb_field2=field2_value & fieldset=fc&fc_field1=field1_value&fc_field2=field2_value"
    query_str = query_str.replace(" ", "")
    print(f"Query string: {query_str}")

    query_keyvals = query_str[1:].split("&")
    query_keyvals = [pair.split("=") for pair in query_keyvals]

    root = logic.dis_filter_url_to_schema(query_keyvals)

    s = logic.dis_filter_schema_to_url(root)

    assert s == query_str, f"Expected {query_str}, but got {s}"

def test_dis_filter_nested_not_operator():
    # Example: NOT(A AND B)
    # This structure needs to be supported according to SPEC_FILTER_DIS_UI_BOOLEAN_OPTIONS
    query_str = "?type=group&op=NOT&c=1&type=group&op=AND&c=2&fieldset=fa&fa_field1=1&fieldset=fb&fb_field1=2"

    query_keyvals = [pair.split("=") for pair in query_str[1:].split("&")]

    root = logic.dis_filter_url_to_schema(query_keyvals)
    s = logic.dis_filter_schema_to_url(root)

    assert s == query_str, f"Expected {query_str}, but got {s}"

def test_dis_filter_deeply_nested():
    # Example: (A OR (B AND (C OR D)))
    query_str = "?type=group&op=OR&c=2&fieldset=fa&fa_f=1&type=group&op=AND&c=2&fieldset=fb&fb_f=2&type=group&op=OR&c=2&fieldset=fc&fc_f=3&fieldset=fd&fd_f=4"

    query_keyvals = [pair.split("=") for pair in query_str[1:].split("&")]

    root = logic.dis_filter_url_to_schema(query_keyvals)
    s = logic.dis_filter_schema_to_url(root)

    assert s == query_str, f"Expected {query_str}, but got {s}"

def test_dis_filter_invalid_child_count_too_few():
    # A group declares 2 children but only provides 1.
    # This should trigger an error (e.g., ValueError or IndexError).
    query_str = "?type=group&op=AND&c=2&fieldset=fa&fa_f=1"

    query_keyvals = [pair.split("=") for pair in query_str[1:].split("&")]

    with pytest.raises(ValueError):
        logic.dis_filter_url_to_schema(query_keyvals)

def test_dis_filter_invalid_child_count_too_many():
    # TODO: This is known to be failing! The logic to catch this is wholly unimplemented
    # A group declares 1 child but provides 2.
    # This should trigger an error because the parser will likely leave dangling tokens.
    query_str = "?type=group&op=AND&c=1&fieldset=fa&fa_f=1&fieldset=fb&fb_f=2"

    query_keyvals = [pair.split("=") for pair in query_str[1:].split("&")]

    with pytest.raises(ValueError):
        logic.dis_filter_url_to_schema(query_keyvals)

def test_dis_filter_malformed_structure():
    # Token stream does not start with a group node.
    query_str = "?fieldset=fa&fa_f=1"

    query_keyvals = [pair.split("=") for pair in query_str[1:].split("&")]

    with pytest.raises(ValueError):
        logic.dis_filter_url_to_schema(query_keyvals)
