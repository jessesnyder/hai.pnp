""" Utility methods. It would be great to keep the imports down as
    much as possible.
"""
import re

def camelize(string):
    # If it's a string on non-space characters, don't mess with it
    no_spaces = re.compile('^\w+$')
    if no_spaces.match(string):
        return string
    # first, title case and capitalize the tokens
    caps = string.title()
    # then, collapse them together
    camel = caps.replace(' ', '')
    
    return camel
