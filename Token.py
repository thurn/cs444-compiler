#!/usr/bin/env python2.6
"""
Her hair was long, her limbs were white,
And fair she was and free;
And in the wind she went as light
As leaf of linden-tree.

Beside the falls of Nimrodel,
By water clear and cool,
Her voice as falling silver fell
Into the shining pool.
"""


class Token(object):
    """Token output by the lexer."""

    def __init__(self, type, value, row, col):
        self.type = type
        self.value = value
        self.row = row
        self.col = col

    def __repr__(self):
        return "T:" + self.type + ":" + self.value + ":" + str(self.row)

    def __str__(self):
        return "T:" + self.type + ":" + self.value + ":" + str(self.row)
