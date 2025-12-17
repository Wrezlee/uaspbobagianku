import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="pbo_uas"
)

mycursor = mydb.cursor()


class User:

    @staticmethod
    def get_all():
        sql = """
            SELECT id, username, password, nama_lengkap, level
            FROM users
        """
        mycursor.execute(sql)
        return mycursor.fetchall()

    @staticmethod
    def search(keyword, level):
        if level == "" or level == "Semua Level":
            sql = """
                SELECT id, username, password, nama_lengkap, level
                FROM users
                WHERE username LIKE %s
                   OR nama_lengkap LIKE %s
            """
            val = (f"%{keyword}%", f"%{keyword}%")
        else:
            sql = """
                SELECT id, username, password, nama_lengkap, level
                FROM users
                WHERE (username LIKE %s OR nama_lengkap LIKE %s)
                  AND level = %s
            """
            val = (f"%{keyword}%", f"%{keyword}%", level.lower())

        mycursor.execute(sql, val)
        return mycursor.fetchall()

    @staticmethod
    def insert_data(username, password, nama_lengkap, level):
        sql = """
            INSERT INTO users (username, password, nama_lengkap, level)
            VALUES (%s, %s, %s, %s)
        """
        val = (username, password, nama_lengkap, level.lower())
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "User berhasil ditambahkan")

    @staticmethod
    def get_by_id(user_id):
        sql = """
            SELECT id, username, password, nama_lengkap, level
            FROM users
            WHERE id = %s
        """
        mycursor.execute(sql, (user_id,))
        return mycursor.fetchone()

    @staticmethod
    def update_data(user_id, username, nama_lengkap, level, password=None):
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

    @staticmethod
    def delete_data(user_id):
        sql = "DELETE FROM users WHERE id=%s"
        mycursor.execute(sql, (user_id,))
        mydb.commit()
        print(mycursor.rowcount, "User berhasil dihapus")
