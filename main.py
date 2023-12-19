from PyQt5.QtWidgets import (QApplication, QWidget, QFileDialog, QLabel, QPushButton, QListWidget, QHBoxLayout, QVBoxLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PIL import Image
from PIL import ImageFilter
import os

class ImageProcessor():
    def __init__(self):
        self.image = None
        self.filename = None
        self.save_dir = "Modified/"
    def loadImage(self, filename):
        self.filename = filename
        image_path = os.path.join(workdir, filename)
        self.image = Image.open(image_path)
    def showImage(self, path):
        main_image.hide()
        pixmapimage = QPixmap(path)
        w, h = main_image.width(), main_image.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        main_image.setPixmap(pixmapimage)
        main_image.show()
    def do_bw(self):
        self.image = self.image.convert("L")
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_mirror(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_rotateL(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_rotateR(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_blur(self):
        self.image = self.image.filter(ImageFilter.BoxBlur(10))
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def saveImage(self):
        path = os.path.join(workdir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)


workdir = ''
def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()


def filter(files, extensions):
    results = []

    for file in files:
        for extension in extensions:
            if file.endswith(extension):
                results.append(file)
    return results

def showFilenamesList():
    chooseWorkdir()
    extensions = ['.jpg','.jpeg', '.png', '.gif', '.bmp']
    result = filter(os.listdir(workdir), extensions)
    list_files.clear()
    for i in result:
        list_files.addItem(i)

def ShowChosenImage():
    if list_files.currentRow() >= 0:
        filename = list_files.currentItem().text()
        workimage.loadImage(filename)
        image_path = os.path.join(workdir, workimage.filename)
        workimage.showImage(image_path)

workimage = ImageProcessor()


app = QApplication([])
main_win = QWidget()
main_win.resize(1000, 600)
main_win.setWindowTitle('RealPhotoshop')

main_image = QLabel("Картинка")
btn_folder = QPushButton("Папка")
list_files = QListWidget() 

btn_tleft = QPushButton("Лево")
btn_tright = QPushButton("Право")
btn_mirr = QPushButton("Зеркало")
btn_sharp = QPushButton("Резкость")
btn_black = QPushButton("Ч/Б")

useless_text = QLabel("Картинка")

folder_Lay = QVBoxLayout()
image_Lay = QVBoxLayout()
btn_Lay = QHBoxLayout()
main_Lay = QHBoxLayout()

folder_Lay.addWidget(btn_folder)
folder_Lay.addWidget(list_files)
image_Lay.addWidget(main_image)
btn_Lay.addWidget(btn_tleft)
btn_Lay.addWidget(btn_tright)
btn_Lay.addWidget(btn_mirr)
btn_Lay.addWidget(btn_sharp)
btn_Lay.addWidget(btn_black)
image_Lay.addLayout(btn_Lay)
main_Lay.addLayout(folder_Lay, 20)
#main_Lay.addWidget(useless_text)
main_Lay.addLayout(image_Lay, 80)


btn_folder.clicked.connect(showFilenamesList)

list_files.currentRowChanged.connect(ShowChosenImage)

btn_black.clicked.connect(workimage.do_bw)
btn_mirr.clicked.connect(workimage.do_mirror)
btn_tleft.clicked.connect(workimage.do_rotateL)
btn_tright.clicked.connect(workimage.do_rotateR)
btn_sharp.clicked.connect(workimage.do_blur)

main_win.setLayout(main_Lay)
main_win.show()
app.exec()