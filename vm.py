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

"""Virtual machine starting with block of generated code and ending with a value.

An iteration of the code block and call to each instruction, passing
a push/pop value stack.
"""

import ansar.connect as ar
from job_if import *
from codegen_if import *
from vm_if import *

#
#
def execute(self, code, client):
	stack = []
	self.console('Virtual machine start')
	for c in code:
		if self.halted:
			return ar.Aborted()
		c(stack)
		t = ', '.join(['{value}'.format(value=v) for v in stack])
		self.console('{code:8} [{values}]'.format(code=c.__art__.name, values=t))
	self.console('Virtual machine end ({value})'.format(value=stack[-1]))
	self.send(MachineValue(stack[-1]), client)

ar.bind(execute)

#
#
def vm(self):
	ar.publish(self, VM_SERVICE)
	m = self.select(ar.Published, ar.NotPublished, ar.Stop)
	if isinstance(m, ar.NotPublished):
		return m
	elif isinstance(m, ar.Stop):
		return ar.Aborted()

	while True:
		m = self.select(ar.Delivered, VirtualMachine, ar.Cleared, ar.Dropped, ar.Stop)
		if isinstance(m, ar.Delivered):
			continue
		elif isinstance(m, (ar.Cleared, ar.Dropped)):
			continue
		elif isinstance(m, ar.Stop):
			return ar.Aborted()

		self.create(execute, m.code, self.return_address)

ar.bind(vm)

#
#
if __name__ == '__main__':
	ar.create_node(vm)
