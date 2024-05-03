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

"""Interface for the code generation phase.

.
"""
import ansar.create as ar

__all__ = [
    'Push',
    'Add',
    'Sub',
    'Mul',
    'Div',
    'Negate',
    'VirtualMachine',
]

class Push(object):
    def __init__(self, value=0.0):
        self.value = value

    def __call__(self, stack):
        v = self.value
        stack.append(v)

class Add(object):
    def __call__(self, stack):
        b = stack.pop()
        a = stack.pop()
        v = a + b
        stack.append(v)

class Sub(object):
    def __call__(self, stack):
        b = stack.pop()
        a = stack.pop()
        v = a - b
        stack.append(v)

class Mul(object):
    def __call__(self, stack):
        b = stack.pop()
        a = stack.pop()
        v = a * b
        stack.append(v)

class Div(object):
    def __call__(self, stack):
        b = stack.pop()
        a = stack.pop()
        v = a / b
        stack.append(v)

class Negate(object):
    def __call__(self, stack):
        a = stack.pop()
        v = -a
        stack.append(v)

ar.bind(Push)
ar.bind(Add)
ar.bind(Sub)
ar.bind(Mul)
ar.bind(Div)
ar.bind(Negate)

class VirtualMachine(object):
	def __init__(self, code=None):
		self.code = code or ar.default_vector()

VIRTUAL_MACHINE_SCHEMA = {
	'code': ar.VectorOf(ar.Any()),
}

ar.bind(VirtualMachine, object_schema=VIRTUAL_MACHINE_SCHEMA)
