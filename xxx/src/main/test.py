import os, sys, fnmatch
#import cs140adagide_qrc

from PyQt4 import QtCore, QtGui, uic

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        uic.loadUi("MainWindow.ui",self)

        

class Controller():
    def __init__(self,MainWindow):
        # Connect up the buttons.
        MainWindow.actionOpen_File.triggered.connect(self.open_file_dialog)
        print 'baa'
        
    def open_file_dialog(self):
        print 'boo!'
        fname = QtGui.QFileDialog.getOpenFileName('Open file','/.')
        '''
        f = open(fname, 'r')
        
        with f:
            data = f.read()
            self.textEdit.setText(data) 
        '''
def main():
    app=QtGui.QApplication(sys.argv)
    windowView=MainWindow()
    Controller(windowView)
    windowView.show()
    sys.exit(app.exec_())



main()
