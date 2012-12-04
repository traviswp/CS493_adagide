from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import Qsci
import sys
from MainWindow import Ui_MainWindow
from FileManager import *
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
		self.dialogManager = DialogManager(self.mainWindow)
		# Connect signals from newFileDialog and saveAsDialog to controller methods
		self.dialogManager.newFileDialog.accepted.connect(self.on_new_file_accepted)
		self.dialogManager.saveAsDialog.accepted.connect(self.on_save_As_file_accepted)
		# HACK: get the current tab which contains the file to delete
		tabWidget = self.mainWindow.findChild(QtGui.QTabWidget,'tabWidget')
		tabWidget.removeTab(1)
		#connect find replace dialog buttons to there methods
		self.dialogManager.findReplaceDialog.close_button.clicked.connect(self.dialogManager.findReplaceDialog.hide)
		self.dialogManager.findReplaceDialog.replace_all_button.clicked.connect(self.replace_all)
		self.dialogManager.findReplaceDialog.replace_button.clicked.connect(self.replace)
		self.dialogManager.findReplaceDialog.find_button.clicked.connect(self.find)
		#overriding standard exit behavior hideous hack?
		self.mainWindow.closeEvent=self.on_exit
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
		self.disableProjectControls()
		
		
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
		if self.executionManager.running:
			self.displayOutput("Error: program already running. Press 'Stop' first.",
							"<font color=red>", "</font>")
		else:
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
			self.dialogManager.newFileDialog.open()
		return
	def on_new_file_accepted(self):
		newFileName = self.dialogManager.newFileDialog.textValue()
		if newFileName != "" and newFileName != None:
			for filename in os.listdir(self.fileManager.projectPath):
				if newFileName == filename:
					reply = QtGui.QMessageBox.warning(self.mainWindow, 'Make a New File',"The file "+filename+" already exists.\n Enter another name?", QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
					if reply == QtGui.QMessageBox.Ok:
						self.on_actionNew_File(False)
					return	
			fullname=self.fileManager.projectPath+"/"+newFileName
			newEditor=self.openFile(fullname)
			newEditor.save()
			#say created successfully
			self.displayOutput('#File, '+ str(newEditor.filename)+', was created succesfully.','<font color="green">','</font>')
			self.setFileControls()
		return	
		
	#To be changed to Import File	
	def on_actionOpen_File(self,checked):
		if self.fileManager.projectPath != None and self.fileManager.projectPath != "":
			fullname=QtGui.QFileDialog.getOpenFileName(caption='Open file',directory=self.fileManager.projectPath)
			if fullname != "" and fullname != None:
				newEditor=self.openFile(fullname)
				newEditor.setFile(newDirectory=self.fileManager.projectPath,newName=newEditor.filename)
				#say import succesful
				self.displayOutput('#File, '+ str(newEditor.filename)+', was imported succesfully.','<font color="green">','</font>')
				self.setFileControls()
		return
		
	def on_actionSave(self,checked):
		tabWidget=self.mainWindow.findChild(QtGui.QTabWidget,'tabWidget')
		current_tab = tabWidget.currentWidget() 
		current_tab.save()
		#say save success in output pane
		self.displayOutput('#File, '+ str(current_tab.filename)+', was saved succesfully.','<font color="green">','</font>')
		return
		
	def on_actionSave_As(self,checked):
		if self.fileManager.projectPath != None and self.fileManager.projectPath != "":
			self.dialogManager.saveAsDialog.open()
		return
	def on_save_As_file_accepted(self):
		newFileName = self.dialogManager.saveAsDialog.textValue()
		if newFileName != "" and newFileName != None:
			for filename in os.listdir(self.fileManager.projectPath):
				if newFileName == filename:
					reply = QtGui.QMessageBox.warning(self.mainWindow, 'Save as New',"The file "+filename+" already exists.\n Enter another name?", QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
					if reply == QtGui.QMessageBox.Ok:
						self.on_actionSave_As(False)
					return				
		tabWidget=self.mainWindow.findChild(QtGui.QTabWidget,'tabWidget')
		current_tab = tabWidget.currentWidget() 
		index = tabWidget.indexOf(current_tab)
		newTab=self.openFile(current_tab.file_path)
		newTab.save()
		current_tab.setFile(newDirectory=self.fileManager.projectPath,newName=newFileName)
		tabWidget.setTabText(index,newFileName)
		tabWidget.setCurrentIndex(tabWidget.indexOf(current_tab))
		#say created successfully
		self.displayOutput('#File, '+ str(newFileName)+', was created succesfully.','<font color="green">','</font>')
		self.setFileControls()
		return	

	def on_actionSave_All(self,checked):
		for projectFile in self.fileManager.files:
			projectFile.save()
			#say saved successfully
			self.displayOutput('#File, '+ str(projectFile.filename)+', was saved succesfully.','<font color="green">','</font>')
		return	
		
	def on_actionNewProject(self,checked):
		tabWidget=self.mainWindow.findChild(QtGui.QTabWidget,'tabWidget')
		tabWidget.clear()
		self.on_actionClose_Project(checked)
		dirPath = str(QtGui.QFileDialog.getSaveFileName(parent = self.mainWindow, caption='Create A New Project', directory='./'))
		if(dirPath != ""):
			if os.path.exists(dirPath):
				reply = QtGui.QMessageBox.warning(self.mainWindow, 'Make a New Project',"The directory "+filename+" already exists.\n Select another Directory?", QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
				if reply == QtGui.QMessageBox.Ok:
					self.on_actionNewProject(False)
				return
			else:
				os.makedirs(dirPath)
			if not os.path.exists(dirPath):
				QtGui.QMessageBox.Critical(self.mainWindow, 'ERROR',"Directory creation unsuccessful", QtGui.QMessageBox.Ok)
				#say there was an error
				self.displayOutput('#Project creation encountered an error.','<font color="red">','</font>')
				return
			self.fileManager.set(str(dirPath))
			#say success
			self.displayOutput('#Project , '+ self.fileManager.projectName+', was created succesfully.','<font color="green">','</font>')
			self.enableProjectControls()
			self.setFileControls()
		return		
		
	def on_actionOpen_Project(self,checked):
		tabWidget=self.mainWindow.findChild(QtGui.QTabWidget,'tabWidget')
		tabWidget.clear()
		self.on_actionClose_Project(checked)
		dirPath = str(QtGui.QFileDialog.getExistingDirectory(parent = self.mainWindow, caption='Open An Existing Project', directory='./'))
		if(dirPath != ""):
			self.fileManager.set(str(dirPath))
			for filename in os.listdir(dirPath):
				if fnmatch.fnmatch(filename, '*.c') or fnmatch.fnmatch(filename, '*.h') or fnmatch.fnmatch(filename, '*.cpp') or fnmatch.fnmatch(filename, '*.cxx') or fnmatch.fnmatch(filename, '*.txt'):
					self.openFile(dirPath +'/'+ filename)
			#say project open successfully
			self.displayOutput('#Project , '+ self.fileManager.projectName+', was opened succesfully.','<font color="green">','</font>')
			self.enableProjectControls()
			self.setFileControls()
		return	
	def on_actionDelete_File(self,checked):
		tabWidget=self.mainWindow.findChild(QtGui.QTabWidget,'tabWidget')
		current_tab = tabWidget.currentWidget() 
		if current_tab != 0:
			index = tabWidget.indexOf(current_tab)
			reply = QtGui.QMessageBox.warning(self.mainWindow, 'Delete this File?',
				"Are you sure you want to delete "+current_tab.filename, QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
			if reply == QtGui.QMessageBox.Yes:
				file=current_tab.filename
				tabWidget.removeTab(index)
				current_tab.setFile(newDirectory=self.fileManager.projectPath,newName=current_tab.filename+'.bak')
				current_tab.close();
				self.fileManager.remove(current_tab)
				os.remove(str(current_tab.file_path))
				#deletion successful
				self.displayOutput('#File, '+ file+', was deleted succesfully.','<font color="green">','</font>')
				self.setFileControls()
		pass		
	
	def on_actionClose_Project(self,checked):
		#stop any running process
		self.stop()
		#close each open file
		for projectFile in self.fileManager.files:
			self.closeFile(projectFile)
		#reset the fleManager
		self.fileManager.reset()
		self.disableProjectControls()
		return		
		
	#this is called when a user press the 'X' button to quit
	def on_exit(self,event):
		self.on_actionQuit(False)
		event.ignore()
		
	def on_actionQuit(self,checked):
		reply = QtGui.QMessageBox.question(self.mainWindow, 'Please Confirm',
            "Are you sure to quit?", QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)
		if reply == QtGui.QMessageBox.Yes:
			self.on_actionClose_Project(checked)
			sys.exit(0)
		pass

	def closeFile(self,projectFile):
		#will this need to run on a seperate thread?
		if projectFile.isModified() == True:
			reply = QtGui.QMessageBox.question(self.mainWindow, 'Save this File?',
            "Would you like to save your changes to "+projectFile.filename, QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)
			if reply == QtGui.QMessageBox.Yes:
				projectFile.save()
				#saved successfully
		tabWidget=self.mainWindow.findChild(QtGui.QTabWidget,'tabWidget')
		tabWidget.removeTab(tabWidget.indexOf(projectFile));
		return

	def openFile(self,projectFile):
		fpath=os.path.dirname(str(projectFile))
		fname=str(projectFile)+""
		fname=fname.replace(fpath+'/',"")
		newEditorPane=ProjectFile(fname,projectFile)
		self.fileManager.add(newEditorPane)
		tabWidget=self.mainWindow.findChild(QtGui.QTabWidget,'tabWidget')
		tabWidget.addTab(newEditorPane, QtCore.QString(newEditorPane.filename))
		tabWidget.setCurrentIndex(tabWidget.indexOf(newEditorPane))
		return newEditorPane

	def disableProjectControls(self):
		Widget=self.mainWindow.findChild(QtGui.QAction,'actionNew_File')
		Widget.setFont(QtGui.QFont("Ariel",10,5,False))
		Widget.setEnabled(False)
		Widget=self.mainWindow.findChild(QtGui.QAction,'actionOpen_File')
		Widget.setFont(QtGui.QFont("Ariel",10,5,False))
		Widget.setEnabled(False)
		Widget=self.mainWindow.findChild(QtGui.QAction,'actionClose_Project')
		Widget.setFont(QtGui.QFont("Ariel",10,5,False))
		Widget.setEnabled(False)
		self.setFileControls()
		return
	def enableProjectControls(self):
		Widget=self.mainWindow.findChild(QtGui.QAction,'actionNew_File')
		Widget.setFont(QtGui.QFont("Ariel",10,50,False))
		Widget.setEnabled(True)
		Widget=self.mainWindow.findChild(QtGui.QAction,'actionOpen_File')
		Widget.setFont(QtGui.QFont("Ariel",10,50,False))
		Widget.setEnabled(True)
		Widget=self.mainWindow.findChild(QtGui.QAction,'actionClose_Project')
		Widget.setFont(QtGui.QFont("Ariel",10,50,False))
		Widget.setEnabled(True)
		self.setFileControls()
		return
		
	def setFileControls(self):
		if self.fileManager.projectOpen:
			if self.fileManager.count > 0:
				Widget=self.mainWindow.findChild(QtGui.QAction,'actionDelete_File')
				Widget.setFont(QtGui.QFont("Ariel",10,50,False))
				Widget.setEnabled(True)
				Widget=self.mainWindow.findChild(QtGui.QAction,'actionSave')
				Widget.setFont(QtGui.QFont("Ariel",10,50,False))
				Widget.setEnabled(True)
				Widget=self.mainWindow.findChild(QtGui.QAction,'actionSave_All')
				Widget.setFont(QtGui.QFont("Ariel",10,50,False))
				Widget.setEnabled(True)
				Widget=self.mainWindow.findChild(QtGui.QAction,'actionSave_As')
				Widget.setFont(QtGui.QFont("Ariel",10,50,False))
				Widget.setEnabled(True)
				return
		Widget=self.mainWindow.findChild(QtGui.QAction,'actionDelete_File')
		Widget.setFont(QtGui.QFont("Ariel",10,5,False))
		Widget.setEnabled(False)
		Widget=self.mainWindow.findChild(QtGui.QAction,'actionSave')
		Widget.setFont(QtGui.QFont("Ariel",10,5,False))
		Widget.setEnabled(False)
		Widget=self.mainWindow.findChild(QtGui.QAction,'actionSave_All')
		Widget.setFont(QtGui.QFont("Ariel",10,5,False))
		Widget.setEnabled(False)
		Widget=self.mainWindow.findChild(QtGui.QAction,'actionSave_As')
		Widget.setFont(QtGui.QFont("Ariel",10,5,False))
		Widget.setEnabled(False)
		return
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
			self.dialogManager.findReplaceDialog.open()

	# Replace All
	def replace_all(self):

		tabWidget = self.mainWindow.findChild(QtGui.QTabWidget,'tabWidget')
		current_tab = tabWidget.currentWidget() 
		if current_tab is not None:
			check_states=self.dialogManager.findReplaceDialog.get_check_states()
			search_for=self.dialogManager.findReplaceDialog.search_for_text.text()
			replace_with=self.dialogManager.findReplaceDialog.replace_with_text.text()
			search_description_tup = (search_for,check_states['match case'],check_states['match entire word'],check_states['wrap around'],check_states['search backward'])

			if current_tab.current_search_selection != search_description_tup:
				self.find()

			while current_tab.current_search_selection == search_description_tup:
				current_tab.replace(replace_with)

				selection_start_row, selection_start_col, selection_end_row, selection_end_col = current_tab.getSelection()

				current_tab.setCursorPosition(selection_end_row, selection_end_col)

				self.find()

	# Replace
	def replace(self):
		check_states=self.dialogManager.findReplaceDialog.get_check_states()
		search_for=self.dialogManager.findReplaceDialog.search_for_text.text()
		replace_with=self.dialogManager.findReplaceDialog.replace_with_text.text()
		tabWidget = self.mainWindow.findChild(QtGui.QTabWidget,'tabWidget')
		current_tab = tabWidget.currentWidget()
		if current_tab is not None:

			search_description_tup = (search_for,check_states['match case'],check_states['match entire word'],check_states['wrap around'],check_states['search backward'])

			if current_tab.current_search_selection != search_description_tup:
				self.find()

			if current_tab.current_search_selection == search_description_tup:
				current_tab.replace(replace_with)

				selection_start_row, selection_start_col, selection_end_row, selection_end_col = current_tab.getSelection()

				current_tab.setCursorPosition(selection_end_row, selection_end_col)

				self.find()

	# Find
	def find(self):
		check_states=self.dialogManager.findReplaceDialog.get_check_states()
		search_for=self.dialogManager.findReplaceDialog.search_for_text.text()
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

