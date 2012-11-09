import sys 
import os
import shlex
import re

from PyQt4 import QtCore
from PyQt4 import QtGui
from CompilerLib import ClangCompiler

    ##################################################################
    #                          Build Manager                         #
    ##################################################################

#class BuildManager(QtGui.QPlainTextEdit):
class BuildManager():

    """
    ----------------------------------------------------------------------
    This class is designed to manage the build/compilation needs of the
    user. By utilizing the CompilerLib, the compiler can be configured, 
    but the intention of this class is to utilize the clang complier for 
    the primary purpose of compiling c++ programs. 
    ----------------------------------------------------------------------
    """

    # signals emitted by this widget
    compile_sucess = QtCore.pyqtSignal(list)
    compile_fail   = QtCore.pyqtSignal(list)

    # initialization
    def __init__(self, controller):

        # build (compilation) output buffer
        self.buffer = ""

        # controller
        self.controller = controller

        # initialize text environment
        #QtGui.QPlainTextEdit.__init__(self, parent)
        
        # set environment defaults initially
        #self.setUndoRedoEnabled(False)
        #self.setReadOnly(True)

        # defaults for text environment
        #textFont = "monospace"
        #textSize = 9
        #self.document().setDefaultFont(QtGui.QFont(textFont, textSize, QtGui.QFont.Normal))

        # set compiler
        self.compiler = ClangCompiler()

        # initial text environment contents
        #self.contents = ""
        self.process = QtCore.QProcess()

        # custom handles for process signals
        self.process.started.connect(self.on_started)
        self.process.readyReadStandardError.connect(self.on_stderr)
        self.process.error.connect(self.on_error)
        self.process.finished.connect(self.on_finished)


    ##################################################################
    #         Custom Handles for Process (Compiler) Signals          #
    ##################################################################

    #
    # When the process starts, ...
    #
    def on_started(self):
        self.write("[ Compilation Started ]\n")

    #
    # When the process finishes compilation, return the appropriate messages.
    #
    def on_finished(self):
        # parse the results of the compilation
        results = self.compiler.parse_clang_output(self.compiler, self.buffer)

        # determine if compilation was successful & return appropriate messages. 
        if self.process.exitCode() == 0:
            #self.compile_success.emit(results)
			self.write(results)
            #self.write("[ Compilation Successful ]")
			self.write("[ Compilation Successful ]")
        else:
            #self.compile_fail.emit(results)
			self.write(results)

        # call controller method "compilationOutput" to display buffer contents
        self.controller.displayOutput(self.buffer)

    #
    # In the case of stdError, return the appropriate messages
    #
    def on_stderr(self):
		data = self.process.readAllStandardError()
		self.write(data)
        #self.controller.displayOutput(self.buffer)

    #
    # In the case of an error, return the appropriate messages
    #
    def on_error(self):
        data = "[ The compiler exited with an error: %s ]" % str(self.process.error())
        self.write(data)
        #self.controller.displayOutput(self.buffer)


    ##################################################################
    #    Edit Text Environment Containing Compilation Message(s)     #
    ##################################################################

    def write(self, data):
        self.buffer += str(data)
        #self.contents += str(data)
        #self.redraw()
        #return data

    def clear(self):
        #self.contents = ""
        #self.redraw()
        self.buffer = ""

    #def redraw(self):
    #    self.SetReadOnly(False)
    #    self.setPlainText(self.contents)
    #    self.setReadOnly(True)

    def build(self, files, executableName, compileArgs):
        # TODO: kill old processes...(Question: How do we know which ones are ours to kill?)
        self.clear()

        # pass all files, args, & the executable to the compiler's run method
        # (NOTE: compiler set in CompilationManager initialization)
        self.compiler.build(self.process, files, executableName, compileArgs)

