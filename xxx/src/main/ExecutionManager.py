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

class ExecutionManager(QtGui.QPlainTextEdit):

    """
    ----------------------------------------------------------------------
    This class is designed to manage the execution needs of the user. 
    ----------------------------------------------------------------------
    """
