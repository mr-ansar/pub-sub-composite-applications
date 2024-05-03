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

"""

import ansar.connect as ar
from job_if import *
from parse_if import *
from codegen_if import *
from vm_if import *

# Push a single job through the multiple phases.
class INITIAL: pass
class PARSING: pass
class GENERATING: pass
class RUNNING: pass

class Job(ar.Point, ar.StateMachine):
	def __init__(self, group, line):
		ar.Point.__init__(self)
		ar.StateMachine.__init__(self, INITIAL)
		self.group = group
		self.line = line

def Job_INITIAL_Start(self, message):
	self.send(Bodmas(self.line), self.group.parse)
	return PARSING

def Job_PARSING_AbstractSyntaxTree(self, message):
	self.send(message, self.group.codegen)
	return GENERATING

def Job_PARSING_Stop(self, message):
	self.complete(ar.Aborted())

def Job_GENERATING_VirtualMachine(self, message):
	self.send(message, self.group.vm)
	return RUNNING

def Job_GENERATING_Stop(self, message):
	self.complete(ar.Aborted())

def Job_RUNNING_MachineValue(self, message):
	self.complete(message)

def Job_RUNNING_Stop(self, message):
	self.complete(ar.Aborted())

JOB_DISPATCH = {
    INITIAL: ((ar.Start,), ()),
    PARSING: ((AbstractSyntaxTree, ar.Stop), ()),
    GENERATING: ((VirtualMachine, ar.Stop), ()),
    RUNNING: ((MachineValue, ar.Stop), ()),
}

ar.bind(Job, JOB_DISPATCH)

#
def job_batch(self, group, settings):
	with open(settings.input_batch) as file:
		batch = [j.rstrip() for j in file]

	running = {}
	for i, j in enumerate(batch):
		a = self.create(Job, group, j)
		running[a] = i

	while running:
		m = self.select(ar.Completed, ar.Stop)
		if isinstance(m, ar.Stop):
			return ar.Aborted()

		i = running.pop(self.return_address, None)
		if i is None:
			continue
		if not isinstance(m.value, MachineValue):
			return ar.Faulted(f'job [{i}] returned unexpected value')

		batch[i] = f'{batch[i]} ({m.value.value})'

	with open(settings.output_batch, 'w') as f:
		for j in batch:
			f.write(f'{j}\n')

	return ar.Ack()

ar.bind(job_batch)

# Build the networking relationships.
def main(self, settings):
	group = ar.GroupTable(
		parse=ar.CreateFrame(ar.SubscribeToListing, PARSE_SERVICE),
		codegen=ar.CreateFrame(ar.SubscribeToListing, CODEGEN_SERVICE),
		vm=ar.CreateFrame(ar.SubscribeToListing, VM_SERVICE),
	)
	session = ar.CreateFrame(job_batch, settings)

	group.create(self, session=session, get_ready=5.0)
	m = self.select(ar.Completed)

	return m.value

ar.bind(main)

#
#
class Settings(object):
    def __init__(self, input_batch=None, output_batch=None):
        self.input_batch = input_batch
        self.output_batch = output_batch

SETTINGS_SCHEMA = {
    'input_batch': ar.Unicode(),
    'output_batch': ar.Unicode(),
}

ar.bind(Settings, object_schema=SETTINGS_SCHEMA)

# Initial values.
factory_settings = Settings(input_batch='batch', output_batch='output')

#
#
if __name__ == '__main__':
	ar.create_node(main, factory_settings=factory_settings)
