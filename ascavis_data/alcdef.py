"""
ALCDEF light curve parsing

Format specification: http://www.minorplanetcenter.net/light_curve2/docs/ALCDEF_Standard.pdf

"""

from collections import namedtuple
from parcon import *

DataEntry = namedtuple("DataEntry",
    ["julian_date", "magnitude", "magnitude_error", "airmass"])
Observation = namedtuple("Observation", ["meta", "lightcurve"])

line_break = Exact(First("\r\n", "\n"))
upper_string = Translate(Upper()[...], "".join)
key = Translate((Upper() | Digit())[...], "".join)
any_string = Exact((AnyChar() - line_break)[...]["".join])

def key_value_pair(key, value):
    return key + "=" + value

def convert_data_entry(array):
    assert 2 <= len(array) <= 4
    julian_date = array[0]
    magnitude = array[1]
    magnitude_error = None
    if len(array) > 2:
        magnitude_error = array[2]
    airmass = None
    if len(array) > 3:
        airmass = array[3]
    return DataEntry(julian_date, magnitude, magnitude_error, airmass)

data_entry = separated(number[float], Literal("|"))[convert_data_entry]
data_block = Exact(separated(key_value_pair("DATA", data_entry), line_break))

meta_data = Exact(separated(key_value_pair(key, any_string), line_break))[dict]

observation = (
        "STARTMETADATA" + meta_data +
        "ENDMETADATA" + data_block +
        "ENDDATA"
    )[lambda x: Observation(*x)]
alcdef = observation[...]
