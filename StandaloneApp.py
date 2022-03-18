#!/usr/bin/python3
# -- coding: utf-8 --
from PyQt5.QtWidgets import QPlainTextEdit,QApplication, QFileDialog, QMessageBox,QTextEdit, QToolBar, QAction, QMenu, QMainWindow, QSystemTrayIcon, QStyleFactory, QSplitter, QTabWidget, QComboBox, QInputDialog, QLabel, QPushButton
from PyQt5.QtGui import QIcon, QColor, QTextCursor, QKeySequence,QFont
from PyQt5.QtCore import Qt, QDir, QFile, QFileInfo, QTextStream, QSettings, QProcess, QUrl
import syntax_py
from PyQt5.Qt import PYQT_CONFIGURATION
from PyQt5.QtWebEngineWidgets import QWebEngineView
from os import path, pardir, system as shell
import concurrent.futures
from sys import argv
import pyperclip as pc
from threading import Thread
from number_bar import NumberBar
import os
import style_sheets as ss
import editor as ed



CHROME_PATH = 'C:\Program Files (x86)\Google\Chrome\Application'

print(PYQT_CONFIGURATION["sip_flags"])
lineBarColor = QColor("#DED6AC")
lineHighlightColor  = QColor("#F5F5F5")
tab = "\t"
eof = "\n"
h = 800
w = 1400


PORT = 1222


class myEditor(QMainWindow):

    def __init__(self, parent = None):
        super(myEditor, self).__init__(parent)
        self.setWindowTitle('Web Browser Bot Standalone Application')
        self.setStyle(QStyleFactory.create('Fusion'))
        self.resize(w, h)
        self.browser = QWebEngineView()
        self.port = PORT
        self.url = ""
        self.browser.load(QUrl(f"http://127.0.0.1:{self.port}"))

        #elf.browser.setUrl(QUrl(f"-https://localhost:{self.port}"))
        self.template_file = []
        self.appfolder = path.abspath("./") + "/"
#        shell("cd " + self.appfolder)
        self.statusBar().showMessage(self.appfolder)
        self.MaxRecentFiles = 10
        self.windowList = []
        self.recentFileActs = []
        self.settings = QSettings("PyEdit", "PyEdit")
        self.dirpath = QDir.homePath() + "/Documents/python_files/"
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowIcon(QIcon(self.appfolder + "icons/icon.png"))
        QIcon.setThemeName('Faenza-Dark')
        self.editor = ed.TextEdit()
        self.editor.setStyleSheet(ss.style_sheet2)
        self.editor.setTabStopWidth(20)
        self.extra_selections = []
        self.mainText = "#!/usr/bin/python3\n# -*- coding: utf-8 -*-\n"
        self.fname = ""
        self.filename = ""
        self.mypython = "2"
        self.mylabel = QTextEdit()
        self.mylabel.setFixedHeight(160)
        self.mylabel.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.numbers = NumberBar(self.editor)
        self.createActions()
        self.highlighter = syntax_py.Highlighter(self.editor.document())

        self.label = QLabel("LOCALHOST PORT:")
        self.port_button = QPushButton(f"{self.port}")
        self.port_button.clicked.connect(self.copy_port_number)

        ### statusbar
        self.statusBar()
        self.statusBar().setStyleSheet(ss.style_sheet2)
        self.statusBar().addPermanentWidget(self.label)
        self.statusBar().addPermanentWidget(self.port_button)
