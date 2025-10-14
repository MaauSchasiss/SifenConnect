from database import engine

try:
    # Conexión directa para probar
    connection = engine.connect()
    print("¡Conexión exitosa a PostgreSQL!")
    connection.close()
except Exception as e:
    print("Error al conectar:", e)
