"""
ALCDEF light curve parsing

"""

from parcon import *

alcdef_parser = "(" + ZeroOrMore(SignificantLiteral("a") | SignificantLiteral("b")) + ")"
