from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.Qt import PYQT_CONFIGURATION;
print(PYQT_CONFIGURATION["sip_flags"])
from PyQt5.QtWebEngineWidgets import QWebEngineView
from color import Color
from PyQt5 import QtPrintSupport
import syntax_py
from os import path, pardir, system as shell
import sys
import StandaloneApp
from number_bar import NumberBar
from sys import argv
from selenium import webdriver

lineBarColor = QColor("#DED6AC")
lineHighlightColor  = QColor("#F5F5F5")
tab = chr(9)
eof = "\n"


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow,self).__init__(*args, **kwargs)
        self.IDE()
        self.setWindowIcon(QIcon('icons/icon.png'))
        self.setWindowTitle('Web Browser Bot Standalone Application')
        self.setStyle(QStyleFactory.create('Fusion'))
        self.createMenuBar()
        self.initUI()

    def initUI(self):
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("http://www.google.com"))

        layout = QHBoxLayout()

        layout.addWidget(self.browser)
        layout.addWidget(self.win)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.show()



    def createMenuBar(self):
        toolbar = QToolBar("My main toolbar")
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)

        play_action = QAction(QIcon("images/play.png"), "&Play", self)
        play_action.setStatusTip("Play")
        play_action.triggered.connect(self.onMyToolBarButtonClick)
        toolbar.addAction(play_action)

        toolbar.addSeparator()

        pause_action = QAction(QIcon("images/pause.png"), "&Pause", self)
        pause_action.setStatusTip("Pause")
        pause_action.triggered.connect(self.onMyToolBarButtonClick)
        toolbar.addAction(pause_action)

        toolbar.addSeparator()

        stop_action = QAction(QIcon("images/stop.png"), "&Stop", self)
        stop_action.setStatusTip("Stop")
        stop_action.triggered.connect(self.onMyToolBarButtonClick)
        toolbar.addAction(stop_action)



        self.setStatusBar(QStatusBar(self))

        self.menu = self.menuBar()

        new_menu = self.menu.addMenu("&New")
        open_menu = self.menu.addMenu('&Open')
        save_menu = self.menu.addMenu('&Save')
        save_as_menu = self.menu.addMenu('&Save As')
        self.menu.addSeparator()

    def onMyToolBarButtonClick(self, s):
        print("click", s)

    def IDE(self):
        if not QSystemTrayIcon.isSystemTrayAvailable():
            QMessageBox.critical(None, "Systray",
                                 "I couldn't detect any system tray on this system.")
            sys.exit(1)
        self.win = StandaloneApp.myEditor()
        shell("cd " + self.win.appfolder)
        if len(argv) > 1:
            print(argv[1])
            self.win.openFileOnStart(argv[1])




app = QApplication(sys.argv)
window = MainWindow()

app.exec_()