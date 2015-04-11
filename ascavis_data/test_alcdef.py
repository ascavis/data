import pytest
from alcdef import *


def test_upper_string():
    assert upper_string.parse_string("ABCDEF") == "ABCDEF"

def test_upper_string_fail():
    with pytest.raises(ParseException):
        upper_string.parse_string("abc")

def test_key_value_pair():
    assert (
        key_value_pair(upper_string, upper_string).parse_string("AB=CD")
        == ("AB", "CD")
    )

def test_data_delimiter():
    assert data_entry.parse_string("3.4|2") == DataEntry(3.4, 2.0, None, None)
    assert data_entry.parse_string("3.4|-2") == DataEntry(3.4, -2.0, None, None)
    assert (
        data_entry.parse_string("+5.9|2.3|0.1|1.1") ==
        DataEntry(5.9, 2.3, 0.1, 1.1)
    )


def test_data_block():
    block = """
DATA=3.2|1.1|0.2|1.08
DATA=3.3|1.2|0.1|1.02
    """
    assert (
        data_block.parse_string(block)
        == [
            DataEntry(3.2, 1.1, 0.2, 1.08),
            DataEntry(3.3, 1.2, 0.1, 1.02),
        ]
    )

def test_any_string():
    assert any_string.parse_string("ab") == "ab"
    with pytest.raises(ParseException):
        any_string.parse_string("a\nb")

def test_meta_data():
    block = """
NAME=something
NUMBER=13
TEST=abc def
    """
    assert (
        meta_data.parse_string(block) ==
        {"NAME": "something", "NUMBER": "13", "TEST": "abc def"}
    )

def test_observation():
    block = """
STARTMETADATA
NAME=something
NUMBER=13
ENDMETADATA
DATA=3.2|1.1|0.2|1.08
DATA=3.3|1.2|0.1|1.02
ENDDATA
    """
    assert observation.parse_string(block) == Observation(
        {"NAME": "something", "NUMBER": "13"}, 
        [DataEntry(3.2, 1.1, 0.2, 1.08), DataEntry(3.3, 1.2, 0.1, 1.02)],
    )

def test_example():
    example = open("sample/ALCDEF_905_Universitas_20150407_221242.txt").read()
    parsed = alcdef.parse_string(example)
    # Check some properties of the example file
    assert len(parsed) == 5
    for obs in parsed:
        assert obs.meta["OBJECTNUMBER"] == "905"
        assert obs.meta["OBJECTNAME"] == "Universitas"
