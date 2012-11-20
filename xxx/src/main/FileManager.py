'''
A class which maintains the set of scintilla editors, filehandles, and filenames
Associated with the current project.

'''
import os, fnmatch, shutil
#from SourceEditor import SourceEditor
from PyQt4 import QtCore
from PyQt4 import Qsci
from PyQt4 import QtGui
# import QsciScintilla, QsciLexerCPP

class FileManager:
	def __init__(self):
		self.projectOpen = false
		self.projectPath = none
		self.files = []
		return

	def closeProject(self):
		#prompt to save each modified file
		return none

	def newProject(self):
		#call closeProject
		#start Dialog
		#create new directory
		#open that directory
		return none

	def openProject(self):
		#call closeProject
		#start Dialog		
		#open the directory
		return none

	def saveAll(self):
		#call save on all open files
		return none


'''
class ProjectModel(QtCore.QObject):
    
    #signals emitted by this model
    projectOpened = QtCore.pyqtSignal(bool)
    unsavedFiles = QtCore.pyqtSignal(list)
    fileOpened = QtCore.pyqtSignal(QtCore.QObject)
    fileClosed = QtCore.pyqtSignal(QtCore.QObject)
    fileModifiedStateChanged = QtCore.pyqtSignal(QtCore.QObject)
    statusMessage = QtCore.pyqtSignal(str)
    
    def __init__(self):
        "A model holding the current project."
        QtCore.QObject.__init__(self)
        
        #Keep track of the current project directory
        self.project_directory = None
        
        #List of the editors associated with this project
        self.file_editors = []
    
    def open(self, project_directory):
        "Tell the project model that we want to open a new/existing project."
        self.close()
        
        if self.closed:
            self.project_directory = project_directory
        
            for filename in os.listdir(str(project_directory)):
                if fnmatch.fnmatch(filename, '*.cpp') or fnmatch.fnmatch(filename, '*.h'):
                    self.__open_file(filename)
                    
            self.projectOpened.emit(True)
        
    def new_project(self, project_directory):
        if os.path.exists(project_directory):
            self.statusMessage.emit("The selected project name already exists. Either choose a different one, or use open to open the existing project.")
            return
        else:
            os.makedirs(project_directory)
        
        if not os.path.exists(project_directory):
            self.statusMessage.emit("There was an error creating the project. Check permissions.")
            return
        
        self.open(project_directory)
        
        if self.project_directory != project_directory:
            shutil.rmtree(project_directory)
                
    def __open_file(self, filename):
        "Helper function to open a file_editor for the current project."
        full_path = os.path.join(self.project_directory, filename)
        
        file_editor = ProjectFile(self, filename, full_path)
        file_editor.modificationStateChanged.connect(self.on_file_modification_state_changed)
        
        self.fileOpened.emit(file_editor)
        self.file_editors.append(file_editor)
        
    def __close_file(self, file_editor):
        "Helper function to close a file_editor for the current project."
        if file_editor not in self.file_editors:
            return
        
        self.file_editors.remove(file_editor)
        file_editor.close()
        
        self.fileClosed.emit(file_editor)
        file_editor.modificationStateChanged.disconnect(self.on_file_modification_state_changed)
        
    def on_file_modification_state_changed(self, file_editor):
        "Just re-emit the signal so that the view can handle it."
        self.fileModifiedStateChanged.emit(file_editor)
        
    def close(self):
        "Tell the project model that we want it to close."
        unsaved = []
        
        for file_editor in self.file_editors:
            if file_editor.modified:
                unsaved.append(file_editor)
        
        if len(unsaved) > 0:
            self.unsavedFiles.emit(unsaved)
        else:
            self.force_close()
                
    def force_close(self):
        "Tell the model to close all file_editors even unsaved ones without issuing unsavedFiles signal."
        
        for file_editor in self.file_editors[:]:
            self.__close_file(file_editor)
            
        self.project_directory = None
        self.projectOpened.emit(False)
        
    def new(self, filename):
        "Tell the project model that we want a new file by a given name."
        if not ( fnmatch.fnmatch(filename, '*.cpp') or fnmatch.fnmatch(filename, '*.h') ):
            self.statusMessage.emit("You must create file_editors with a '.cpp' or '.h' extension.")
            return
        
        full_path = os.path.join(self.project_directory, filename)
        if os.path.exists(full_path):
            self.statusMessage.emit("The specified file '%s' is already in this project directory." % filename)
            return
        
        #create the file
        
        with open(full_path, 'w') as filehandle:
            filehandle.write('')
            
        self.__open_file(filename)
        
    def delete(self, file_editor):
        "Move a file_editor that the user asks to have deleted into the '.project_trash' folder in the project."
        if not file_editor in self.file_editors:
            return
        
        trashes_directory = os.path.join(self.project_directory, ".project_trash")
        if not os.path.exists(trashes_directory):
            os.makedirs(trashes_directory)
            
        self.__close_file(file_editor)
            
        shutil.move(file_editor.file_path, os.path.join(trashes_directory, file_editor.filename))
        
    def save(self, file_editor):
        "Tell this project model to save the file that has the given name."
        
        #Questionable whether we should actually check this
        if file_editor in self.file_editors:
            file_editor.save()
    
    def save_all(self):
        "Tell this project model to save all file_editors."
        for file_editor in self.file_editors:
            file_editor.save()
    
    @property
    def closed(self):
        return self.project_directory == None and len(self.file_editors) == 0

    def filenames(self):
        temp = [os.path.join(self.project_directory, f.filename) for f in self.file_editors if f.extension == "cpp"]
        return temp
'''
