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
		self.projectOpen = False
		self.projectPath = ""
		self.projectName= ""
		self.count = 0
		self.files = []
		return
		
	def set(self, filepath):
		self.projectOpen = True
		self.projectPath = filepath
		Ppath=os.path.dirname(str(filepath))
		Pname=str(filepath)+""
		Pname=Pname.replace(Ppath+'/',"")
		self.projectName=str(Pname)
		self.count = 0
		self.files = []
		return
		
	def reset(self):
		self.projectOpen = False
		self.projectPath = ""
		self.projectName= ""
		self.count = 0
		self.files = []
		return

	def remove(self, object):
		self.count-= 1
		self.files.remove(object)
		
	def add(self, object):
		self.count+= 1
		self.files.append(object)