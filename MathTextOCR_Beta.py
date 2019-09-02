import sys
import time

from aip import AipOcr

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit, QFileDialog
from PyQt5.QtWidgets import QStackedLayout, QGridLayout
from PyQt5.QtGui import QPixmap, QCursor, QPainter, QBrush
from PyQt5.QtCore import Qt

import numpy as np
import cv2 as cv
import pyautogui as ag

APP_ID = ''
API_KEY = ''
SECRET_KEY = ''

DT = [0.4, 0.2, 1.6]

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

oImg_file_path = 'output.jpg'
oTxt_file_path = 'output.txt'

class MtocrToolbar(QMainWindow):
    file_path = 'math0.jpg'

    def __init__(self):
        super().__init__()
        self.initVar()
        self.initGui()

    def initVar(self):
        self.file_path = 'math0.jpg'
        self.file = open(self.file_path, 'rb')
    
    def initGui(self):
        self.setGeometry(1000, 1000, 200, 60)
        self.setWindowOpacity(0.85)
        self.setWindowTitle('MathTextOCR')

        self.wgt_blank = QWidget()
        
        # selection
        self.btn_file = QPushButton('打开文件')
        self.btn_file.clicked.connect(self.openFile)
        
        '''
        self.btn_rFirst = QPushButton('<<')
        self.btn_rFirst.clicked.connect(self.enableRecordFirst)

        self.btn_rPrev = QPushButton('<')
        self.btn_rPrev.clicked.connect(self.enableRecordPrev)

        self.btn_rNext = QPushButton('>')
        self.btn_rNext.clicked.connect(self.enableRecordNext)

        self.btn_rLast = QPushButton('>>')
        self.btn_rLast.clicked.connect(self.enableRecordLast)
        '''

        self.ldt_hotkey = QLineEdit()

        self.btn_isOK = QPushButton('OK')
        self.btn_isOK.clicked.connect(self.showPic)

        self.lyt_selection = QGridLayout()
        '''
        self.lyt_selection.addWidget(self.btn_file, 0, 0)
        self.lyt_selection.addWidget(self.btn_rFirst, 0, 1)
        self.lyt_selection.addWidget(self.btn_rPrev, 0, 2)
        self.lyt_selection.addWidget(self.btn_rNext, 0, 3)
        self.lyt_selection.addWidget(self.btn_rLast, 0, 4)
        self.lyt_selection.addWidget(self.ldt_hotkey, 0, 5)
        self.lyt_selection.addWidget(self.btn_isOK, 0, 6)
        '''
        self.lyt_selection.addWidget(self.btn_file, 0, 0)
        self.lyt_selection.addWidget(self.ldt_hotkey, 0, 1)
        self.lyt_selection.addWidget(self.btn_isOK, 0, 2)

        self.wgt_selection = QWidget()
        self.wgt_selection.setLayout(self.lyt_selection)

        # picture
        self.win_picture = MtocrPicture(self.file_path, 'm')

        # main
        self.lyt_main = QStackedLayout()
        self.lyt_main.addWidget(self.wgt_blank)
        self.lyt_main.addWidget(self.wgt_selection)
        self.lyt_main.setCurrentIndex(1)

        self.wgt_main = QWidget()
        self.wgt_main.setLayout(self.lyt_main)

        self.setCentralWidget(self.wgt_main)
        self.show()
    
    def openFile(self):
        file = QFileDialog.getOpenFileName(self, '选择文件', '', 'Image files (*.jpg , *.png)')[0]
        if file != '':
            print(file)
            self.file_path = file
            self.file = open(self.file_path, 'rb')
    
    '''
    def enableRecordFirst(self):
        width, height = ag.size()
        self.setGeometry(0, 0, width, height)
        self.setWindowOpacity(0.10)
        self.lyt_main.setCurrentIndex(0)
        self.rFirst = True 
    
    def recordFirst(self):
        self.setGeometry(300, 300, 200, 60)
        self.setWindowOpacity(0.85)
        self.lyt_main.setCurrentIndex(1)
        self.first = ag.position()
        self.rFirst = False
        print('First: ')
        print(self.first)
    
    def enableRecordPrev(self):
        width, height = ag.size()
        self.setGeometry(0, 0, width, height)
        self.setWindowOpacity(0.10)
        self.lyt_main.setCurrentIndex(0)
        self.rPrev = True 

    def recordPrev(self):
        self.setGeometry(300, 300, 200, 60)
        self.setWindowOpacity(0.85)
        self.lyt_main.setCurrentIndex(1)
        self.prev = ag.position()
        self.rPrev = False
        print('Prev: ')
        print(self.prev)
    
    def enableRecordNext(self):
        width, height = ag.size()
        self.setGeometry(0, 0, width, height)
        self.setWindowOpacity(0.10)
        self.lyt_main.setCurrentIndex(0)
        self.rNext = True 

    def recordNext(self):
        self.setGeometry(300, 300, 200, 60)
        self.setWindowOpacity(0.85)
        self.lyt_main.setCurrentIndex(1)
        self.next = ag.position()
        self.rNext = False        
        print('Next: ')
        print(self.next)

    def enableRecordLast(self):
        width, height = ag.size()
        self.setGeometry(0, 0, width, height)
        self.setWindowOpacity(0.10)
        self.lyt_main.setCurrentIndex(0)
        self.rLast = True

    def recordLast(self):
        self.setGeometry(300, 300, 200, 60)
        self.setWindowOpacity(0.85)
        self.lyt_main.setCurrentIndex(1)
        self.last = ag.position()
        self.rLast = False
        print('Last')
        print(self.last)
    '''
    
    def showPic(self):
        self.win_picture.setFilePath(self.file_path)
        if self.ldt_hotkey.text() != '':
            self.win_picture.setHotkey(self.ldt_hotkey.text()[0])
        self.win_picture.show()
    
    '''
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.rFirst:
                self.recordFirst()
            elif self.rPrev:
                self.recordPrev()
            elif self.rNext:
                self.recordNext()
            elif self.rLast:
                self.recordLast()
    '''