#        self.statusBar().showMessage('Welcome')
        ### begin toolbar
        tb = QToolBar(self)
        tb.setMovable(True)


        #tb.setFloatable(True)
        tb.setWindowTitle("File Toolbar")        
        ### file buttons
        self.newAct = QAction("&New", self, shortcut=QKeySequence.New,
                toolTip="new file", triggered=self.newFile)
        self.newAct.setIcon(QIcon(self.appfolder + "/icons/new_file"))
        tb.addAction(self.newAct)
        
        self.openAct = QAction("&Open", self, shortcut=QKeySequence.Open,
                toolTip="open file", triggered=self.openFile)
        self.openAct.setIcon(QIcon(self.appfolder + "/icons/open"))
        tb.addAction(self.openAct)

        tb.addSeparator()

        self.saveAct = QAction("&Save", self, shortcut=QKeySequence.Save,
                toolTip="save file", triggered=self.fileSave)
        self.saveAct.setIcon(QIcon(self.appfolder + "/icons/save"))
        tb.addAction(self.saveAct)
        
        self.saveAsAct = QAction("&Save as ...", self, shortcut=QKeySequence.SaveAs,toolTip="save file as ...", triggered=self.fileSaveAs)
        self.saveAsAct.setIcon(QIcon(self.appfolder + "/icons/save_as"))
        tb.addAction(self.saveAsAct)

        tb.addSeparator()

        self.py3Act = QAction("Run in Python 3 (F5)", self, shortcut="F5",
                toolTip="run in Python 3 (F5)", triggered=self.runPy3)
        self.py3Act.setIcon(QIcon(self.appfolder + "/icons/play"))
        tb.addAction(self.py3Act)


        self.stopAct = QAction("Stop", self, shortcut="F7",
                              toolTip="stop (F7)", triggered=self.killPython)
        self.stopAct.setIcon(QIcon(self.appfolder + "/icons/stop"))
        tb.addAction(self.stopAct)

        tb.addSeparator()
        tb.layout().setSpacing(5)

        self.refreshAct = QAction("Refresh Port", self, shortcut="F8",
                               toolTip="refresh port (F8)", triggered=lambda:self.start_thread())
        self.refreshAct.setIcon(QIcon(self.appfolder + "/icons/refresh"))
        tb.addAction(self.refreshAct)

        self.refreshBrAct = QAction("Refresh Browser", self, shortcut="F9",
                                    toolTip="refresh browser (F9)", triggered=self.refreshBrowser)
        self.refreshBrAct.setIcon(QIcon(self.appfolder + "/icons/refresh-page"))
        tb.addAction(self.refreshBrAct)


        self.changePortAct = QAction("Change Port", self, shortcut="F10",
                                    toolTip="change port (F10)", triggered=self.changePort)
        self.changePortAct.setIcon(QIcon(self.appfolder + "/icons/ethernet"))
        tb.addAction(self.changePortAct)

        tb.addSeparator()

        self.openTemplateAct = QAction("Open Template", self, shortcut="F11",
                                     toolTip="open template (F11)", triggered=self.openTemplate)
        self.openTemplateAct.setIcon(QIcon(self.appfolder + "/icons/txt-file"))
        tb.addAction(self.openTemplateAct)

        """self.specifyBrowserAct = QAction("Specify Browser", self, shortcut="F12",
                                       toolTip="specify browser (F12)", triggered=self.specify_browser)
        self.specifyBrowserAct.setIcon(QIcon(self.appfolder + "/icons/website"))
        tb.addAction(self.specifyBrowserAct)"""

        self.addToolBar(tb)
        bar=self.menuBar()
        self.filemenu=bar.addMenu("File")
        self.separatorAct = self.filemenu.addSeparator()
        self.filemenu.addAction(self.newAct)
        self.filemenu.addAction(self.openAct)
        self.filemenu.addAction(self.saveAct)
        self.filemenu.addAction(self.saveAsAct)
        self.filemenu.addSeparator()
        for i in range(self.MaxRecentFiles):
            self.filemenu.addAction(self.recentFileActs[i])
        self.updateRecentFileActions()
        self.filemenu.addSeparator()
        self.clearRecentAct = QAction("Clear Recent Files List", self, triggered=self.clearRecentFiles)
        self.clearRecentAct.setIcon(QIcon.fromTheme("edit-clear"))
        self.filemenu.addAction(self.clearRecentAct)
        self.filemenu.addSeparator()

        
        editmenu = bar.addMenu("Edit")
        editmenu.addAction(QAction(QIcon('icons/undo.png'), "Undo", self, triggered = self.editor.undo, shortcut = "Ctrl+z"))
        editmenu.addAction(QAction(QIcon('icons/redo.png'), "Redo", self, triggered = self.editor.redo, shortcut = "Ctrl+y"))
        editmenu.addSeparator()
        editmenu.addAction(QAction(QIcon('icons/copy.png'), "Copy", self, triggered = self.editor.copy, shortcut = "Ctrl+c"))
        editmenu.addAction(QAction(QIcon('icons/cutting.png'), "Cut", self, triggered = self.editor.cut, shortcut = "Ctrl+x"))
        editmenu.addAction(QAction(QIcon('icons/paste.png'), "Paste", self, triggered = self.editor.paste, shortcut = "Ctrl+v"))
        editmenu.addAction(QAction(QIcon('icons/delete.png'), "Delete", self, triggered = self.editor.cut, shortcut = "Del"))
        editmenu.addSeparator()
        editmenu.addAction(QAction(QIcon('icons/select-all.png'), "Select All", self, triggered = self.editor.selectAll, shortcut = "Ctrl+a"))
        editmenu.addSeparator()
        editmenu.addAction(self.py3Act)
        editmenu.addSeparator()

        self.loadTemplates()

        self.installEventFilter(self)
        self.editor.setFocus()
        self.cursor = QTextCursor()
        self.editor.setTextCursor(self.cursor)
        self.editor.setPlainText(self.mainText)
        self.editor.moveCursor(self.cursor.End)
        self.editor.document().modificationChanged.connect(self.setWindowModified)
        # Brackets ExtraSelection ...
        self.left_selected_bracket  = QTextEdit.ExtraSelection()
        self.right_selected_bracket = QTextEdit.ExtraSelection()
        ### shell settings
        self.process = QProcess(self)
        self.process.setProcessChannelMode(QProcess.MergedChannels)
        self.process.readyRead.connect(self.dataReady)
        self.process.started.connect(lambda: self.mylabel.append("code starting to run"))
        self.process.finished.connect(lambda: self.mylabel.append("code stopped"))

        self.editor.setContextMenuPolicy(Qt.CustomContextMenu)
        self.editor.customContextMenuRequested.connect(self.contextMenuRequested)

        layoutV = QSplitter(Qt.Vertical)
        layoutB = QSplitter(Qt.Horizontal)
        layoutE = QSplitter(Qt.Horizontal)
        layoutT = QSplitter(Qt.Horizontal)
        layoutE2 = QSplitter(Qt.Vertical)


        layoutB.addWidget(self.browser)
        layoutE.addWidget(self.numbers)
        layoutE.addWidget(self.editor)
        layoutE2.addWidget(layoutE)

        self.mylabel.setMinimumHeight(28)
        self.mylabel.setStyleSheet(ss.style_sheet2)
        layoutE2.addWidget(self.mylabel)

        layoutT.addWidget(layoutB)
        layoutT.addWidget(layoutE2)

        # layoutV.addWidget(bar)
        # layoutV.addWidget(tb)
        layoutV.addWidget(layoutT)

        ### main window

        self.setCentralWidget(layoutV)

    #conntection with thread, so there is no freeze in refresh port buttons
    def refreshCode(self):
        stream = os.popen(f"npx kill-port {self.port}")
        return stream.read()
    def show_template_dialog(self):
        template, pressed = QInputDialog.getItem(self,"Select Template", "Options:", self.template_file, 0, False)
        if pressed:
            self.insertTemplate(template)

    def openTemplate(self):
        self.show_template_dialog()

    def show_browser_dialog(self):
        URL, ok = QInputDialog.getText(self, "Specify Browser", "Enter URL:")
        if ok:
            self.statusBar().showMessage(f"{URL}")
            self.refreshBrowser()

    def copy_port_number(self):
        pc.copy(f'{self.port}')

    def specify_browser(self):
        self.show_browser_dialog()


    def start_thread(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(self.refreshCode)
            self.statusBar().showMessage(future.result())

        """
        process = Thread(target=self.refreshCode, args=[])
        process.start()
        process.join()"""

    def refreshBrowser(self):
        self.browser.update()
        self.browser.load(QUrl(f"http://127.0.0.1:{self.port}"))
        #self.browser.setUrl(QUrl(f"https://localhost:{self.port}"))


    def contextMenuRequested(self,point):
        cmenu = self.editor.createStandardContextMenu()
        cmenu.addSeparator()
        cmenu.addAction(self.py3Act)
        cmenu.addSeparator()
        cmenu.exec_(self.editor.mapToGlobal(point))

    def show_port_dialog(self):
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(10)
        inputDialog = QInputDialog(None)
        inputDialog.setFixedSize(300,100)
        port, ok = inputDialog.getInt(self,'Change Port' ,'Select New Port Number:' , 1000, 1000, 9999, 1)
        inputDialog.setFont(font)
        if ok:
            self.statusBar().showMessage(f'Port number changes as {port}')
            self.port = port
            self.port_button.setText(f'{port}')

    def changePort(self):
        self.show_port_dialog()


    def loadTemplates(self):
        folder = self.appfolder + "/templates"
        if QDir().exists(folder):
            self.currentDir = QDir(folder)
            fileName = "*"
            files = self.currentDir.entryList([fileName],
                    QDir.Files | QDir.NoSymLinks)

            for i in range(len(files)):
                file = (files[i])
                if file.endswith(".py"):
                    self.template_file.append(file.replace(self.appfolder + "/templates", "").replace(".py", ""))

    def insertTemplate(self, file_name):
        line = int(self.getLineNumber())
        path = self.appfolder + "/templates/" + file_name + ".py"
        if path:
            inFile = QFile(path)
            if inFile.open(QFile.ReadOnly | QFile.Text):
                text = inFile.readAll()
                self.editor.setFocus()

                text = (self.mainText + str(text, encoding = 'utf8'))
                try: ### python 3
                    self.editor.setPlainText(text)
                except TypeError:  ### python 2
                    self.editor.setPlainText(text)
                self.setModified(True)
                self.statusBar().showMessage(f"{file_name}.py inserted")
                inFile.close()
                text= ""
                self.selectLine(line)
            else:
                self.statusBar().showMessage("Error Occured When Open Template!")

    def selectLine(self, line):
        return

    def dataReady(self):
        out = ""
        try:
            out = str(self.process.readAll(), encoding = 'utf8').rstrip()
        except TypeError:
            self.msgbox("Error", str(self.process.readAll(), encoding = 'utf8'))
            out = str(self.process.readAll()).rstrip()
        self.mylabel.append(out)
        self.mylabel.moveCursor(self.cursor.Start)
        if self.mylabel.find("line"):
            s = self.mylabel.toPlainText().partition("line")[2].partition("\n")[0]
            #self.gotoErrorLine(int(s))
        self.mylabel.moveCursor(self.cursor.End)
        self.mylabel.ensureCursorVisible()
        
    def createActions(self):
        for i in range(self.MaxRecentFiles):
            self.recentFileActs.append(
                   QAction(self, visible=False,
                            triggered=self.openRecentFile))

    def getLineNumber(self):
        self.editor.moveCursor(self.cursor.StartOfLine)
        linenumber = self.editor.textCursor().blockNumber() + 1
        return linenumber

    def gotoErrorLine(self, ln):
        linecursor = QTextCursor(self.editor.document().findBlockByLineNumber(ln-1))
        self.editor.moveCursor(QTextCursor.End)
        self.editor.setTextCursor(linecursor)
        self.editor.moveCursor(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)

    def clearLabel(self):
        self.mylabel.setText("")

    def openRecentFile(self):
        action = self.sender()
        if action:
            if (self.maybeSave()):
                self.openFileOnStart(action.data())

    def newFile(self):
        if self.maybeSave():
            self.editor.clear()
            self.editor.setPlainText(self.mainText)
            self.filename = ""
            self.setModified(False)
            self.editor.moveCursor(self.cursor.End)
            self.statusBar().showMessage("new File created.")
            self.editor.setFocus()
            self.setWindowTitle("new File[*]")

    def openFileOnStart(self, path=None):
        if path:
            inFile = QFile(path)
            if inFile.open(QFile.ReadWrite | QFile.Text):
                text = inFile.readAll()
                try:
                        # Python v3.
                    text = str(text, encoding = 'utf8')
                except TypeError:
                        # Python v2.
                    text = str(text)
                self.editor.setPlainText(text)
                self.setModified(False)
                self.setCurrentFile(path)
                self.editor.setFocus()
                self.statusBar().showMessage("File '" + path + "' loaded succesfully ")

    def openFile(self, path=None):
        if self.maybeSave():
            if not path:
                path, _ = QFileDialog.getOpenFileName(self, "Open File", self.dirpath,
                    "Python Files (*.py)")

            if path:
                self.openFileOnStart(path)
            
    def fileSave(self):
        if (self.filename != ""):
            file = QFile(self.filename)
            if not file.open( QFile.WriteOnly | QFile.Text):
                QMessageBox.warning(self, "Error",
                        "Cannot write file %s:\n%s." % (self.filename, file.errorString()))
                return

            outstr = QTextStream(file)
            QApplication.setOverrideCursor(Qt.WaitCursor)
            outstr << self.editor.toPlainText()
            QApplication.restoreOverrideCursor()                
            self.setModified(False)
            self.fname = QFileInfo(self.filename).fileName() 
            self.setWindowTitle(self.fname + "[*]")
            self.statusBar().showMessage("File saved.")
            self.setCurrentFile(self.filename)
            self.editor.setFocus()
            
            
        else:
            self.fileSaveAs()

    def fileSaveAs(self):
        fn, _ = QFileDialog.getSaveFileName(self, "Save as...", self.filename,
                "Python files (*.py)")

        if not fn:
            print("Error saving")
            return False

        lfn = fn.lower()
        if not lfn.endswith('.py'):
            fn += '.py'

        self.filename = fn
        self.fname = path.splitext(str(fn))[0].split("/")[-1]
        return self.fileSave()
        
    def closeEvent(self, e):
        if self.maybeSave():
            e.accept()
        else:
            e.ignore()
        
        ### ask to save

    def maybeSave(self):
        if not self.isModified():
            return True

        if self.filename.startswith(':/'):
            return True

        ret = QMessageBox.question(self, "Message",
                "<h4><p>The document was modified.</p>\n" \
                "<p>Do you want to save changes?</p></h4>",
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)

        if ret == QMessageBox.Yes:
            if self.filename == "":
                self.fileSaveAs()
                return False
            else:
                self.fileSave()
                return True

        if ret == QMessageBox.Cancel:
            return False

        return True   

    def runPy3(self):
        self.refreshCode()
        if not self.editor.toPlainText() == self.mainText:
            if self.filename:

                self.mypython = "3"
                self.statusBar().showMessage("running " + self.filename + " in Python 3")
                self.fileSave()
                cmd = "python"
                self.readData(cmd)

            else:
                self.filename = "tmp3.py"
                self.fileSave()
                self.runPy3()
        else:
            self.statusBar().showMessage("no code to run")
        self.refreshBrowser()

    def readData(self, cmd):
        self.mylabel.clear()
        dname = path.abspath(path.join(self.filename, pardir)) + "/"
        self.process.start(cmd,['-u', dname + self.strippedName(self.filename)])

    def killPython(self):
        if (self.mypython == "3"):
            cmd = "kill -9"
        self.readData(cmd)

    def match_left(self, block, character, start, found):
        map = {'{': '}', '(': ')', '[': ']'}

        while block.isValid():
            data = block.userData()
            if data is not None:
                braces = data.braces
                N = len(braces)

                for k in range(start, N):
                    if braces[k].character == character:
                        found += 1

                    if braces[k].character == map[character]:
                        if not found:
                            return braces[k].position + block.position()
                        else:
                            found -= 1

                block = block.next()
                start = 0

    def document(self):
        return self.editor.document
        
    def isModified(self):
        return self.editor.document().isModified()

    def setModified(self, modified):
        self.editor.document().setModified(modified)

    def setLineWrapMode(self, mode):
        self.editor.setLineWrapMode(mode)

    def clear(self):
        self.editor.clear()

    def setPlainText(self, *args, **kwargs):
        self.editor.setPlainText(*args, **kwargs)

    def setDocumentTitle(self, *args, **kwargs):
        self.editor.setDocumentTitle(*args, **kwargs)

    def setCurrentFile(self, fileName):
        self.filename = fileName
        if self.filename:
            self.setWindowTitle(self.strippedName(self.filename) + "[*]")
        else:
            self.setWindowTitle("no File")      
        
        files = self.settings.value('recentFileList', [])

        try:
            files.remove(fileName)
        except ValueError:
            pass

        files.insert(0, fileName)
        del files[self.MaxRecentFiles:]

        self.settings.setValue('recentFileList', files)

        for widget in QApplication.topLevelWidgets():
            if isinstance(widget, myEditor):
                widget.updateRecentFileActions()

    def updateRecentFileActions(self):
        mytext = ""
        files = self.settings.value('recentFileList', [])

        numRecentFiles = min(len(files), self.MaxRecentFiles)

        for i in range(numRecentFiles):
            text = "&%d %s" % (i + 1, self.strippedName(files[i]))
            self.recentFileActs[i].setText(text)
            self.recentFileActs[i].setData(files[i])
            self.recentFileActs[i].setVisible(True)
            self.recentFileActs[i].setIcon(QIcon.fromTheme("gnome-mime-text-x-python"))

        for j in range(numRecentFiles, self.MaxRecentFiles):
            self.recentFileActs[j].setVisible(False)

        self.separatorAct.setVisible((numRecentFiles > 0))
        
    def strippedName(self, fullFileName):
        return QFileInfo(fullFileName).fileName()
        
    def clearRecentFiles(self):
        self.settings.clear()
        self.updateRecentFileActions()
        
    def msgbox(self,title, message):
        QMessageBox.warning(self, title, message)



if __name__ == '__main__':
    import sys
    app = QApplication(argv)
    if not QSystemTrayIcon.isSystemTrayAvailable():
        QMessageBox.critical(None, "Systray",
                             "I couldn't detect any system tray on this system.")
        sys.exit(1)
    win = myEditor()
    shell("cd " + win.appfolder)
    win.setWindowTitle("Web Browser Bot Standalone Application" + "[*]")
    win.show()
    if len(argv) > 1:
        print(argv[1])
        win.openFileOnStart(argv[1])

    app.exec_()
