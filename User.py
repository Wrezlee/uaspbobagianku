import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="pbo_uas"
)

mycursor = mydb.cursor()


class User:

    def __init__(self):
        pass

    def get_all():
        sql = """
            SELECT id, username, nama_lengkap, level, password
            FROM users
        """
        mycursor.execute(sql)
        return mycursor.fetchall()

    def search(keyword, level):
        if level in ("", "Semua Level"):
            sql = """
                SELECT id, username, nama_lengkap, level, password
                FROM users
                WHERE nama_lengkap LIKE %s OR username LIKE %s
            """
            val = (f"%{keyword}%", f"%{keyword}%")
        else:
            sql = """
                SELECT id, username, nama_lengkap, level, password
                FROM users
                WHERE (nama_lengkap LIKE %s OR username LIKE %s)
                AND level = %s
            """
            val = (f"%{keyword}%", f"%{keyword}%", level.lower())

        mycursor.execute(sql, val)
        return mycursor.fetchall()

    def insert_data(id_user, username, password, nama_lengkap, level):
        sql = """
            INSERT INTO users (id, username, password, nama_lengkap, level)
            VALUES (%s, %s, %s, %s, %s)
        """
        val = (id_user, username, password, nama_lengkap, level.lower())
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "User berhasil ditambahkan")

    def select_data_by_id(user_id):
        sql = """
            SELECT id, username, nama_lengkap, level
            FROM users
            WHERE id = %s
        """
        mycursor.execute(sql, (user_id,))
        return mycursor.fetchone()

    def update_data(user_id, username, nama_lengkap, password, level):
        if password:
            sql = """
                UPDATE users
                SET username=%s,
                    nama_lengkap=%s,
                    password=%s,
                    level=%s
                WHERE id=%s
            """
            val = (username, nama_lengkap, password, level.lower(), user_id)
        else:
            sql = """
                UPDATE users
                SET username=%s,
                    nama_lengkap=%s,
                    level=%s
                WHERE id=%s
            """
            val = (username, nama_lengkap, level.lower(), user_id)

        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "User berhasil diupdate")

    def delete_data(user_id):
        sql = "DELETE FROM users WHERE id=%s"
        mycursor.execute(sql, (user_id,))
        mydb.commit()
        print(mycursor.rowcount, "User berhasil dihapus")
