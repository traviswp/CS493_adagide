from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import Qsci

from MainWindow import Ui_MainWindow
from FileManager import FileManager
from ExecutionManager import ExecutionManager
from BuildManager import BuildManager
from EditorPane import *
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
		self.executionManager = ExecutionManager()
		self.buildManager = BuildManager(self)
		
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
		tabWidget = self.mainWindow.findChild(QtGui.QTabWidget,'tabWidget')
		currFile = tabWidget.currentWidget()
		self.buildManager.build(currFile.file_path, currFile.filename, "-Wall")
		return

	def run(self):
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
		fpath=QtGui.QFileDialog.getOpenFileName(caption='Open file',directory='./')
		newEditorPane=ProjectFile(fpath,fpath)

		tabWidget=self.mainWindow.findChild(QtGui.QTabWidget,'tabWidget')
		tabWidget.addTab(newEditorPane, QtCore.QString(fpath))
		return

	def on_actionBuild(self,checked):
		build();
		return
	
	def on_button_build(self,checked):
		self.build();
		return
	
	def on_actionNew_Project(self,checked):
		return

	def on_actionOpen_Project(self,checked):
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


