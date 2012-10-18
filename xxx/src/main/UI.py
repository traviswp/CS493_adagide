# Compile .ui file to a python module
from PyQt4 import uic

#uic.compileUiDir("/home/proteac/Desktop")
modfile = open("MainWindow.py", "w")
uic.compileUi("MainWindow.ui", modfile, execute=True)
modfile.close()

# Display the python qt ui module
import sys
from PyQt4.QtGui import QApplication, QMainWindow 
from MainWindow import Ui_MainWindow

app = QApplication(sys.argv)
window = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(window)

window.show()
sys.exit(app.exec_())