class MtocrPicture(QMainWindow):
    def __init__(self, fpath, hotkey):
        super().__init__()

        self.img = cv.imread('output.jpg', cv.IMREAD_GRAYSCALE)
        self.file_path = fpath
        self.hkUpper = ord(hotkey.upper())
        self.hkLower = ord(hotkey.lower())
        self.height = self.width = 0
        self.saveFlag = False
        self.inputFlag = False
        self.selectedRegion = []
        self.setWindowFlags(Qt.FramelessWindowHint)

    def setFilePath(self, fpath):
        self.file_path = fpath
        self.img = cv.imread(self.file_path, cv.IMREAD_GRAYSCALE)
        self.height, self.width = self.img.shape[:2]
    
    def setHotkey(self, hotkey):
        self.hkUpper = ord(hotkey.upper())
        self.hkLower = ord(hotkey.lower())

    def DoMathpixOcr(self):
        for region in self.selectedRegion:
            ag.hotkey('ctrl', 'alt', 'm')
            ag.moveTo(region[0], region[1], DT[0])
            ag.mouseDown(region[0], region[1])
            ag.moveRel(region[2], region[3], DT[1])
            ag.mouseUp()
            time.sleep(DT[2])

            clb = QApplication.clipboard()
            print(clb.text())

            row_top = region[1] - self.x()
            row_btm = row_top + region[3]
            col_lft = region[0] - self.y()
            col_rgt = col_lft + region[2]
            h = region[3] + 60
            white_1 = np.zeros((h, self.width), np.uint8)
            white_1.fill(255)
            white_2 = np.zeros((row_btm - row_top, self.width - col_lft), np.uint8)
            white_2.fill(255)
            self.img = np.vstack((self.img[:row_btm], white_1, self.img[row_btm:]))
            self.img[row_top+h:row_btm+h, col_rgt:] = self.img[row_top:row_btm, col_rgt:]
            self.img[row_top:row_btm, col_lft:] = white_2

            cv.putText(self.img, clb.text(), (20, row_btm + 40), cv.FONT_HERSHEY_TRIPLEX, 0.7, (0, 0, 0), 1, 4)

        cv.imwrite(oImg_file_path, self.img)

        f = open(oImg_file_path, 'rb')
        result = client.basicAccurate(f.read())
        fout = open(oTxt_file_path, 'w')
        for item in result['words_result']:
            fout.write(item['words'])
            fout.write('\n')
        fout.close()

    def mousePressEvent(self, event):
        if self.inputFlag and event.button() == Qt.LeftButton:
            x, y = ag.position()
            self.selectedRegion.append((x, y))

    def mouseReleaseEvent(self, event):
        if self.inputFlag and event.button() == Qt.LeftButton:
            x, y = ag.position()
            c = self.selectedRegion.pop()
            self.selectedRegion.append((c[0], c[1], x - c[0], y - c[1]))
            print(self.selectedRegion)
            # self.repaint()
            self.inputFlag = False
    
    def keyPressEvent(self, event):
        if event.key() == self.hkLower or event.key() == self.hkUpper:
            self.inputFlag = True
        if event.key() == Qt.Key_Return:
            self.DoMathpixOcr()

    def paintEvent(self, event):
        self.setGeometry(100, 100, self.width, self.height)
        qp = QPainter()
        qp.begin(self)
        qp.setCompositionMode(QPainter.CompositionMode_SourceOver)
        qp.drawPixmap(0, 0, QPixmap(self.file_path))
        '''
        qp.setBrush(QBrush(Qt.SolidPattern))
        for region in self.selectedRegion:
            qp.drawRect(region[0] - self.x(), region[1] - self.y(), region[2], region[3]) 
        '''
        qp.end()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = MtocrToolbar()
    sys.exit(app.exec_())
