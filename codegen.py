# Author: Scott Woods <scott.18.ansar@gmail.com.com>
# MIT License
#
# Copyright (c) 2022
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
""".

.
"""
import ansar.connect as ar
from job_if import *
from parse_if import *
from codegen_if import *

#
#
def walk(ast):
	if isinstance(ast, BinaryOperator):
		yield from walk(ast.left_operand)
		yield from walk(ast.right_operand)
		if ast.operator == OP.ADD:
			yield Add()
		elif ast.operator == OP.SUB:
			yield Sub()
		elif ast.operator == OP.MUL:
			yield Mul()
		elif ast.operator == OP.DIV:
			yield Div()
		else:
			pass
	elif isinstance(ast, UnaryOperator):
		yield from walk(ast.operand)
		yield Negate()
	elif isinstance(ast, Operand):
		yield Push(ast.value)
	else:
		pass

#
#
def generate(self, ast, client):
	code = []
	self.console('Instruction block begin')
	for i, c in enumerate(walk(ast)):
		if self.halted:
			return ar.Aborted()
		self.console('[{i:04}] {code}'.format(i=i, code=c.__art__.name))
		code.append(c)
	self.console('Instruction block end')
	self.send(VirtualMachine(code), client)

ar.bind(generate)

#
#
def codegen(self):
	ar.publish(self, CODEGEN_SERVICE)
	m = self.select(ar.Published, ar.NotPublished, ar.Stop)
	if isinstance(m, ar.NotPublished):
		return m
	elif isinstance(m, ar.Stop):
		return ar.Aborted()

	while True:
		m = self.select(ar.Delivered, AbstractSyntaxTree, ar.Cleared, ar.Dropped, ar.Stop)
		if isinstance(m, ar.Delivered):
			continue
		elif isinstance(m, (ar.Cleared, ar.Dropped)):
			continue
		elif isinstance(m, ar.Stop):
			return ar.Aborted()

		self.create(generate, m.ast, self.return_address)

ar.bind(codegen)

if __name__ == '__main__':
	ar.create_node(codegen)
