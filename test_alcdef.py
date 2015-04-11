from alcdef import *


def test_grammar():
    assert alcdef_parser.parse_string("(ababa)") == ['a', 'b', 'a', 'b', 'a']
