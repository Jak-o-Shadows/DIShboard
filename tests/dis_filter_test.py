import board.logic as logic


if __name__ == "__main__":

    query_str = "   ?type=group&op=AND&c=2 &fieldset=fa&fa_field1=field1_value&fa_field2=field2_value &type=group&op=OR&c=2 &fieldset=fb&fb_field1=field1_value&fb_field2=field2_value & fieldset=fc&fc_field1=field1_value&fc_field2=field2_value"
    query_str = query_str.replace(" ", "")
    print(f"Query string: {query_str}")

    query_keyvals = query_str[1:].split("&")
    query_keyvals = [pair.split("=") for pair in query_keyvals]

    root = logic.dis_filter_url_to_schema(query_keyvals)

    print(root)

    s = logic.dis_filter_schema_to_url(root)
    print(s)

    assert s == query_str, f"Expected {query_str}, but got {s}"