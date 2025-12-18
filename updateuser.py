# -*- coding: utf-8 -*-
import sys
import mysql.connector
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

# ==========================================
# 1. KONFIGURASI DATABASE (MODEL)
# ==========================================
print("➤ Memulai Program Update User...")
print("➤ Menghubungkan ke Database...")

mydb = None
mycursor = None

try:
    # Coba koneksi ke Database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",       # Sesuaikan password XAMPP
        database="pbo_uas" # Pastikan nama database BENAR
    )
    mycursor = mydb.cursor()
    print("✅ Koneksi Database BERHASIL!")
except mysql.connector.Error as e:
    print(f"❌ KONEKSI GAGAL: {e}")
    print("   Pastikan XAMPP (MySQL) sudah di-Start.")

class User:
    @staticmethod
    def select_data_by_id(user_id):
        # Cek koneksi
        if mydb is None or not mydb.is_connected():
            return None, "Database tidak terhubung!"
        
        try:
            # Query Select by ID
            sql = "SELECT id, username, nama_lengkap, level, password FROM users WHERE id = %s"
            mycursor.execute(sql, (user_id,))
            result = mycursor.fetchone()
            
            if result:
                return result, "Data ditemukan"
            else:
                return None, "User tidak ditemukan"
        except mysql.connector.Error as err:
            return None, f"Error SQL: {err}"

    @staticmethod
    def update_data(user_id, username, nama_lengkap, password, level):
        if mydb is None or not mydb.is_connected():
            return False, "Database tidak terhubung!"

        try:
            # Jika password diisi, update password juga
            if password:
                sql = "UPDATE users SET username=%s, nama_lengkap=%s, password=%s, level=%s WHERE id=%s"
                val = (username, nama_lengkap, password, level, user_id)
            else:
                # Jika password kosong, jangan ubah password lama
                sql = "UPDATE users SET username=%s, nama_lengkap=%s, level=%s WHERE id=%s"
                val = (username, nama_lengkap, level, user_id)

            mycursor.execute(sql, val)
            mydb.commit()
            print(f"➤ Data terupdate. Rows affected: {mycursor.rowcount}")
            return True, "Data berhasil diupdate!"
        except mysql.connector.Error as err:
            return False, f"Error Database: {err}"

