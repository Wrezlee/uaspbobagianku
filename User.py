import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",      
    database="pbo_uas" 
)

mycursor = mydb.cursor()

class User:
    
    # Konstruktor kosong (opsional)
    def __init__(self):
        pass

    # --- CREATE (INSERT) ---
    def insert_data(username, password, nama_lengkap, level):
        sql = "INSERT INTO users (username, password, nama_lengkap, level) VALUES (%s, %s, %s, %s)"
        val = (username, password, nama_lengkap, level)
        
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "Data user berhasil ditambahkan")
        return True

    # --- READ (GET ALL) ---
    def get_all():
        sql = "SELECT id, username, nama_lengkap, level, password FROM users"
        mycursor.execute(sql)
        result = mycursor.fetchall()
        return result

    # --- READ (SEARCH) ---
    def search(keyword, level):
        if level == "Semua Level" or level == "":
            sql = "SELECT id, username, nama_lengkap, level, password FROM users WHERE username LIKE %s OR nama_lengkap LIKE %s"
            val = (f"%{keyword}%", f"%{keyword}%")
        else:
            sql = "SELECT id, username, nama_lengkap, level, password FROM users WHERE (username LIKE %s OR nama_lengkap LIKE %s) AND level = %s"
            val = (f"%{keyword}%", f"%{keyword}%", level)
        
        mycursor.execute(sql, val)
        return mycursor.fetchall()

    # --- READ (GET BY ID - Untuk Update/Hapus) ---
    def select_data_by_id(id):
        sql = "SELECT id, username, nama_lengkap, level, password FROM users WHERE id = %s"
        val = (id,)
        mycursor.execute(sql, val)
        return mycursor.fetchone()

    # --- UPDATE ---
    def update_data(id, username, nama_lengkap, password, level):
        if password:
            # Jika password diisi, update password juga
            sql = "UPDATE users SET username=%s, nama_lengkap=%s, password=%s, level=%s WHERE id=%s"
            val = (username, nama_lengkap, password, level, id)
        else:
            # Jika password kosong, jangan ubah password lama
            sql = "UPDATE users SET username=%s, nama_lengkap=%s, level=%s WHERE id=%s"
            val = (username, nama_lengkap, level, id)

        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "Data berhasil diupdate")
        return True

    # --- DELETE ---
    def delete_data(id):
        sql = "DELETE FROM users WHERE id = %s"
        val = (id,)
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "Data berhasil dihapus")
        return True