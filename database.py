import mysql.connector

def connect_to_db():
    """
    Establece la conexión con la base de datos remota en Railway usando las variables proporcionadas.
    """
    conn = mysql.connector.connect(
        host="mysql.railway.internal",  # MYSQLHOST
        user="root",                   # Usuario raíz de la base de datos
        password="AALCqBDaYexmmkDBZzqGgdMXpBpcwDIj",  # MYSQLPASSWORD
        database="railway",            # MYSQLDATABASE
        port=3306                      # MYSQLPORT
    )
    return conn

# Prueba de conexión
if __name__ == "__main__":
    try:
        connection = connect_to_db()
        print("Conexión exitosa a la base de datos.")
        connection.close()
    except mysql.connector.Error as err:
        print(f"Error al conectar a la base de datos: {err}")
