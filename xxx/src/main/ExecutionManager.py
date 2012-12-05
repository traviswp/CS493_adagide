import sys 
import os
import shlex
import re

from PyQt4 import QtCore
from PyQt4 import QtGui
from CompilerLib import ClangCompiler

##################################################################
#                           Run Manager                          #
##################################################################

#class ExecutionManager(QtGui.QPlainTextEdit):
class ExecutionManager():

	"""
	----------------------------------------------------------------------
	This class is designed to manage the execution needs of the user. 
	----------------------------------------------------------------------
	"""

	#
	# initialization
	#

	def __init__(self, controller):

		self.running = False
		
		# execution output buffer
		self.buffer = ""

		# controller
		self.controller = controller

		#self.process = QtCore.QProcess(self)
		self.process = QtCore.QProcess()

		# connect custom process handlers
		self.process.started.connect(self.on_started)
		self.process.readyReadStandardOutput.connect(self.on_stdout)
		self.process.error.connect(self.on_error)
		self.process.finished.connect(self.on_finished)

	#
	# custom process handlers
	#

	def on_started(self):
		self.write("[ Program Started ]")

	def on_finished(self):
		self.running = False
		self.write("[ Program Terminated ]")

		# call controller method "compilationOutput" to display buffer contents

	def on_stdout(self):
		data = self.process.readAll()
		self.write(data)

	def on_error(self):
		if(self.running):
			#self.write("An error occurred: %s" % str(self.process.error()))
			self.write('<font color=red>An error occurred: ' + str(self.process.error()) + '</font>')
		else:
			self.write('<font color=red>' + "Stopping program..." + '</font>')

	#
	# buffer manipulation
	#

	def clear(self):
		self.buffer = ""

	def write(self, data):
		self.buffer += str(data)
		self.controller.displayOutput(self.buffer)
		self.clear()


	'''
	def redraw(self)
		self.PlainText(self.buffer + self.line_buffer.text())
		cursor_offset = len(self.line_buffer.text()) - self.line_buffer.cursorPostion()
		self.moveCursor(QtGui.QTextCursor.End)
		for i in range(cursor_offset):
			self.moveCursor(QtGui.QTextCursor.Left, QtGui.QTextCursor.MoveAnchor)

	def commit_buffer(self):
		data = self.line_buffer.text() + "\n"
		self.line_buffer.setText("")
		self.write(data)
		if self.process is not None:
		self.process.writeData(data)

	def keyPressEvent(self, event):
		#TODO: This should allow modifiers and other things of this sort so that users can copy and paste stuff out of the console
		if not self.isReadOnly():
		if event.key() in (QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return):
		self.commit_buffer()
		else:
		self.line_buffer.keyPressEvent(event)
		self.redraw()
	'''

	#
	# Execution
	#

	def run(self, filedir, filename, arg_string):
		self.running = True
		self.clear()
		if os.name != "posix":
			filename=filename.replace("./","\\")
			arg_string=filedir+filename+" "+arg_string
			args = shlex.split(arg_string)
			self.process.start(QtCore.QString("WScript.Shell"), QtCore.QStringList(args))
			#self.writeDataToProcess(arg_string)
		else:
			args = shlex.split(arg_string)
			self.process.setWorkingDirectory(filedir)
			self.process.start(QtCore.QString(filename), QtCore.QStringList(args))
	
	def writeDataToProcess(self, data):
		self.process.writeData(data)
		
	def stop(self):
		self.process.kill()
		self.running = False
		return;

		# TODO kill old processes

