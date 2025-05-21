import sys
import cv2
import os
import pyperclip
import tempfile
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap, QClipboard
from datetime import datetime
from pathlib import Path

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1113, 1000)
        MainWindow.setMaximumSize(QtCore.QSize(1113, 1000))
        MainWindow.setStyleSheet("background-color: rgb(170, 170, 255);")
        MainWindow.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)  # Çarpıdan kapatma devre dışı

        self.centralwidget = QtWidgets.QWidget(MainWindow)

        self.lblCamera = QtWidgets.QLabel(self.centralwidget)
        self.lblCamera.setGeometry(QtCore.QRect(110, 40, 911, 561))
        self.lblCamera.setText("")

        self.cmbSize = QtWidgets.QComboBox(self.centralwidget)
        self.cmbSize.setGeometry(QtCore.QRect(760, 620, 241, 30))
        self.cmbSize.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.cmbSize.addItems(["145x150 (Küçük)", "150x200 (Standart)", "250x300 (Büyük)"])

        self.cmbCamera = QtWidgets.QComboBox(self.centralwidget)
        self.cmbCamera.setGeometry(QtCore.QRect(110, 620, 600, 30))
        self.cmbCamera.setStyleSheet("background-color: rgb(255, 255, 255);")

        self.btnCapture = QtWidgets.QPushButton(self.centralwidget)
        self.btnCapture.setGeometry(QtCore.QRect(450, 670, 261, 71))
        self.btnCapture.setStyleSheet("background-color: rgb(255, 170, 255);")
        self.btnCapture.setText("KAMERAYI BAŞLAT")

        self.btnSave = QtWidgets.QPushButton(self.centralwidget)
        self.btnSave.setGeometry(QtCore.QRect(760, 670, 241, 71))
        self.btnSave.setStyleSheet("background-color: rgb(255, 170, 255);")
        self.btnSave.setText("KAYDET")

        self.btnExit = QtWidgets.QPushButton(self.centralwidget)
        self.btnExit.setGeometry(QtCore.QRect(140, 680, 261, 71))
        self.btnExit.setStyleSheet("background-color: rgb(255, 170, 255);")
        self.btnExit.setText("ÇIKIŞ")

        self.btnCopy = QtWidgets.QPushButton(self.centralwidget)
        self.btnCopy.setGeometry(QtCore.QRect(450, 760, 261, 50))
        self.btnCopy.setStyleSheet("background-color: rgb(255, 200, 100);")
        self.btnCopy.setText("KOPYALA")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(420, 820, 281, 41))
        self.label.setStyleSheet("font: 75 12pt \"MS Shell Dlg 2\";")
        self.label.setText("Karşıyaka Adliyesi Bilgi İşlem Şefliği")

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(440, 870, 221, 21))
        self.label_2.setStyleSheet("font: 75 10pt \"MS Shell Dlg 2\";")
        self.label_2.setText("Ramazan DOĞAN Bilgisayar Teknikeri")

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)
