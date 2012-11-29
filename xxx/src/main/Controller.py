from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import Qsci
import sys
from MainWindow import Ui_MainWindow
from FileManager import FileManager
from ExecutionManager import ExecutionManager
from BuildManager import BuildManager
from EditorPane import *
from DialogManager import *

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
		self.DialogManager = DialogManager(self.mainWindow)
		# Connect signals from FindReplaceDialog to controller methods
		self.DialogManager.findReplaceDialog.find.connect(self.find)
		self.DialogManager.findReplaceDialog.replace.connect(self.replace)
		self.DialogManager.findReplaceDialog.replace_all.connect(self.replace_all)
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
		
		inputTextBox = self.mainWindow.findChild(QtGui.QLineEdit, 'stdinTextBox');
		inputTextBox.returnPressed.connect(self.enter);

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
		outputConsole = self.mainWindow.findChild(QtGui.QTextEdit, 'outputTextBox')
		outputConsole.clear()
		
		# Find run args
		runArgsLine = self.mainWindow.findChild(QtGui.QLineEdit, 'runArgs')
		runArgs = runArgsLine.text()
		runArgsLine.clear()
		
		# Run executable
		tabWidget = self.mainWindow.findChild(QtGui.QTabWidget,'tabWidget')
		currFile = tabWidget.currentWidget()
		filedir = os.path.dirname(str(currFile.file_path))
		executableName = str(currFile.file_path) + ""
		executableName = executableName.replace(filedir + '/', "")
		executableName = executableName.split('.')[0]
		self.executionManager.run(filedir, "./" + executableName, str(runArgs))
		return

	def stop(self):
		self.executionManager.stop()
		return

	def displayOutput(self,outBuffer,HTMLtags=None,HTMLclosingtags=None):
		if HTMLtags != None:
			outputConsole = self.mainWindow.findChild(QtGui.QTextEdit, 'outputTextBox')
			if HTMLclosingtags != None:
				outputConsole.append(HTMLtags + outBuffer + HTMLclosingtags)
			else:
				outputConsole.append(HTMLtags + outBuffer + '</font>')
		else:
			outputConsole = self.mainWindow.findChild(QtGui.QTextEdit, 'outputTextBox')
			outputConsole.append(outBuffer)

	def enter(self):
		if self.executionManager.process.state() == 2: # 0->not running, 1->starting, 2->running
			inputTextBox = self.mainWindow.findChild(QtGui.QLineEdit, 'stdinTextBox')
			inputLine = inputTextBox.text()
			inputTextBox.clear()

			outputConsole = self.mainWindow.findChild(QtGui.QTextEdit, 'outputTextBox')
			self.displayOutput(inputLine,'<font color="blue"><i>','</i></font>')
			#outputConsole.append('<font color="blue"><i>' + inputLine + '</i></font>')

			self.executionManager.writeDataToProcess(str(inputLine) + '\n')




	def on_button_stop(self,checked):
		self.stop()
		return
		
	def on_actionStop(self,checked):
		self.stop()
		return
		
	def on_button_enter(self,checked):
		self.enter();
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
		self.run()
		return
	####################################################################
	# File Controls                                                    #
	####################################################################
	def on_actionNew_File(self,checked):
		if self.fileManager.projectPath != None and self.fileManager.projectPath != "":
			newFileName='ted.h'#open a dialog to get the file name
			if newFileName != "" and newFileName != None:
				for filename in os.listdir(self.fileManager.projectPath):
					if newFileName == filename:
						#A file by that name already exists
						#overwrite reject or prompt
						return	
				fullname=self.fileManager.projectPath+"/"+newFileName
				newEditor=self.openFile(fullname)
				newEditor.save()
		return
		
	#To be changed to Import File	
	def on_actionOpen_File(self,checked):
		if self.fileManager.projectPath != None and self.fileManager.projectPath != "":
			fullname=QtGui.QFileDialog.getOpenFileName(caption='Open file',directory=self.fileManager.projectPath)
			if fullname != "" and fullname != None:
				newEditor=self.openFile(fullname)
				newEditor.setFile(newDirectory=self.fileManager.projectPath,newName=newEditor.filename)
		return
		
	def on_actionSave(self,checked):
		tabWidget=self.mainWindow.findChild(QtGui.QTabWidget,'tabWidget')
		current_tab = tabWidget.currentWidget() 
		current_tab.save()
		return
		
	def on_actionSave_As(self,checked):
		if self.fileManager.projectPath != None and self.fileManager.projectPath != "":
			newFileName='jenny.c'#open a dialog to get the file name
			if newFileName != "" and newFileName != None:
				for filename in os.listdir(self.fileManager.projectPath):
					if newFileName == filename:
						#A file by that name already exists
						#overwrite reject or prompt
						return				
			tabWidget=self.mainWindow.findChild(QtGui.QTabWidget,'tabWidget')
			current_tab = tabWidget.currentWidget() 
			index = tabWidget.indexOf(current_tab)
			newTab=self.openFile(current_tab.file_path)
			newTab.save()
			current_tab.setFile(newDirectory=self.fileManager.projectPath,newName=newFileName)
			tabWidget.setTabText(index,newFileName)
			return
		
	def on_actionSave_All(self,checked):
		for projectFile in self.fileManager.files:
			projectFile.save()
		return	
		
	def on_actionNewProject(self,checked):
		self.on_actionClose_Project(checked)
		dirPath = str(QtGui.QFileDialog.getSaveFileName(parent = self.mainWindow, caption='Create A New Project', directory='./'))
		if(dirPath != ""):
			if os.path.exists(dirPath):
				self.statusMessage.emit("The selected project name already exists. Either choose a different one, or use open to open the existing project.")
				return
			else:
				os.makedirs(dirPath)
			if not os.path.exists(dirPath):
				self.statusMessage.emit("There was an error creating the project. Check permissions.")
				return
			self.fileManager.projectPath = str(dirPath)
		else:
			#maybe give feedback
			pass
		return		
		
	def on_actionOpen_Project(self,checked):
		self.on_actionClose_Project(checked)
		dirPath = str(QtGui.QFileDialog.getExistingDirectory(parent = self.mainWindow, caption='Open An Existing Project', directory='./'))
		if(dirPath != ""):
			self.fileManager.projectPath = dirPath
			for filename in os.listdir(dirPath):
				if fnmatch.fnmatch(filename, '*.c') or fnmatch.fnmatch(filename, '*.h') or fnmatch.fnmatch(filename, '*.cpp') or fnmatch.fnmatch(filename, '*.cxx') or fnmatch.fnmatch(filename, '*.txt'):
					self.openFile(dirPath +'/'+ filename)     
		else:
			#maybe give feedback
			pass
		return	
		
	def on_actionClose_Project(self,checked):
		for projectFile in self.fileManager.files:
			self.closeFile(projectFile)
		self.fileManager.files=[]
		self.fileManager.projectOpen=False
		self.fileManager.projectPath=None
		self.count=0
		return		

	def on_actionQuit(self,checked):
		self.on_actionClose_Project(checked)
		sys.exit(0)
		pass

	def closeFile(self,projectFile):
		#will this need to run on a seperate thread?
		if projectFile.isModified() == True:
			print 'got it!'
			#prompt for save
			#save or do not
		tabWidget=self.mainWindow.findChild(QtGui.QTabWidget,'tabWidget')
		tabWidget.removeTab(tabWidget.indexOf(projectFile));
		return

	def openFile(self,projectFile):
		fpath=os.path.dirname(str(projectFile))
		fname=str(projectFile)+""
		fname=fname.replace(fpath+'/',"")
		newEditorPane=ProjectFile(fname,projectFile)
		self.fileManager.files.append(newEditorPane)
		tabWidget=self.mainWindow.findChild(QtGui.QTabWidget,'tabWidget')
		tabWidget.addTab(newEditorPane, QtCore.QString(newEditorPane.filename))
		return newEditorPane

	########################################################################

	# Undo
	def on_actionUndo(self,checked):
		tabWidget = self.mainWindow.findChild(QtGui.QTabWidget,'tabWidget')
		current_tab = tabWidget.currentWidget() 		
		if current_tab is not None:
			current_tab.undo()

	# Redo
	def on_actionRedo(self,checked):
		tabWidget = self.mainWindow.findChild(QtGui.QTabWidget,'tabWidget')
		current_tab = tabWidget.currentWidget() 		
		if current_tab is not None:
			current_tab.redo()

	# Cut
	def on_actionCut(self,checked):
		tabWidget = self.mainWindow.findChild(QtGui.QTabWidget,'tabWidget')
		current_tab = tabWidget.currentWidget() 		
		if current_tab is not None:
			current_tab.cut()

	# Copy
	def on_actionCopy(self,checked):
		tabWidget = self.mainWindow.findChild(QtGui.QTabWidget,'tabWidget')
		current_tab = tabWidget.currentWidget() 		
		if current_tab is not None:
			current_tab.copy()

	# Paste
	def on_actionPaste(self,checked):
		tabWidget = self.mainWindow.findChild(QtGui.QTabWidget,'tabWidget')
		current_tab = tabWidget.currentWidget() 		
		if current_tab is not None:
			current_tab.paste()

	# Select All
	def on_actionSelect_All(self,checked):
		tabWidget = self.mainWindow.findChild(QtGui.QTabWidget,'tabWidget')
		current_tab = tabWidget.currentWidget() 		
		if current_tab is not None:
			current_tab.selectAll()

	# Find & Replace
	def on_actionFind_Replace(self,checked):
		tabWidget = self.mainWindow.findChild(QtGui.QTabWidget,'tabWidget')
		current_tab = tabWidget.currentWidget() 		
		if current_tab is not None:
			self.DialogManager.findReplaceDialog.open()

	# Replace All
	def replace_all(self, check_states, search_for, replace_with):
		tabWidget = self.mainWindow.findChild(QtGui.QTabWidget,'tabWidget')
		current_tab = tabWidget.currentWidget() 
		if current_tab is not None:

			search_description_tup = (search_for,check_states['match case'],check_states['match entire word'],check_states['wrap around'],check_states['search backward'])

			if current_tab.current_search_selection != search_description_tup:
				self.find(check_states, search_for)

			while current_tab.current_search_selection == search_description_tup:
				current_tab.replace(replace_with)

				selection_start_row, selection_start_col, selection_end_row, selection_end_col = current_tab.getSelection()

				current_tab.setCursorPosition(selection_end_row, selection_end_col)

				self.find(check_states, search_for)

	# Replace
	def replace(self, check_states, search_for, replace_with):
		tabWidget = self.mainWindow.findChild(QtGui.QTabWidget,'tabWidget')
		current_tab = tabWidget.currentWidget()
		if current_tab is not None:

			search_description_tup = (search_for,check_states['match case'],check_states['match entire word'],check_states['wrap around'],check_states['search backward'])

			if current_tab.current_search_selection != search_description_tup:
				self.find(check_states, search_for)

			if current_tab.current_search_selection == search_description_tup:
				current_tab.replace(replace_with)

				selection_start_row, selection_start_col, selection_end_row, selection_end_col = current_tab.getSelection()

				current_tab.setCursorPosition(selection_end_row, selection_end_col)

				self.find(check_states, search_for)

	# Find
	def find(self, check_states, search_for):
		tabWidget = self.mainWindow.findChild(QtGui.QTabWidget,'tabWidget')
		current_tab = tabWidget.currentWidget()
		if current_tab is not None:

			search_description_tup = (search_for,check_states['match case'],check_states['match entire word'],check_states['wrap around'],check_states['search backward'])

			if current_tab.current_search_selection == search_description_tup:
				was_found = current_tab.findNext()
			else:
				was_found = current_tab.findFirst(  search_for,
													False,
													check_states['match case'],
													check_states['match entire word'],
													check_states['wrap around'],
													not check_states['search backward']
												 )

			if was_found:
				#Set a variable indicating the the current selection is the result of a search.
				current_tab.current_search_selection = search_description_tup

	########################################################################

