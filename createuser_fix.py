# -*- coding: utf-8 -*-
import sys
import mysql.connector
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

# ==========================================
# 1. KONFIGURASI DATABASE (MODEL)
# ==========================================
print("➤ Memulai Program...")
print("➤ Menghubungkan ke Database...")

mydb = None
mycursor = None

try:
    # Coba koneksi ke Database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",       # Sesuaikan password XAMPP (biasanya kosong)
        database="pbo_uas" # Pastikan nama database BENAR
    )
    mycursor = mydb.cursor()
    print("✅ Koneksi Database BERHASIL!")
except mysql.connector.Error as e:
    print(f"❌ KONEKSI GAGAL: {e}")
    print("   Pastikan XAMPP (MySQL) sudah di-Start.")
    # Kita tidak exit, agar UI tetap muncul dan User melihat errornya di layar

class User:
    @staticmethod
    def insert_data(username, password, nama_lengkap, level):
        # Cek koneksi
        if mydb is None or not mydb.is_connected():
            return False, "Database tidak terhubung! Cek XAMPP."
        
        try:
            # Query Insert (Tanpa ID karena Auto Increment)
            sql = "INSERT INTO users (username, password, nama_lengkap, level) VALUES (%s, %s, %s, %s)"
            val = (username, password, nama_lengkap, level)
            
            mycursor.execute(sql, val)
            mydb.commit()
            print(f"➤ Data tersimpan. Rows affected: {mycursor.rowcount}")
            return True, "Data berhasil disimpan!"
        except mysql.connector.Error as err:
            print(f"➤ Error SQL: {err}")
            return False, f"Error Database: {err}"

# ==========================================
# 2. TAMPILAN UI (VIEW & CONTROLLER)
# ==========================================
class Ui_FormTambahUser(object):
    def setupUi(self, FormTambahUser):
        print("➤ Menyiapkan UI...")
        FormTambahUser.setObjectName("FormTambahUser")
        FormTambahUser.resize(600, 750)
        FormTambahUser.setStyleSheet("""
            QWidget { background-color: #121212; color: #E0E0E0; font-family: 'Segoe UI'; font-size: 11pt; }
            QLineEdit, QComboBox { background-color: #2D2D2D; border: 1px solid #404040; border-radius: 8px; padding: 8px; color: white; }
            QLineEdit:focus, QComboBox:focus { border: 2px solid #2962FF; }
            QPushButton { background-color: #333333; border: 1px solid #444444; border-radius: 8px; padding: 10px; color: white; font-weight: bold; }
            QPushButton#btnSimpan { background-color: #2962FF; border: none; }
            QPushButton#btnSimpan:hover { background-color: #1565C0; }
            QPushButton#btnKembali { background-color: #D32F2F; border: none; }
            QPushButton#btnKembali:hover { background-color: #B71C1C; }
        """)

        self.layout = QtWidgets.QVBoxLayout(FormTambahUser)

        # JUDUL
        self.label_judul = QtWidgets.QLabel("Tambah User")
        self.label_judul.setStyleSheet("font-size: 28px; font-weight: bold; margin-bottom: 20px;")
        self.label_judul.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.label_judul)

        # GROUP BOX
        self.group = QtWidgets.QGroupBox("Data User Baru")
        self.group.setStyleSheet("QGroupBox { border: 1px solid #333; border-radius: 10px; margin-top: 20px; } QGroupBox::title { color: #82B1FF; }")
        self.form_layout = QtWidgets.QVBoxLayout(self.group)

        # ID (Disabled - Auto Increment)
        self.form_layout.addWidget(QtWidgets.QLabel("ID User (Otomatis):"))
        self.lineEdit_id = QtWidgets.QLineEdit()
        self.lineEdit_id.setPlaceholderText("Auto-Increment")
        self.lineEdit_id.setEnabled(False)
        self.lineEdit_id.setStyleSheet("background-color: #1a1a1a; color: gray;")
        self.form_layout.addWidget(self.lineEdit_id)

        # NAMA
        self.form_layout.addWidget(QtWidgets.QLabel("Nama Lengkap:"))
        self.lineEdit_nama = QtWidgets.QLineEdit()
        self.lineEdit_nama.setPlaceholderText("Contoh: Ruli")
        self.form_layout.addWidget(self.lineEdit_nama)

        # USERNAME
        self.form_layout.addWidget(QtWidgets.QLabel("Username:"))
        self.lineEdit_username = QtWidgets.QLineEdit()
        self.lineEdit_username.setPlaceholderText("Username Login")
        self.form_layout.addWidget(self.lineEdit_username)

        # PASSWORD
        self.form_layout.addWidget(QtWidgets.QLabel("Password:"))
        self.lineEdit_password = QtWidgets.QLineEdit()
        self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.form_layout.addWidget(self.lineEdit_password)

        # LEVEL
        self.form_layout.addWidget(QtWidgets.QLabel("Level:"))
        self.comboBox_level = QtWidgets.QComboBox()
        self.comboBox_level.addItems(["User", "Admin"])
        self.form_layout.addWidget(self.comboBox_level)

        # TOMBOL SIMPAN
        self.btnSimpan = QtWidgets.QPushButton("💾 Simpan Data")
        self.btnSimpan.setObjectName("btnSimpan")
        self.form_layout.addWidget(self.btnSimpan)

        self.layout.addWidget(self.group)

        # TOMBOL KEMBALI
        self.layout_btn = QtWidgets.QHBoxLayout()
        self.btnKembali = QtWidgets.QPushButton("Kembali / Keluar")
        self.btnKembali.setObjectName("btnKembali")
        self.btnKembali.clicked.connect(FormTambahUser.close)
        self.layout_btn.addWidget(self.btnKembali)
        self.layout.addLayout(self.layout_btn)

        # CONNECT BUTTON
        self.btnSimpan.clicked.connect(self.aksi_simpan)

    def aksi_simpan(self):
        print("➤ Tombol Simpan Ditekan...")
        # 1. Ambil Input
        nama = self.lineEdit_nama.text()
        username = self.lineEdit_username.text()
        password = self.lineEdit_password.text()
        level = self.comboBox_level.currentText()

        # 2. Validasi
        if not nama or not username or not password:
            QMessageBox.warning(None, "Peringatan", "Mohon isi semua data!")
            return

        # 3. Panggil Fungsi Database
        sukses, pesan = User.insert_data(username, password, nama, level)

        if sukses:
            QMessageBox.information(None, "Berhasil", pesan)
            # Reset Form
            self.lineEdit_nama.clear()
            self.lineEdit_username.clear()
            self.lineEdit_password.clear()
            self.comboBox_level.setCurrentIndex(0)
        else:
            QMessageBox.critical(None, "Gagal", f"Gagal Menyimpan:\n{pesan}")

# ==========================================
# 3. EKSEKUSI PROGRAM
# ==========================================
if __name__ == "__main__":
    try:
        app = QtWidgets.QApplication(sys.argv)
        window = QtWidgets.QWidget()
        ui = Ui_FormTambahUser()
        ui.setupUi(window)
        window.show()
        print("➤ Jendela Ditampilkan. Silakan cek UI.")
        sys.exit(app.exec_())
    except Exception as e:
        print(f"❌ CRITICAL ERROR SAAT STARTUP: {e}")
        input("Tekan Enter untuk keluar...")