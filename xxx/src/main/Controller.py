from PyQt4 import QtCore
from PyQt4 import QtGui

from MainWindow import Ui_MainWindow
from FileManager import FileManager
from ExecutionManager import ExecutionManager
from BuildManager import BuildManager

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
		self.buildManager = BuildManager()
		
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
	def build():
		return
	def run():
		return
	def stop():
		return

	# Put all UI element event handlers here
	def on_actionSave():
		return
