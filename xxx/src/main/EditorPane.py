'''
A class which maintains the set of scintilla editors, filehandles, and filenames
Associated with the current project.

'''
import os, fnmatch, shutil
#from SourceEditor import SourceEditor
from PyQt4 import QtCore
from PyQt4 import Qsci
from PyQt4 import QtGui
from PyQt4.Qsci import QsciScintilla, QsciScintillaBase, QsciLexerPython
# import QsciScintilla, QsciLexerCPP

class FileEditor(Qsci.QsciScintilla):
    """
    The settings and configuration of this class are based on the example tutorial by Eli Bendersky.
    http://eli.thegreenplace.net/2011/04/01/sample-using-qscintilla-with-pyqt/
    """
    
    #def __init__(self, parent):
    def __init__(self):

        Qsci.QsciScintilla.__init__(self)
        
        # Set the default font
        font = QtGui.QFont()
        font.setFamily('Courier') #Monospace
        font.setFixedPitch(True)
        font.setPointSize(10)
        self.setFont(font)
        self.setMarginsFont(font)
        
        # Margin 0 is used for line numbers 
        fontmetrics = QtGui.QFontMetrics(font)
        self.setMarginsFont(font)
        self.setMarginWidth(0, fontmetrics.width("0000"))
        self.setMarginLineNumbers(10, True)
        self.setMarginsBackgroundColor(QtGui.QColor("#cccccc"))

        
        ################################################
        self.setWhitespaceVisibility(self.WsVisible)
        ################################################

        
        # same-line brace matching....
        self.setBraceMatching(Qsci.QsciScintilla.SloppyBraceMatch)
        
        # Current line visible with special background color
        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QtGui.QColor("#99ccff"))
        
        # Choosing a lexer (syntax highlighting)
        lexer = Qsci.QsciLexerCPP() # C++ lexer
        lexer.setDefaultFont(font)
        self.setLexer(lexer)
        self.SendScintilla(Qsci.QsciScintilla.SCI_STYLESETFONT, 1, 'Courier')
        
        self.SendScintilla(Qsci.QsciScintilla.SCI_SETHSCROLLBAR, 0)
        #self.SendScintilla(Qsci.QsciScintilla.SCI_SETSCROLLWIDTH, 10)
        #self.SendScintilla(Qsci.QsciScintilla.SCI_SETSCROLLWIDTHTRACKING, 1)
        
        # not too small
        self.setMinimumSize(200, 200)


        ###################################################################

        # set vertical line at character 80 
        self.setEdgeMode(QsciScintilla.EdgeLine)
        self.setEdgeColumn(80)
        self.setEdgeColor(QtGui.QColor("#3333ff"))


class ProjectFile(FileEditor):

    modificationStateChanged = QtCore.pyqtSignal(QtCore.QObject)

    def __init__(self, filename, file_path, parent_model=None):
        FileEditor.__init__(self)
        self.parent_model = parent_model
        self.filename = filename
        self.file_path = file_path
        self.filehandle = QtCore.QFile(self.file_path)
        self.filehandle.open(QtCore.QIODevice.ReadWrite)
        self.read(self.filehandle)
        self.setModified(False)
        #self.selectionChanged.connect(self.on_selection_changed)
        self.modificationChanged.connect(self.on_modification_changed)

        # Used to keep track of what search the current selection is a result of.
        # None indicates that the current selection is not the result of a search operation.
        self.current_search_selection = None

        # if the project file is a text file, then turn off syntax highlighting
        if ".txt" in self.filename:
            self.setLexer(None)


    def on_selection_changed(self):
        self.current_search_selection = None

    def save(self):
        #"Save this file"
        if self.filehandle != None:
            self.filehandle.seek(0)
            self.filehandle.resize(0)
            self.write(self.filehandle)
            self.filehandle.flush()
            self.setModified(False)
        return

    def setFile(self,newDirectory=None,newName=None):
        if newDirectory == None or newDirectory == '':
            newDirectory=os.path.dirname(str(file_path))
        if newName == None or newName == '':
            newName=self.filename
        for filename in os.listdir(newDirectory):
            if newName == filename:
                #A file by that name already exists
                #overwrite reject or prompt
                return False	

        self.filehandle.close()
        self.filehandle=QtCore.QFile(newDirectory+'/'+newName)
        self.filehandle.open(QtCore.QIODevice.ReadWrite)
        self.filehandle.seek(0)
        self.filehandle.resize(0)
        self.write(self.filehandle)
        self.filehandle.flush()
        self.setModified(False)				
        return True

    def close(self):
        self.filehandle.close()
        self.filehandle = None

    @property
    def modified(self):
        "Check if the file is modified compared to the saved version."
        return self.isModified()

    @property
    def extension(self):
        return self.filename.split(".")[-1]

    def on_modification_changed(self, value):
        self.modificationStateChanged.emit(self)


