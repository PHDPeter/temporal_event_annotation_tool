from PyQt5.QtWidgets import  QWidget, QLabel, QApplication, QGridLayout, QDial, QMessageBox, QFileDialog, QPushButton,  \
    QMenuBar, QPlainTextEdit, QAction, QMenu, QMainWindow, QCheckBox, QMdiArea, QMdiSubWindow, QDockWidget

from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot, QObject
from PyQt5.QtGui import QImage, QPixmap, QIcon

import PyQt5.QtGui as QtGui
from PyQt5.QtGui import QPalette, QColor

import action_time_antation_tool

import sys

class SubWindow(QMdiSubWindow):
    def __init__(self,th_used, parent = None):
        super(SubWindow, self).__init__(parent)
        #label = QLabel("Sub Window",  self)
        self.th_i=th_used

    def closeEvent(self, event):
        #for i,th_i in enumerate(self.label_v_list):
        self.th_i.th.stop()
        self.th_i.th.quit()
        self.th_i.th.wait()
        print("closing the thersed of this cam")
        #print("cam ID:"+str(i)+", shut down")

        #event.ignore()
        event.accept()

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.title = 'event annotation tool'
        self.left = 50
        self.top = 50
        self.v_width = 640-200 #1400#
        self.v_height = 480-200 #1000#
        self.set_input=0

        self.setWindowTitle(self.title)

        self.mdi = QMdiArea()
        self.setCentralWidget(self.mdi)
        self.mdi.tileSubWindows()

        PATH_FILE = '/home/barbara/Desktop/demo'#'/home/barbara/Desktop/car_data/Normal/Nevsky prospect traffic surveillance video'
        video_feed=action_time_antation_tool.annotation_openCV(PATH_FILE)

        v_sub = SubWindow(video_feed)  # QMdiSubWindow()
        v_sub.setWidget(video_feed)
        v_sub.resize(self.v_width+25, self.v_height+75)
        v_sub.setMaximumSize(self.v_width+25, self.v_height+75)
        v_sub.setWindowTitle("Feed " + str(len(self.label_v_list)))
        self.mdi.addSubWindow(v_sub)  # self.mdi
        self.mdi.tileSubWindows()
        v_sub.show()

def run_GUI():
    #quit_event = multiprocessing.Event()  # this event is trigger to force clean shutdown of the app
    #quit_event_handler = StopEvent(quit_event)  # set up ^C or SIGINT event handling to shutdown
    #signal(SIGINT, quit_event_handler.stop_handler)

    app = QApplication(sys.argv)
    # Force the style to be the same on all OSs:
    app.setStyle("Fusion")

    # Now use a palette to switch to dark colors:
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)

    #Win = App()
    #Win.show()
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run_GUI()