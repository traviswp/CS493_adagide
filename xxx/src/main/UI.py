# Compile .ui file to a python module
from PyQt4 import uic

modfile = open("MainWindow.py", "w")
uic.compileUi("MainWindow.ui", modfile, execute=True)
modfile.close()
