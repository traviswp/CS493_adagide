from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import Qsci

from MainWindow import Ui_MainWindow
from FileManager import FileManager
from ExecutionManager import ExecutionManager
from BuildManager import BuildManager
from EditorPane import *
import copy
"""
The Controller is the glue that holds the project together.
	-It is a bridge that connects the User Interface to the backend code.
	-It inherits QtCore.QObject, which has the "connect(UIElement, QtCore.SIGNAL, functionCallback)" method.
	 This lets us register specific UI elements (eg. buttons) with python functions.
"""
class Controller(QtCore.QObject):

	def __init__(self, mainWindow, debugMode=False):
		QtCore.QObject.__init__(self)

		# Prints angry debug messages, if activated
		self.debugMode = debugMode

		# Register mainWindow object
		self.mainWindow = mainWindow

		# Create/initialize other objects
		self.fileManager = FileManager()
		self.executionManager = ExecutionManager(self)
		self.buildManager = BuildManager(self)
		
		# HACK: get the current tab which contains the file to delete
		tabWidget = self.mainWindow.findChild(QtGui.QTabWidget,'tabWidget')
		tabWidget.removeTab(1)

		# Link UI elements to functions
		for item in self.mainWindow.findChildren(QtGui.QAction): # Menubar action elements
			try:
				itemName = str(item.objectName())
				if itemName != "":
					function = self.__getattribute__("on_" + itemName)
					item.triggered.connect(function)
			except AttributeError:
				if(debugMode):
					print "Controller should have a member function called '%s', but doesn't!" %("on_"+itemName)

		for item in self.mainWindow.findChildren(QtGui.QPushButton): # Buttons elements
			try:
				itemName = str(item.objectName())
				if itemName != "":
					function = self.__getattribute__("on_" + itemName)
					item.clicked.connect(function)
			except AttributeError:
				if(debugMode):
					print "Controller should have a member function called '%s', but doesn't!" %("on_"+itemName)

	# Put all basic class functions here
	def build(self):

		# before displaying the new build, clear the output text box
		outputConsole = self.mainWindow.findChild(QtGui.QTextEdit, 'outputTextBox')
		outputConsole.clear()

		# get the current tab which contains the file to be built
		tabWidget = self.mainWindow.findChild(QtGui.QTabWidget,'tabWidget')
		currFile = tabWidget.currentWidget()

		# get the file(s) to be built
		files = currFile.file_path

		# set the name of the executable
		filename = currFile.filename
		length = len(filename)
		if (filename[length-4:length] == ".cpp"):
			executableName = filename[0:length-4]
		else:
			# This should never happen if you are trying to build a valid file...
			# If we get here it means that people are trying to compile non-.cpp
			# files...
			executableName = "SIDE.err"


		# TODO get the compilation arguments 
		compileArgs = ""

		# build with parameters defined above
		self.buildManager.build((files,), executableName, compileArgs)

		return

	def run(self):
		tabWidget = self.mainWindow.findChild(QtGui.QTabWidget,'tabWidget')
		currFile = tabWidget.currentWidget()
		filedir = os.path.dirname(str(currFile.file_path))
		executableName = str(currFile.file_path) + ""
		executableName = executableName.replace(filedir + '/', "")
		executableName = executableName.split('.')[0]
		self.executionManager.run(filedir, "./" + executableName, "")
		return

	def stop(self):
		return

	def displayOutput(self,outBuffer):
		outputConsole = self.mainWindow.findChild(QtGui.QTextEdit, 'outputTextBox')
		outputConsole.append(outBuffer)


	# Put all UI element event handlers here
	def on_actionSave(self,checked):
		tabWidget=self.mainWindow.findChild(QtGui.QTabWidget,'tabWidget')
		current_tab = tabWidget.currentWidget() 
		current_tab.save()
		return

	def on_actionOpen_File(self,checked):
		fullname=QtGui.QFileDialog.getOpenFileName(caption='Open file',directory='./')
		if fullname != "":
			fpath=os.path.dirname(str(fullname))
			fname=str(fullname)+""
			fname=fname.replace(fpath+'/',"")
			newEditorPane=ProjectFile(fname,fullname)

			tabWidget=self.mainWindow.findChild(QtGui.QTabWidget,'tabWidget')

			tabWidget.addTab(newEditorPane, QtCore.QString(newEditorPane.filename))

		# HACK: get the current tab which contains the file to delete
		tabWidget = self.mainWindow.findChild(QtGui.QTabWidget,'tabWidget')
		tabWidget.removeTab(0)

		return

	def on_actionBuild(self,checked):
		self.build();
		return
	
	def on_button_build(self,checked):
		self.build();
		return
	
	def on_actionRun(self,checked):
                self.run();
		return

	def on_button_run(self,checked):
                self.run();
		return

	def on_actionNew_File(self,checked):
		return

	def on_actionSave_All(self,checked):
		return

	def on_actionClose_Project(self,checked):
		return

	def on_actionQuit(self,checked):
		return

	def on_actionUndo(self,checked):
		return

	def on_actionRedo(self,checked):
		return

	def on_actionCut(self,checked):
		return

	def on_actionCopy(self,checked):
		return

	def on_actionPaste(self,checked):
		return

	def on_actionSelect_All(self,checked):
		return

	def on_actionFind_Replace(self,checked):
		return

	def on_action(self,checked):
		return

