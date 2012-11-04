import os, sys, fnmatch
#import cs140adagide_qrc

from PyQt4 import QtCore, QtGui, uic

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        uic.loadUi("MainWindow.ui",self)

        # Connect up the buttons.
        self.actionOpen_File.triggered.connect(self.open_file_dialog)
    def open_file_dialog(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file','/home')
        f = open(fname, 'r')
        
        with f:        
            data = f.read()
            self.textEdit.setText(data) 
def main():
    app=QtGui.QApplication(sys.argv)
    windowView=MainWindow()
    windowView.show()
    sys.exit(app.exec_())



main()
