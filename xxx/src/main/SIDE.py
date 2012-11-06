# Declare/Initialize the python qt ui module
import sys
from PyQt4.QtGui import QApplication, QMainWindow 
from MainWindow import Ui_MainWindow

app = QApplication(sys.argv)
window = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(window)

# Create controller object, and register ui window with it
from Controller import Controller
controller = Controller(window, True)

# Display the ui
window.show()
sys.exit(app.exec_())

