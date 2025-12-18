# -*- coding: utf-8 -*-
import sys
import mysql.connector
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from User import User

# ==========================================
# 1. KONFIGURASI DATABASE (MODEL)
# ==========================================
print("➤ Memulai Program Hapus User...")
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
            sql = "SELECT id, username, nama_lengkap, level FROM users WHERE id = %s"
            mycursor.execute(sql, (user_id,))
            result = mycursor.fetchone()
            
            if result:
                return result, "Data ditemukan"
            else:
                return None, "User tidak ditemukan"
        except mysql.connector.Error as err:
            return None, f"Error SQL: {err}"

    @staticmethod
    def delete_data(user_id):
        if mydb is None or not mydb.is_connected():
            return False, "Database tidak terhubung!"

        try:
            sql = "DELETE FROM users WHERE id = %s"
            mycursor.execute(sql, (user_id,))
            mydb.commit()
            
            if mycursor.rowcount > 0:
                print(f"➤ Data terhapus. Rows affected: {mycursor.rowcount}")
                return True, "Data berhasil dihapus!"
            else:
                return False, "Gagal menghapus (ID mungkin tidak ada)"
        except mysql.connector.Error as err:
            return False, f"Error Database: {err}"

# ==========================================
# 2. TAMPILAN UI (VIEW & CONTROLLER)
# ==========================================
class Ui_FormHapusUser(object):
    def setupUi(self, FormHapusUser):
        print("➤ Menyiapkan UI...")
        FormHapusUser.setObjectName("FormHapusUser")
        FormHapusUser.resize(600, 700)
        FormHapusUser.setStyleSheet("""
            QWidget { background-color: #121212; color: #E0E0E0; font-family: 'Segoe UI'; font-size: 11pt; }
            QGroupBox { background-color: #1E1E1E; border: 1px solid #333333; border-radius: 12px; margin-top: 24px; font-weight: bold; }
            QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; color: #FF5252; }
            QLabel { color: #B0B0B0; }
            QLineEdit { background-color: #2D2D2D; border: 1px solid #404040; border-radius: 8px; padding: 8px; color: #9E9E9E; }
            QLineEdit:enabled { color: white; }
            QPushButton { background-color: #333333; border: 1px solid #444444; border-radius: 8px; padding: 10px; color: white; font-weight: bold; }
            QPushButton#btnCari { background-color: #2962FF; border: none; }
            QPushButton#btnHapus { background-color: #D32F2F; border: none; }
            QPushButton#btnHapus:hover { background-color: #B71C1C; }
            QPushButton#btnKembali { background-color: #2962FF; border: none;}
        """)

        self.layout = QtWidgets.QVBoxLayout(FormHapusUser)

        # JUDUL
        self.label_judul = QtWidgets.QLabel("Hapus User")
        self.label_judul.setStyleSheet("font-size: 28px; font-weight: bold; margin-bottom: 20px; color: white;")
        self.label_judul.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.label_judul)

        # GROUP BOX
        self.group = QtWidgets.QGroupBox("Konfirmasi Hapus")
        self.form_layout = QtWidgets.QVBoxLayout(self.group)

        # SEARCH SECTION
        self.form_layout.addWidget(QtWidgets.QLabel("ID User:"))
        self.search_layout = QtWidgets.QHBoxLayout()
        
        self.lineEdit_id = QtWidgets.QLineEdit()
        self.lineEdit_id.setPlaceholderText("Masukkan ID...")
        self.lineEdit_id.setStyleSheet("color: white;")
        self.search_layout.addWidget(self.lineEdit_id)
        
        self.btnCari = QtWidgets.QPushButton("🔍 Cari")
        self.btnCari.setObjectName("btnCari")
        self.btnCari.setMaximumWidth(100)
        self.search_layout.addWidget(self.btnCari)
        
        self.form_layout.addLayout(self.search_layout)

        # FIELDS (READ ONLY)
        self.form_layout.addWidget(QtWidgets.QLabel("Nama:"))
        self.lineEdit_nama = QtWidgets.QLineEdit()
        self.lineEdit_nama.setReadOnly(True)
        self.form_layout.addWidget(self.lineEdit_nama)

        self.form_layout.addWidget(QtWidgets.QLabel("Username:"))
        self.lineEdit_username = QtWidgets.QLineEdit()
        self.lineEdit_username.setReadOnly(True)
        self.form_layout.addWidget(self.lineEdit_username)

        self.form_layout.addWidget(QtWidgets.QLabel("Level:"))
        self.lineEdit_level = QtWidgets.QLineEdit()
        self.lineEdit_level.setReadOnly(True)
        self.form_layout.addWidget(self.lineEdit_level)

        # SPACER
        self.form_layout.addItem(QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))

        # TOMBOL HAPUS
        self.btnHapus = QtWidgets.QPushButton("🗑 Hapus Permanen")
        self.btnHapus.setObjectName("btnHapus")
        self.btnHapus.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnHapus.setEnabled(False) # Disable dulu sebelum ketemu data
        self.form_layout.addWidget(self.btnHapus)

        self.layout.addWidget(self.group)

        # TOMBOL KEMBALI
        self.layout_btn = QtWidgets.QHBoxLayout()
        self.btnKembali = QtWidgets.QPushButton("Kembali")
        self.btnKembali.setObjectName("btnKembali")
        self.btnKembali.clicked.connect(FormHapusUser.close)
        self.layout_btn.addWidget(self.btnKembali)
        self.layout.addLayout(self.layout_btn)

        # CONNECT BUTTONS
        self.btnCari.clicked.connect(self.aksi_cari)
        self.btnHapus.clicked.connect(self.aksi_hapus)

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
            # data[0]=id, data[1]=username, data[2]=nama, data[3]=level
            self.lineEdit_username.setText(data[1])
            self.lineEdit_nama.setText(data[2])
            self.lineEdit_level.setText(data[3])
            
            # Aktifkan tombol hapus karena data ketemu
            self.btnHapus.setEnabled(True)
            self.btnHapus.setStyleSheet("background-color: #D32F2F; color: white; font-weight: bold;")
            
            QMessageBox.information(None, "Ditemukan", f"User '{data[2]}' ditemukan!")
        else:
            QMessageBox.warning(None, "Info", pesan)
            self.reset_form()

    def aksi_hapus(self):
        print("➤ Tombol Hapus Ditekan...")
        oid = self.lineEdit_id.text()
        nama = self.lineEdit_nama.text()

        if not oid or not nama:
            return

        # Konfirmasi User
        reply = QMessageBox.question(None, 'Konfirmasi Hapus', 
                                     f"Apakah Anda yakin ingin menghapus user '{nama}' secara permanen?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            # Panggil Model Hapus
            sukses, pesan = User.delete_data(oid)

            if sukses:
                QMessageBox.information(None, "Berhasil", pesan)
                self.lineEdit_id.clear()
                self.reset_form()
            else:
                QMessageBox.critical(None, "Gagal", f"Gagal Menghapus:\n{pesan}")

    def reset_form(self):
        self.lineEdit_username.clear()
        self.lineEdit_nama.clear()
        self.lineEdit_level.clear()
        self.btnHapus.setEnabled(False) # Disable tombol hapus lagi
        self.btnHapus.setStyleSheet("background-color: #333333; color: gray;")

# ==========================================
# 3. EKSEKUSI PROGRAM
# ==========================================
if __name__ == "__main__":
    try:
        app = QtWidgets.QApplication(sys.argv)
        window = QtWidgets.QWidget()
        ui = Ui_FormHapusUser()
        ui.setupUi(window)
        window.show()
        print("➤ Jendela Hapus User Ditampilkan.")
        sys.exit(app.exec_())
    except Exception as e:
        print(f"❌ CRITICAL ERROR SAAT STARTUP: {e}")
        input("Tekan Enter untuk keluar...")