# ==========================================
# 2. TAMPILAN UI (VIEW & CONTROLLER)
# ==========================================
class Ui_FormUpdateUser(object):
    def setupUi(self, FormUpdateUser):
        print("➤ Menyiapkan UI...")
        FormUpdateUser.setObjectName("FormUpdateUser")
        FormUpdateUser.resize(600, 750)
        FormUpdateUser.setStyleSheet("""
            QWidget { background-color: #121212; color: #E0E0E0; font-family: 'Segoe UI'; font-size: 11pt; }
            QGroupBox { background-color: #1E1E1E; border: 1px solid #333333; border-radius: 12px; margin-top: 24px; font-weight: bold; }
            QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; color: #82B1FF; }
            QLineEdit, QComboBox { background-color: #2D2D2D; border: 1px solid #404040; border-radius: 8px; padding: 8px; color: white; }
            QLineEdit:focus, QComboBox:focus { border: 2px solid #2962FF; }
            QPushButton { background-color: #333333; border: 1px solid #444444; border-radius: 8px; padding: 10px; color: white; font-weight: bold; }
            QPushButton:hover { background-color: #424242; }
            QPushButton#btnCari, QPushButton#btnUpdate { background-color: #2962FF; border: none; }
            QPushButton#btnCari:hover, QPushButton#btnUpdate:hover { background-color: #1565C0; }
            QPushButton#btnKembali { background-color: #D32F2F; border: none; }
            QPushButton#btnKembali:hover { background-color: #B71C1C; }
        """)

        self.layout = QtWidgets.QVBoxLayout(FormUpdateUser)

        # JUDUL
        self.label_judul = QtWidgets.QLabel("Update User")
        self.label_judul.setStyleSheet("font-size: 28px; font-weight: bold; margin-bottom: 20px;")
        self.label_judul.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.label_judul)

        # GROUP BOX
        self.group = QtWidgets.QGroupBox("Edit Data User")
        self.form_layout = QtWidgets.QVBoxLayout(self.group)

        # SEARCH SECTION
        self.form_layout.addWidget(QtWidgets.QLabel("Cari ID User:"))
        self.search_layout = QtWidgets.QHBoxLayout()
        
        self.lineEdit_id = QtWidgets.QLineEdit()
        self.lineEdit_id.setPlaceholderText("Masukkan ID...")
        self.search_layout.addWidget(self.lineEdit_id)
        
        self.btnCari = QtWidgets.QPushButton("🔍 Cari")
        self.btnCari.setObjectName("btnCari")
        self.btnCari.setMaximumWidth(100)
        self.search_layout.addWidget(self.btnCari)
        
        self.form_layout.addLayout(self.search_layout)

        # FIELDS
        self.form_layout.addWidget(QtWidgets.QLabel("Nama Baru:"))
        self.lineEdit_nama = QtWidgets.QLineEdit()
        self.lineEdit_nama.setPlaceholderText("Nama Lengkap")
        self.form_layout.addWidget(self.lineEdit_nama)

        self.form_layout.addWidget(QtWidgets.QLabel("Username Baru:"))
        self.lineEdit_username = QtWidgets.QLineEdit()
        self.lineEdit_username.setPlaceholderText("Username")
        self.form_layout.addWidget(self.lineEdit_username)

        self.form_layout.addWidget(QtWidgets.QLabel("Password Baru:"))
        self.lineEdit_password = QtWidgets.QLineEdit()
        self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_password.setPlaceholderText("Kosongkan jika tidak ingin diubah")
        self.form_layout.addWidget(self.lineEdit_password)

        self.form_layout.addWidget(QtWidgets.QLabel("Level Akses:"))
        self.comboBox_level = QtWidgets.QComboBox()
        self.comboBox_level.addItems(["User", "Admin"])
        self.form_layout.addWidget(self.comboBox_level)

        # SPACER
        self.form_layout.addItem(QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))

        # TOMBOL UPDATE
        self.btnUpdate = QtWidgets.QPushButton("💾 Simpan Perubahan")
        self.btnUpdate.setObjectName("btnUpdate")
        self.form_layout.addWidget(self.btnUpdate)

        self.layout.addWidget(self.group)

        # TOMBOL KEMBALI
        self.layout_btn = QtWidgets.QHBoxLayout()
        self.btnKembali = QtWidgets.QPushButton("Kembali")
        self.btnKembali.setObjectName("btnKembali")
        self.btnKembali.clicked.connect(FormUpdateUser.close)
        self.layout_btn.addWidget(self.btnKembali)
        self.layout.addLayout(self.layout_btn)

        # CONNECT BUTTONS
        self.btnCari.clicked.connect(self.aksi_cari)
        self.btnUpdate.clicked.connect(self.aksi_update)

    def aksi_cari(self):
        print("➤ Tombol Cari Ditekan...")
        oid = self.lineEdit_id.text()
        
        if not oid:
            QMessageBox.warning(None, "Peringatan", "Masukkan ID User terlebih dahulu!")
            return

        # Panggil Model
        data, pesan = User.select_data_by_id(oid)
        
        if data:
            print(f"➤ Data Ditemukan: {data}")
            # data[0]=id, data[1]=username, data[2]=nama, data[3]=level, data[4]=password
            self.lineEdit_username.setText(data[1])
            self.lineEdit_nama.setText(data[2])
            
            # Set Combo Box
            index = self.comboBox_level.findText(data[3], QtCore.Qt.MatchFixedString)
            if index >= 0:
                self.comboBox_level.setCurrentIndex(index)
            
            self.lineEdit_password.clear()
            QMessageBox.information(None, "Ditemukan", f"User '{data[2]}' ditemukan!")
        else:
            QMessageBox.warning(None, "Info", pesan)
            self.reset_form()

    def aksi_update(self):
        print("➤ Tombol Update Ditekan...")
        oid = self.lineEdit_id.text()
        nama = self.lineEdit_nama.text()
        username = self.lineEdit_username.text()
        password = self.lineEdit_password.text()
        level = self.comboBox_level.currentText()

        if not oid:
            QMessageBox.warning(None, "Peringatan", "Cari ID dulu sebelum update!")
            return
        
        if not nama or not username:
            QMessageBox.warning(None, "Peringatan", "Nama dan Username wajib diisi!")
            return

        # Panggil Model Update
        sukses, pesan = User.update_data(oid, username, nama, password, level)

        if sukses:
            QMessageBox.information(None, "Berhasil", pesan)
            self.lineEdit_id.clear()
            self.reset_form()
        else:
            QMessageBox.critical(None, "Gagal", f"Gagal Update:\n{pesan}")

    def reset_form(self):
        self.lineEdit_username.clear()
        self.lineEdit_nama.clear()
        self.lineEdit_password.clear()
        self.comboBox_level.setCurrentIndex(0)

# ==========================================
# 3. EKSEKUSI PROGRAM
# ==========================================
if __name__ == "__main__":
    try:
        app = QtWidgets.QApplication(sys.argv)
        window = QtWidgets.QWidget()
        ui = Ui_FormUpdateUser()
        ui.setupUi(window)
        window.show()
        print("➤ Jendela Update User Ditampilkan.")
        sys.exit(app.exec_())
    except Exception as e:
        print(f"❌ CRITICAL ERROR SAAT STARTUP: {e}")
        input("Tekan Enter untuk keluar...")