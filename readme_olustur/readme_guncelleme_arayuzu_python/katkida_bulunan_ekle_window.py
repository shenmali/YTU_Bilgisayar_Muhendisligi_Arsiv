import sys
import json
from PyQt5.QtWidgets import (QLineEdit, QDialog, QPushButton, QVBoxLayout, 
                             QDesktopWidget, QLabel, QMessageBox)
from threadler import KatkiEkleThread  
from progress_dialog import CustomProgressDialog
import requests  # requests modülünü içe aktar

JSON_DOSYASI = '../katkida_bulunanlar.json'

class KatkidaBulunanEkleWindow(QDialog):
    def __init__(self, parent):
        super().__init__()
        self.setModal(True)
        self.parent = parent
        self.title = 'Katkıda Bulunan Ekle'
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setMinimumSize(500, 200)  # Pencerenin en küçük olabileceği boyutu ayarlayın
        self.resize(500, 200)  # Pencerenin başlangıç boyutunu ayarlayın

        layout = QVBoxLayout()
        self.progressDialog = CustomProgressDialog('Kontrol Ediliyor...', self)
        self.progressDialog.close()
        # Ad ve GitHub Linki için giriş alanları
        self.name_label = QLabel('Ad:')
        self.name_input = QLineEdit()
        self.github_label = QLabel('GitHub Kullanıcı Adı:')
        self.github_input = QLineEdit()
        self.ekle_btn = QPushButton('Ekle', self)
        self.ekle_btn.setStyleSheet("background-color: green;")
        # Butona basıldığında ekleme işlevini çalıştır
        self.ekle_btn.clicked.connect(self.kaydet)

        # Arayüze elemanları ekle
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.github_label)
        layout.addWidget(self.github_input)
        layout.addWidget(self.ekle_btn)
        
        self.setLayout(layout)
        self.center()  # Pencereyi ekranın merkezine yerleştir
        self.show()

    def center(self):
        # Pencereyi ekranın ortasına al
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    def kaydet(self):
        # Thread örneğini oluştur
        ad = self.name_input.text()
        github_kullanici_adi = self.github_input.text()
        self.thread = KatkiEkleThread(ad, github_kullanici_adi, JSON_DOSYASI,self)
        self.thread.finished.connect(self.islemSonucu)
        # ProgressDialog'u göster
        self.progressDialog.show()
        self.thread.start()
    def islemSonucu(self, success, message):
        self.progressDialog.close()
        if success:
            QMessageBox.information(self, 'Başarılı', message)
            # Gerekli güncellemeleri yapın ve pencereyi kapatın
            self.parent.butonlariYenile()
            self.close()
        else:
            QMessageBox.warning(self, 'Hata', message)