from lib2to3.pytree import convert
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QFileDialog, QMessageBox
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
import sys
import cv2
import os

class UI(QMainWindow):
    def __init__(self) -> None:
        super(UI, self).__init__()

        #load ui file
        uic.loadUi(".\\userInterface.ui", self)

        #define our widgets
        self.button = self.findChild(QPushButton, "pushButton")
        self.label = self.findChild(QLabel, "label")

        #click dropdown Box
        self.button.clicked.connect(self.clicker)

        #show the app
        self.show()
    
    def clicker(self):
        fname = QFileDialog.getOpenFileName(self, "Open File", "C:\\Users", "All Files (*);; Video File (*.mp4)")
        imgAdd = self.convert(fname[0])

        self.pixmap = QPixmap(imgAdd)
        self.label.setPixmap(self.pixmap)

    def convert(self, address):
        cam = cv2.VideoCapture(address)

        for i in range(len(address) - 1, -1, -1):
            if address[i] == "/":
                break

        try:
            # creating a folder named data
            # if not os.path.exists('data'):
            #     os.makedirs('data')
            path = os.path.join(address[:i + 1], "data")
            os.mkdir(path)
        except OSError:
            self.show_popup("Error: Creating directory of data")
        
        # frame
        currentframe = 0

        
        while(True):
            
            # reading from frame
            ret,frame = cam.read()
        
            if ret:
                # if video is still left continue creating images
                name = address[:i] + '/data/frame' + str(currentframe) + '.jpg'
                print ('Creating...' + name)
        
                # writing the extracted images
                cv2.imwrite(name, frame)
        
                # increasing counter so that it will
                # show how many frames are created
                currentframe += 1
            else:
                break
        
        # Release all space and windows once done
        cam.release()
        cv2.destroyAllWindows()
        return name

    def show_popup(self, text):
        msg = QMessageBox()
        msg.setWindowTitle("ERROR")
        msg.setText(text)

        x = msg.exec_()


app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()