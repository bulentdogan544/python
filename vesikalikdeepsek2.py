import sys
import cv2
import os
import tempfile
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from datetime import datetime
from pathlib import Path

# Yüz tanıma modeli
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1113, 1000)
        MainWindow.setMaximumSize(QtCore.QSize(1113, 1000))
        MainWindow.setStyleSheet("background-color: rgb(170, 170, 255);")
        MainWindow.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        
        # Kamera görüntüsü için label
        self.lblCamera = QtWidgets.QLabel(self.centralwidget)
        self.lblCamera.setGeometry(QtCore.QRect(110, 40, 911, 561))
        self.lblCamera.setText("")
        self.lblCamera.setStyleSheet("background-color: black; border: 2px solid white;")

        # Boyut seçim combobox
        self.cmbSize = QtWidgets.QComboBox(self.centralwidget)
        self.cmbSize.setGeometry(QtCore.QRect(760, 620, 241, 30))
        self.cmbSize.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.cmbSize.addItems(["150x180 (Standart)", "200x240 (Büyük)", "300x360 (Profesyonel)"])

        # Kamera seçim combobox
        self.cmbCamera = QtWidgets.QComboBox(self.centralwidget)
        self.cmbCamera.setGeometry(QtCore.QRect(110, 620, 600, 30))
        self.cmbCamera.setStyleSheet("background-color: rgb(255, 255, 255);")

        # Butonlar
        self.btnCapture = QtWidgets.QPushButton(self.centralwidget)
        self.btnCapture.setGeometry(QtCore.QRect(450, 670, 261, 71))
        self.btnCapture.setStyleSheet("""
            QPushButton {
                background-color: rgb(255, 170, 255);
                border-radius: 10px;
                font: bold 14px;
            }
            QPushButton:hover {
                background-color: rgb(255, 130, 255);
            }
        """)
        self.btnCapture.setText("KAMERAYI BAŞLAT")

        self.btnSave = QtWidgets.QPushButton(self.centralwidget)
        self.btnSave.setGeometry(QtCore.QRect(760, 670, 241, 71))
        self.btnSave.setStyleSheet("""
            QPushButton {
                background-color: rgb(255, 170, 255);
                border-radius: 10px;
                font: bold 14px;
            }
            QPushButton:hover {
                background-color: rgb(255, 130, 255);
            }
        """)
        self.btnSave.setText("KAYDET")

        self.btnExit = QtWidgets.QPushButton(self.centralwidget)
        self.btnExit.setGeometry(QtCore.QRect(140, 680, 261, 71))
        self.btnExit.setStyleSheet("""
            QPushButton {
                background-color: rgb(255, 100, 100);
                border-radius: 10px;
                font: bold 14px;
            }
            QPushButton:hover {
                background-color: rgb(255, 70, 70);
            }
        """)
        self.btnExit.setText("ÇIKIŞ")

        self.btnCopy = QtWidgets.QPushButton(self.centralwidget)
        self.btnCopy.setGeometry(QtCore.QRect(450, 760, 261, 50))
        self.btnCopy.setStyleSheet("""
            QPushButton {
                background-color: rgb(255, 200, 100);
                border-radius: 10px;
                font: bold 12px;
            }
            QPushButton:hover {
                background-color: rgb(255, 180, 80);
            }
        """)
        self.btnCopy.setText("KOPYALA")

        # Bilgi label'ları
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(420, 820, 281, 41))
        self.label.setStyleSheet("font: bold 12pt \"Arial\"; color: white;")
        self.label.setText("Karşıyaka Adliyesi Bilgi İşlem Şefliği")

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(440, 870, 221, 21))
        self.label_2.setStyleSheet("font: bold 10pt \"Arial\"; color: white;")
        self.label_2.setText("Ramazan DOĞAN Bilgisayar Teknikeri")

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.camera = None
        self.timer = QTimer()
        self.captured_image = None
        self.face_detected = False
        
        # Buton bağlantıları
        self.ui.btnCapture.clicked.connect(self.toggle_camera)
        self.ui.btnSave.clicked.connect(self.save_image)
        self.ui.btnExit.clicked.connect(self.close)
        self.ui.btnCopy.clicked.connect(self.copy_to_clipboard)
        
        # Vesikalık klasörü oluştur
        self.vesikalik_folder = Path.home() / "Documents" / "Vesikalik"
        if not self.vesikalik_folder.exists():
            self.vesikalik_folder.mkdir(parents=True)
        
        # Mevcut kameraları listele
        self.list_cameras()
    
    def list_cameras(self):
        """Mevcut kameraları tespit ederek combobox'a ekler"""
        self.ui.cmbCamera.clear()
        index = 0
        while True:
            cap = cv2.VideoCapture(index)
            if not cap.read()[0]:
                break
            self.ui.cmbCamera.addItem(f"Kamera {index}")
            cap.release()
            index += 1
    
    def toggle_camera(self):
        """Kamerayı başlatır veya durdurur"""
        if self.camera is None:
            self.start_camera()
        else:
            self.stop_camera()
    
    def start_camera(self):
        """Seçilen kamerayı başlatır"""
        camera_index = self.ui.cmbCamera.currentIndex()
        self.camera = cv2.VideoCapture(camera_index)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # 30ms'de bir güncelle
        self.ui.btnCapture.setText("DURDUR")
    
    def stop_camera(self):
        """Kamerayı durdurur"""
        self.timer.stop()
        if self.camera is not None:
            self.camera.release()
            self.camera = None
        self.ui.btnCapture.setText("KAMERAYI BAŞLAT")
        self.ui.lblCamera.clear()
        self.ui.lblCamera.setStyleSheet("background-color: black; border: 2px solid white;")
    
    def update_frame(self):
        """Kameradan gelen görüntüyü işler ve gösterir"""
        ret, frame = self.camera.read()
        if ret:
            # Yüz tespiti (ilk dosyadaki gibi parametreler)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            
            self.face_detected = len(faces) > 0
            
            for (x, y, w, h) in faces:
                # Yüz kutusunu çiz (ilk dosyadaki gibi)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            # Görüntüyü Qt formatına çevir
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            p = convert_to_Qt_format.scaled(
                self.ui.lblCamera.width(), 
                self.ui.lblCamera.height(), 
                QtCore.Qt.KeepAspectRatio
            )
            self.ui.lblCamera.setPixmap(QPixmap.fromImage(p))
            
            self.captured_image = frame
    
    def save_image(self):
        """Vesikalık fotoğrafı kaydeder"""
        if self.captured_image is not None and self.face_detected:
            # Seçilen boyuta göre ayarlar
            size_text = self.ui.cmbSize.currentText()
            
            if "150x180" in size_text:
                output_size = (150, 180)  # Standart vesikalık (35x45mm eşdeğeri)
            elif "200x240" in size_text:
                output_size = (200, 240)  # Büyük boy
            elif "300x360" in size_text:
                output_size = (300, 360)  # Profesyonel boy
            else:
                output_size = (150, 180)  # Varsayılan
            
            # Yüz tespiti ve kırpma
            gray = cv2.cvtColor(self.captured_image, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            
            if len(faces) > 0:
                (x, y, w, h) = faces[0]
                # Yüz bölgesini kırp (ilk dosyadaki gibi)
                face_img = self.captured_image[y:y+h, x:x+w]
                
                # Yeniden boyutlandır (en-boy oranını koru)
                resized_img = cv2.resize(face_img, output_size, interpolation=cv2.INTER_AREA)
                
                # Kaydet
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = self.vesikalik_folder / f"vesikalik_{timestamp}.jpg"
                cv2.imwrite(str(filename), resized_img)
                
                QMessageBox.information(
                    self, 
                    "Başarılı", 
                    f"Vesikalık başarıyla kaydedildi!\n\n"
                    f"Konum: {filename}\n"
                    f"Boyut: {output_size[0]}x{output_size[1]} piksel"
                )
            else:
                QMessageBox.warning(self, "Hata", "Yüz tespit edilemedi! Lütfen kameraya düzgün poz verin.")
        else:
            QMessageBox.warning(self, "Hata", "Kaydedilecek görüntü yok veya yüz tespit edilemedi!")
    
    def copy_to_clipboard(self):
        """Görüntüyü panoya kopyalar"""
        if self.captured_image is not None and self.face_detected:
            # Geçici dosya oluştur
            temp_file = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
            cv2.imwrite(temp_file.name, self.captured_image)
            
            # Panoya kopyala
            pixmap = QPixmap(temp_file.name)
            QtWidgets.QApplication.clipboard().setPixmap(pixmap)
            
            QMessageBox.information(self, "Başarılı", "Görüntü panoya kopyalandı!\n\nWord veya Paint'te yapıştırabilirsiniz.")
            
            # Geçici dosyayı sil
            temp_file.close()
            os.unlink(temp_file.name)
        else:
            QMessageBox.warning(self, "Hata", "Kopyalanacak görüntü yok veya yüz tespit edilemedi!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Modern görünüm
    
    # Font ayarı
    font = QtGui.QFont()
    font.setFamily("Arial")
    font.setPointSize(10)
    app.setFont(font)
    
    window = MainWindow()
    window.setWindowTitle("Vesikalık Fotoğraf Uygulaması")
    window.show()
    sys.exit(app.exec_())
