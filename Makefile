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

# Generate useful lists of build artefacts.
EXECUTABLES := job-batch parse codegen vm ansar-group
BUILD := $(EXECUTABLES:%=dist/%)
SPEC := $(EXECUTABLES:%=%.spec)

# The default target is the development loop.
all: test

# Turn a python script into an executable.
dist/% : %.py
	pyinstaller --onefile --hidden-import=_cffi_backend --log-level ERROR -p . $<

# Specific rules for library scripts.
dist/ansar-group:
	pyinstaller --onefile --hidden-import=_cffi_backend --log-level ERROR -p . `which ansar-group`

#
#
build:: $(BUILD)

clean-build::
	-rm -rf build dist *.spec

#
#
ANSAR=.ansar-home

$(ANSAR): build
	ansar create
	ansar deploy dist

home: $(ANSAR)

#
#
job-batch: home
	ansar add job-batch job-batch
	ansar add parse parse
	ansar add codegen codegen
	ansar add vm vm

run:
	ansar --debug-level=DEBUG run --main-role=job-batch

clean:: clean-build
	-ansar -f destroy

#
#
expression-library: home
	ansar add parse parse
	ansar add codegen codegen
	ansar add vm vm
	ansar network --connect-scope=GROUP --to-scope=HOST
	ansar network

start-library:
	ansar start
