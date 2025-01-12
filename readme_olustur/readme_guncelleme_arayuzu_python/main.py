import sys
from PyQt5.QtWidgets import QApplication,QDesktopWidget, QWidget, QPushButton, QVBoxLayout,QProgressDialog, QMessageBox
from PyQt5.QtCore import Qt
from katkida_bulunanlari_duzenle_window import KatkidaBulunanGuncelleWindow
from yazarin_notlari_duzenle_window import YazarinNotlariWindow
from ders_ekle_guncelle_window import DersEkleGuncelleWindow
from hoca_ekle_guncelle_window import HocaEkleGuncelleWindow
from progress_dialog import CustomProgressDialog
from threadler import ScriptRunnerThread
class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Readme Düzenleyici'
        self.width = 540
        self.height = 200
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.resize(self.width, self.height)
        layout = QVBoxLayout()
        # Butonları oluştur
        self.buttons = [
            QPushButton('Katkıda Bulunan Ekle/Güncelle'),
            QPushButton('Yazarın Notları Ekle/Güncelle'),
            QPushButton('Hoca Ekle/Güncelle'),
            QPushButton('Ders Ekle/Güncelle'),
            QPushButton('Readme Scripti Çalıştır')
        ]

        self.progressDialog = CustomProgressDialog('README.md dosyaları güncelleniyor...', self)
        self.progressDialog.close()
        # Her butona tıklama işleyicisi ekle
        self.buttons[0].clicked.connect(self.acKatkidaBulunanEkleGuncelle)
        self.buttons[1].clicked.connect(self.acYazarinNotlari)
        self.buttons[2].clicked.connect(self.acHocaEkleGuncelle)
        self.buttons[3].clicked.connect(self.acDersEkleGuncelle)
        self.buttons[4].clicked.connect(self.readmeScriptiCalistir)
        # Butonları pencereye ekle
        for btn in self.buttons:
            layout.addWidget(btn)

        # Layout'u ayarla
        self.setLayout(layout)
        self.show()
        self.center(),

    def center(self):
        # Pencereyi ekranın ortasına al
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    def acKatkidaBulunanEkleGuncelle(self):
        # Katkıda Bulunan Güncelle penceresini aç
        self.katkidaBulunanGuncelleWindow = KatkidaBulunanGuncelleWindow()
        self.katkidaBulunanGuncelleWindow.show()
    def acYazarinNotlari(self):
        # Katkıda Bulunan Güncelle penceresini aç
        self.yazarinNotlariWindow = YazarinNotlariWindow()
        self.yazarinNotlariWindow.show()
    def acHocaEkleGuncelle(self):
        # Katkıda Bulunan Güncelle penceresini aç
        self.hocaEkleGuncelleWindow = HocaEkleGuncelleWindow()
        self.hocaEkleGuncelleWindow.show()
    def acDersEkleGuncelle(self):
        # Katkıda Bulunan Güncelle penceresini aç
        self.dersEkleGuncelleWindow = DersEkleGuncelleWindow()
        self.dersEkleGuncelleWindow.show()

    def readmeScriptiCalistir(self):
        self.progressDialog.show()

        paths = ('../google_forum_islemleri', '..')
        self.thread = ScriptRunnerThread(paths)
        self.thread.finished.connect(self.onFinished)
        self.thread.error.connect(self.onError)
        self.thread.start()

    def onFinished(self):
        self.progressDialog.close()
        QMessageBox.information(self, 'Başarılı', 'README.md dosyaları güncellendi!')

    def onError(self, message):
        self.progressDialog.close()
        QMessageBox.critical(self, 'Hata', f'Bir hata oluştu: {message}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
