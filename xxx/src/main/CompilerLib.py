import sys 
import os
import shlex
import re

from PyQt4 import QtCore
from PyQt4 import QtGui

class ClangCompiler():

	"""
	----------------------------------------------------------------------
	This class is designed to provide the ability for the caller to 
	access the clang compiler. This class supports:
	+ compiling 
	+ determing compiler message types
	+ parsing compiler messages
	----------------------------------------------------------------------
	"""

	def build(self, process, files, executableName, compileArgs):

		# default arguments
		executableName = os.path.dirname(str(files[0])) + "/" + executableName
		args = ["-g", "-Wall", "-o", executableName]

		# concatenate default args & the list of files

		# TODO: do we need to include a "customArgs" for runtime args that
		#       a user might supply? (I think yes....)

		#args.extend(runtimeArgs)

		args.extend(files)

		# call the clang compiler with the specified argsf
		process.start(QtCore.QString("clang++"), QtCore.QStringList(args))

	#
	# Determines if a line is a clang error message
	#
	@staticmethod
	def is_error_line(line):
		if len(re.findall(".*:[0-9]+:[0-9]+: error:.*", line)) == 1:
			return True
		return False

	#
	# Determines if a line is a clang warning message
	#
	@staticmethod
	def is_warning_line(line):
		if len(re.findall(".*:[0-9]+:[0-9]+: warning:.*", line)) == 1:
			return True
		return False

	#
	# Parse a clang error/warning message and return a dictionary of information
	# including: the file name, the line and character where the error was 
	# recorded, the error type, and an error message. 
	#
	@staticmethod
	def parse_clang_msg(line):

		# parse the various elements of a clang message
		elements = line.split(":",4)

		# capture the contents of a clang message w/ specific identifiers
		retval = {}
		retval['filename']   = elements[0]
		retval['line_no']    = elements[1]
		retval['char_no']    = elements[2]
		retval['error_type'] = elements[3]
		retval['error_msg']  = elements[4]

		return retval

	#
	# Parse the clang compiler messages, returning a dictionary of the errors.
	# [NOTE: could be empty]
	#
	@staticmethod
	def parse_clang_output(self, output):

		# parse clang output line by line
		lines = output.split("\n")

		# determine all lines of output that are warnings/errors
		sections = []
		for i, line in enumerate(lines):
			if self.is_error_line(line) or self.is_warning_line(line):
				sections.append(i)
		
		# for each warning/error message, get the 'full message' and append
		# this data to a dictionary with other warning/error information. 
		errors = []
		for i, line_pos in enumerate(sections):
			temp = self.parse_clang_msg(lines[line_pos])

			if i + 1 < len(sections):
				temp['full_msg'] = "\n".join(lines[line_pos:sections[i + 1]])
			else:
				temp['full_msg'] = "\n".join(lines[line_pos:])

			errors.append(temp)
			

		return errors
