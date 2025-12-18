# -*- coding: utf-8 -*-
import sys
import mysql.connector
import warnings
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox

# --- IMPORT FILE LAIN (Tanpa Subprocess) ---
# Pastikan nama file sesuai dengan yang Anda simpan
try:
    from User import User
    from createuser_fix import Ui_FormTambahUser
    from updateuser import Ui_FormUpdateUser
    from hapususer import Ui_FormHapusUser
except ImportError as e:
    print(f"❌ Error Import: {e}")
    print("Pastikan file createuser_fix.py, updateuser_fix.py, hapususer_fix.py, dan User.py ada di folder yang sama.")
    sys.exit(1)

# Matikan warning agar terminal bersih
warnings.filterwarnings("ignore", category=DeprecationWarning)

class Ui_FormListUser(object):
    def setupUi(self, FormListUser):
        FormListUser.setObjectName("FormListUser")
        FormListUser.resize(900, 700)
        
        # STYLE SHEET
        FormListUser.setStyleSheet("""
            QWidget { background-color: #121212; color: #E0E0E0; font-family: 'Segoe UI'; font-size: 11pt; }
            QFrame#card { background-color: #1E1E1E; border: 1px solid #333333; border-radius: 12px; }
            QLineEdit, QComboBox { 
                background-color: #2D2D2D; 
                border: 1px solid #404040; 
                border-radius: 8px; 
                padding: 6px 12px; 
                color: white; 
            }
            QLineEdit:focus, QComboBox:focus { border: 2px solid #2962FF; }
            
            QTableWidget { background-color: #1E1E1E; border: 1px solid #333333; gridline-color: #2C2C2C; border-radius: 8px; }
            QHeaderView::section { background-color: #252525; padding: 8px; border: none; border-bottom: 2px solid #2962FF; color: white; font-weight: bold; }
            
            QPushButton { background-color: #333333; border: 1px solid #444444; border-radius: 8px; padding: 10px; color: white; font-weight: bold; }
            QPushButton:hover { background-color: #424242; }
            
            QPushButton#btnTambah, QPushButton#btnUpdate { background-color: #2962FF; border: none; }
            QPushButton#btnTambah:hover, QPushButton#btnUpdate:hover { background-color: #1565C0; }
            
            QPushButton#btnHapus { background-color: #D32F2F; border: none; }
            QPushButton#btnHapus:hover { background-color: #B71C1C; }
            
            QPushButton#btnKembali { background-color: #757575; border: none; }
            QPushButton#btnKembali:hover { background-color: #616161; }
            
            QPushButton#btnCari { background-color: #2D2D2D; padding: 6px 12px; }
            QPushButton#btnCari:hover { background-color: #383838; }
        """)

        self.centralwidget = QtWidgets.QWidget(FormListUser)
        self.mainLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.mainLayout.setContentsMargins(20, 20, 20, 20)

        # CARD CONTAINER
        self.card = QtWidgets.QFrame(self.centralwidget)
        self.card.setObjectName("card")
        self.cardLayout = QtWidgets.QVBoxLayout(self.card)

        # TITLE
        self.label = QtWidgets.QLabel("👤 Manajemen User")
        self.label.setStyleSheet("font-size: 20pt; font-weight: bold; color: white; margin-bottom: 10px;")
        self.cardLayout.addWidget(self.label)

        # FILTER AREA
        self.filterLayout = QtWidgets.QHBoxLayout()
        self.filterLayout.setContentsMargins(0, 0, 0, 10)
        
        self.lineEdit_search = QtWidgets.QLineEdit()
        self.lineEdit_search.setMinimumSize(250, 35)
        self.lineEdit_search.setPlaceholderText("🔍 Cari Nama atau Username...")
        self.filterLayout.addWidget(self.lineEdit_search)
        
        self.comboBox_filterLevel = QtWidgets.QComboBox()
        self.comboBox_filterLevel.setMinimumSize(150, 35)
        self.comboBox_filterLevel.addItems(["Semua Level", "Admin", "User"])
        self.filterLayout.addWidget(self.comboBox_filterLevel)
        
        self.btnCari = QtWidgets.QPushButton("Cari")
        self.btnCari.setObjectName("btnCari")
        self.btnCari.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.filterLayout.addWidget(self.btnCari)
        
        self.filterLayout.addStretch()
        self.cardLayout.addLayout(self.filterLayout)

        # TABLE
        self.tableUser = QtWidgets.QTableWidget()
        self.tableUser.setColumnCount(5)
        self.tableUser.setHorizontalHeaderLabels(["ID", "Nama", "Username", "Level", "Password"])
        self.tableUser.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tableUser.setAlternatingRowColors(True)
        self.cardLayout.addWidget(self.tableUser)

        # BUTTONS AREA
        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.buttonLayout.setSpacing(10)
        
        self.btnTambah = QtWidgets.QPushButton("+ Tambah User")
        self.btnTambah.setObjectName("btnTambah")
        self.btnTambah.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.buttonLayout.addWidget(self.btnTambah)
        
        self.btnUpdate = QtWidgets.QPushButton("✎ Update User")
        self.btnUpdate.setObjectName("btnUpdate")
        self.btnUpdate.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.buttonLayout.addWidget(self.btnUpdate)
        
        self.btnHapus = QtWidgets.QPushButton("🗑 Hapus User")
        self.btnHapus.setObjectName("btnHapus")
        self.btnHapus.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.buttonLayout.addWidget(self.btnHapus)
        
        self.btnKembali = QtWidgets.QPushButton("⬅ Kembali")
        self.btnKembali.setObjectName("btnKembali")
        self.btnKembali.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.buttonLayout.addWidget(self.btnKembali)

        self.cardLayout.addLayout(self.buttonLayout)
        self.mainLayout.addWidget(self.card)
        FormListUser.setCentralWidget(self.centralwidget)

        # --- LOGIKA TOMBOL ---
        self.btnCari.clicked.connect(self.load_data) 
        self.btnTambah.clicked.connect(self.open_tambah)
        self.btnUpdate.clicked.connect(self.open_update)
        self.btnHapus.clicked.connect(self.open_hapus)
        self.btnKembali.clicked.connect(FormListUser.close)

        # Load data awal
        self.load_data()

    # --- FUNGSI LOAD DATA ---
    def load_data(self):
        keyword = self.lineEdit_search.text()
        level = self.comboBox_filterLevel.currentText()
        
        if keyword or level != "Semua Level":
            data = User.search(keyword, level)
        else:
            data = User.get_all()
            
        self.tableUser.setRowCount(0)
        for row_idx, row_data in enumerate(data):
            self.tableUser.insertRow(row_idx)
            for col_idx, col_data in enumerate(row_data):
                self.tableUser.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

    # --- FUNGSI BUKA WINDOW (MENGGUNAKAN IMPORT) ---
    
    def open_tambah(self):
        # 1. Buat Instance QWidget baru
        self.window_tambah = QtWidgets.QWidget() 
        # 2. Panggil Class UI dari file createuser_fix
        self.ui_tambah = Ui_FormTambahUser()
        # 3. Setup UI ke window baru
        self.ui_tambah.setupUi(self.window_tambah)
        # 4. Tampilkan
        self.window_tambah.show()

    def open_update(self):
        self.window_update = QtWidgets.QWidget()
        self.ui_update = Ui_FormUpdateUser()
        self.ui_update.setupUi(self.window_update)
        self.window_update.show()

    def open_hapus(self):
        self.window_hapus = QtWidgets.QWidget()
        self.ui_hapus = Ui_FormHapusUser()
        self.ui_hapus.setupUi(self.window_hapus)
        self.window_hapus.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    FormListUser = QtWidgets.QMainWindow()
    ui = Ui_FormListUser()
    ui.setupUi(FormListUser)
    FormListUser.show()
    sys.exit(app.exec_())