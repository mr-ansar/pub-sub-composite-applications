# Author: Scott Woods <scott.suzuki@gmail.com>
# MIT License
#
# Copyright (c) 2017-2022
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Interface for the parser phase.

.
"""
import ansar.create as ar

__all__ = [
    'Bodmas',
	'OP',
    'BinaryOperator',
    'UnaryOperator',
    'Operand',
    'AbstractSyntaxTree',
]

class Bodmas(object):
	def __init__(self, expression=None):
		self.expression = expression

BODMAS_SCHEMA = {
	'expression': ar.Unicode(),
}

ar.bind(Bodmas, object_schema=BODMAS_SCHEMA)

#
#
OP = ar.Enumeration(ADD=0, SUB=1, MUL=2, DIV=3, NEGATE=4)

class BinaryOperator(object):
	def __init__(self, left_operand=None, right_operand=None, operator=None):
		self.left_operand = left_operand
		self.right_operand = right_operand
		self.operator = operator

BINARY_OPERATOR_SCHEMA = {
	'left_operand': ar.Any(),
	'right_operand': ar.Any(),
	'operator': OP,
}

class UnaryOperator(object):
	def __init__(self, operand=None, operator=None):
		self.operand = operand
		self.operator = operator

UNARY_OPERATOR_SCHEMA = {
	'operand': ar.Any(),
	'operator': OP,
}

class Operand(object):
	def __init__(self, value=0.0):
		self.value = value

OPERAND_SCHEMA = {
	'value': ar.Float8(),
}

ar.bind(BinaryOperator, object_schema=BINARY_OPERATOR_SCHEMA)
ar.bind(UnaryOperator, object_schema=UNARY_OPERATOR_SCHEMA)
ar.bind(Operand, object_schema=OPERAND_SCHEMA)

class AbstractSyntaxTree(object):
	def __init__(self, ast=None):
		self.ast = ast

AST_SCHEMA = {
	'ast': ar.Any(),
}

ar.bind(AbstractSyntaxTree, object_schema=AST_SCHEMA)
