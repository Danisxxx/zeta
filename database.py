import mysql.connector

def connect_to_db():
    """
    Establece la conexión a la base de datos MySQL en Railway.
    
    :return: Conexión activa a la base de datos.
    :raises mysql.connector.Error: Si ocurre un error al conectar.
    """
    try:
        # Configuración basada en los datos proporcionados por Railway
        conn = mysql.connector.connect(
            host="junction.proxy.rlwy.net",  # Host proporcionado
            user="root",                     # Usuario
            password="********",             # Contraseña (reemplazar con la real)
            database="railway",              # Nombre de la base de datos
            port=32786                       # Puerto proporcionado
        )
        print("Conexión exitosa a la base de datos")
        return conn
    except mysql.connector.Error as err:
        print(f"Error al conectar a la base de datos: {err}")
        raise

# Prueba de conexión (opcional, para verificar)
if __name__ == "__main__":
    try:
        connection = connect_to_db()
        connection.close()
    except Exception as e:
        print(f"No se pudo conectar a la base de datos: {e}")
