import sys
import base64
import requests
import json

from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QPixmap, QCursor, QPainter, QBrush
from PyQt5.QtCore import Qt
import numpy as np
import cv2 as cv

import io
import os
from google.cloud import vision
from google.cloud.vision import types



app_id = ""
app_key = ""
google_api_key = ""

history = []
remove = []



class Image:
    img_file_path = "math1.jpg"
    img_file = None
    height = width = 0
    count = 0

    def __init__(self, isPre = True, thres = 100):
        self.img_file = cv.imread(self.img_file_path, cv.IMREAD_GRAYSCALE)
        self.height, self.width = self.img_file.shape[:2]
        if isPre:
            self.imgPreprocess(thres)

    def getPath(self):
        return self.img_file_path

    def getSize(self):
        return (self.height, self.width)

    def imgPreprocess(self, thres):
        for i in range(0, self.height):
            for j in range(0, self.width):
                if self.img_file[i,j] < thres:
                    self.img_file[i,j] = 255

    def imgCrop(self, area):
        if area[0] == area[2] and area[1] == area[3]:
            return -1
        else:
            new = self.img_file[area[1]:area[3], area[0]:area[2]]
            save_file_path = "Equations\eqs_%d.jpg" % self.count
            self.count += 1
            cv.imwrite(save_file_path, new)
            history.append(area)
            remove.append(False)
            print("Crop image from (%d, %d) to (%d, %d), saved as .\%s." % \
                (area[0], area[1], area[2], area[3], save_file_path))
            return save_file_path

    def imgDeCrop(self, p):
        count = 0
        for area in history:
            if (area[0] - p[0]) * (area[2] - p[0]) < 0 and \
                (area[1] - p[1]) * (area[3] - p[1]) < 0:
                f = "Equations\eqs_%d.jpg" % count
                if os.path.exists(f):
                    os.remove(f)
                    remove[count] = True
            count += 1

    def finalCrop(self):
        count = 0
        for area in history:
            if remove[count] == False:
                cv.rectangle(self.img_file, (area[0], area[1]), (area[2], area[3]), \
                    (255,255,255), thickness = -1)
                cv.imwrite("output.jpg", self.img_file)
            count += 1
        return "output.jpg"



class GoogleApi():
    client = vision.ImageAnnotatorClient()
    imgInst = None
    file_name = None

    def __init__(self, img):
        self.imgInst = img
        self.file_name = self.imgInst.getPath()

        isNeed = input("Do you need pre-cropping? (y/n): ")
        if isNeed == 'y':
            self.initDetect()

    def initDetect(self):
        with io.open(self.file_name, "rb") as image_file:
            content = image_file.read()
        image = types.Image(content = content)
        response = self.client.document_text_detection(image = image)
        texts = response.full_text_annotation

        for page in texts.pages:
            for block in page.blocks:
                for paragraph in block.paragraphs:
                    coor = []
                    isMath = False
                    for word in paragraph.words:
                        for symbol in word.symbols:
                            t = symbol.text
                            c = symbol.confidence
                            if isMath == False:
                                if c < 0.8 or (t >= 'a' and t <= 'z') or \
                                    (t >= 'A' and t <= 'Z'):
                                    isMath = True
                                    x = symbol.bounding_box.vertices[0].x
                                    y = symbol.bounding_box.vertices[0].y
                                    coor.append(x)
                                    coor.append(y)
                            else:
                                if t.encode('utf-8') >= b'\x80\xff':
                                    isMath = False
                                    coor.append(x)
                                    coor.append(y)
                                    self.imgInst.imgCrop(coor)
                                    coor = []
                                x = symbol.bounding_box.vertices[2].x
                                y = symbol.bounding_box.vertices[2].y
        

    def detect(self, path):
        with io.open(path, "rb") as image_file:
            content = image_file.read()
        image = types.Image(content = content)
        response = self.client.document_text_detection(image = image)
        texts = response.full_text_annotation
        output = open("output.txt", mode = 'w')
        output.write(texts.text)
        output.flush()



class MainWindow(QWidget):
    eqs_file_path = "Equations\eqs_file.txt" 
    eqs_file = open(eqs_file_path, mode = 'a')
    bgX = bgY = edX = edY = -1 
    isDetection = True 
    mode = 0 # 0 - drag, 1 - click two, 2 - delete
    imgInst = Image(isPre = False)
    apiInst = GoogleApi(imgInst)

    def __init__(self, parent = None):
        QWidget.__init__(self)
        QWidget.setWindowTitle(self, "MathText OCR")

        QWidget.setGeometry(self, 100, 100, \
            self.imgInst.getSize()[1], self.imgInst.getSize()[0])

        # l = QLabel(self)
        # img = QPixmap(self.imgInst.getPath())
        # l.setPixmap(img)

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        qp.setCompositionMode(QPainter.CompositionMode_SourceOver)
        img = QPixmap(self.imgInst.getPath())
        qp.drawPixmap(0, 0, img)
        self.drawBrushes(qp)
        qp.end()

    def drawBrushes(self, qp):
        brush = QBrush(Qt.Dense6Pattern)
        qp.setBrush(brush)
        count = 0
        for a in history:
            if remove[count] == False:
                qp.drawRect(a[0], a[1], a[2]-a[0], a[3]-a[1])
            count += 1

    def ocrDetect(self):
        count = 0
        for t in remove:
            if remove[count] == False:
                save_file_path = "Equations\eqs_%d.jpg" % count

                print("Now processing the image...")
                img_data = 'data:image/jpg;base64,' + \
                    base64.b64encode(open(save_file_path, "rb").read()).decode() 
                r = requests.post("https://api.mathpix.com/v3/latex", \
                    data = json.dumps({"src": img_data}), \
                    headers = {"app_id": app_id, "app_key": app_key, \
                        "Content-type": "application/json"})
                data = json.loads(r.text)
                print("raw output: " + json.dumps(data, indent = 4, sort_keys = True))
                if data["latex_confidence"] < 0.4:
                    print("Detection Error.")
                    print("Equation detected: %s\n" % data["latex"])
                    self.eqs_file.write("%d: " % count + data["latex"] + '\n')
                    self.eqs_file.flush()
                else:
                    print("Detection succeeded.")
                    print("Equation detected: %s\n" % data["latex"])
                    self.eqs_file.write("%d: " % count + data["latex"] + '\n')
                    self.eqs_file.flush()

            count += 1

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            if self.mode == 0:
                self.bgX = e.pos().x()
                self.bgY = e.pos().y()
            elif self.mode == 1:
                if self.bgX == -1:
                    self.bgX = e.pos().x()
                    self.bgY = e.pos().y()
                else:
                    self.edX = e.pos().x()
                    self.edY = e.pos().y()
                    self.imgInst.imgCrop((self.bgX, self.bgY, self.edX, self.edY))
                    self.bgX = self.bgY = self.edX = self.edY = -1
        elif e.button() == Qt.RightButton:
            self.imgInst.imgDeCrop((e.pos().x(), e.pos().y()))
        self.update()

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            if self.mode == 0:
                self.edX = e.pos().x()
                self.edY = e.pos().y()
                self.imgInst.imgCrop((self.bgX, self.bgY, self.edX, self.edY))
                self.bgX = self.bgY = self.edX = self.edY = -1
        self.update()
        
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Return:
            print("Starting final OCR process...")
            output = self.imgInst.finalCrop()
            if self.isDetection == True:
                self.ocrDetect()
            self.apiInst.detect(output)
            print("OCR succeeded.")

    def closeEvent(self, event):
        self.eqs_file.write("====================\n")
        self.eqs_file.close()



def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

