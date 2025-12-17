import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="pbo_uas"
)
mycursor=mydb.cursor()

class User:

    def __init__(self):
        self
  
    def login(username,password):
        sql = "SELECT level FROM user WHERE username=%s AND password=%s"
        val = (username, password)
        mycursor.execute(sql, val)
        result = mycursor.fetchone()
        return str(result[0])
        
    def insert_data(val1,val2,val3,val4):
        sql="INSERT INTO user (nama,username,password,level) VALUES (%s,%s,%s,%s)"
        val=(val1,val2,val3,val4)
        mycursor.execute(sql,val)
        mydb.commit()
        print(mycursor.rowcount,"Data berhasil ditambahkan...")

    def select_data_by_id(val1):
        sql = "SELECT nama,password,level FROM user WHERE username = %s"
        val = (val1)
        mycursor.execute(sql,val)
        myresult = mycursor.fetchone()
        return myresult
    
    def update_data(nama,username,password,level):
        sql = "UPDATE user SET nama = %s, password = %s, level = %s WHERE username = %s"
        val = (nama,username,password,level)
        mycursor.execute(sql,val)
        mydb.commit()
        print(mycursor.rowcount, "Data berhasil diupdate")
        
    def delete_data(val1):
        sql = "DELETE FROM user WHERE username = %s"
        value=(val1,)
        mycursor.execute(sql, value)
        mydb.commit()
        print(mycursor.rowcount, "Data Berhasil dihapus...")