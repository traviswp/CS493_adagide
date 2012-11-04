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

class BuildManager(QtGui.QPlainTextEdit):

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
    def __init__(self, parent=None):

        # initialize text environment
        QtGui.QPlainTextEdit.__init__(self, parent)
        
        # set environment defaults initially
        self.setUndoRedoEnabled(False)
        self.setReadOnly(True)

        # defaults for text environment
        textFont = "monospace"
        textSize = 9
        self.document().setDefaultFont(QtGui.QFont(textFont, textSize, QtGui.QFont.Normal))

        # set compiler
        self.compiler = CompilerLib.ClangCimpiler()

        # initial text environment contents
        self.contents = ""
        self.process = QtCore.QProcess(self)

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
        pass

    #
    # When the process finishes compilation, return the appropriate messages.
    #
    def on_finished(self):
        # parse the results of the compilation
        results = self.compiler.parse_output(self.contents)

        # determine if compilation was successful & return appropriate messages. 
        if self.process.exitCode() == 0:
            self.compile_success.emit(results)
            self.write("[ Compilation Successful ]")  
        else:
            self.compile_fail.emit(results)

    #
    # In the case of stdError, return the appropriate messages
    #
    def on_stderr(self):
        data = self.process.readAllStandardError()
        self.write(data)

    #
    # In the case of an error, return the appropriate messages
    #
    def on_error(self):
        data = "[ The compiler exited with an error: %s ]" % str(self.process.error())
        self.write(data)


    ##################################################################
    #    Edit Text Environment Containing Compilation Message(s)     #
    ##################################################################

    def write(self, data):
        self.contents += str(data
        self.redraw()

    def clear(self):
        self.contents = ""
        self.redraw()

    def redraw(self):
        self.SetReadOnly(False)
        self.setPlainText(self.contents)
        self.setReadOnly(True)

    def build(self, files, executableName, runtimeArgs):
        # TODO: kill old processes...(Question: How do we know which ones are ours to kill?)
        self.clear()

        # pass all files, args, & the executable to the compiler's run method
        # (NOTE: compiler set in CompilationManager initialization)
        self.compiler.build(self.process, files, executableName, runtimeArgs)

