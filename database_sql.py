import sqlite3
import acciones as a 
import main
import colorama as c

def conexion():
    try:
        conn = sqlite3.connect('inventario.db')
        return conn
    except sqlite3.Error as e:
        print(f"Error al conectar con la base de datos: {e}")
        return None
    
def crear_tabla():
    try:
        conn = conexion()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                cantidad INTEGER NO NULL,
                precio REAL NO NULL,
                categoria TEXT
            )
        ''')
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Error con la tabla:{e}")
        conn.rollback()
        conn.close()



def guardar_producto_sql(nombre,descripcion,cantidad,precio,categoria):
    try:
        conn=conexion()
        cursor=conn.cursor()
        cursor.execute("""INSERT INTO productos(nombre,descripcion,cantidad,precio,categoria)
                       VALUES (?,?,?,?,?)""",(nombre,descripcion,cantidad,precio,categoria))
        conn.commit()
        print(c.Fore.LIGHTGREEN_EX + "Producto registrado correctamente en la base de datos."+ c.Style.RESET_ALL)
        print("Volviendo al menu principal.")
        main.bucle_main()
    except sqlite3.Error as e:
        print(f"Error.no se pudo registrar el producto:{e}")
        conn.rollback()
        cursor.close
    
def consultar_productos_sql():
    try:
        conn=conexion()
        cursor=conn.cursor()
        cursor.execute("SELECT * FROM productos")
        inventario=cursor.fetchall()
        main.lista_consulta_producto(inventario)
        conn.close()    
        return inventario
    except sqlite3.Error as e:
        print(f"Error.no se puede consultar lo/s producto/s:{e}")
        conn.rollback()
        conn.close()

def mostrar_producto(indice):
    try:
        conn=conexion()
        cursor=conn.cursor()
        cursor.execute("SELECT * FROM productos WHERE id = ?",(indice,) )
        items=cursor.fetchall()
        
        main.lista_consulta_producto(items)
        cursor.close()
        return items
    except sqlite3.Error as e:
        print(f"Error.no se pudo mostrar el producto:{e}")
        conn.rollback()
        conn.close()
    
def modificar_producto_sql(new_valor:str,config:int,id_producto:int):
    lista=["nombre","descripcion","cantidad","precio","categoria"]
    try:
        conn=conexion()
        cursor=conn.cursor()
        cursor.execute(f"UPDATE productos set {lista[config]} = ? WHERE id = ?",(new_valor,id_producto))
        conn.commit()
        conn.close()
        print(f"La modificacion a sido exitosa. ")
    except sqlite3.Error as e:
        print(f"Error con la modificacion:{e}")
        conn.rollback()
        conn.close()

def borrar_producto_sql(producto):
    try:
        conn=conexion()
        cursor=conn.cursor()
        cursor.execute("DELETE FROM productos WHERE id = ?",(producto[0],))
        conn.commit()
        conn.close()
        print("El producto a sido eliminado exitosamente.volivendo al menu buscar producto")
        a.mostrar_productos()
    except sqlite3.Error as e:
        print(f"Error con la modificacion:{e}")
        conn.rollback()
        conn.close()

def notificaciones_sql(config=0):
    '''Funcion que trae los valores cantidad menor a la variable config '''
    if config == 0:
        with open ("config_notificaciones.txt","r") as configuracion:
            config=configuracion.read().strip()
        if not config.isdigit():
            config=0
        else:
            config=int(config)
    try:
        conn=conexion()
        cursor=conn.cursor()
        cursor.execute(
    "SELECT * FROM productos WHERE cantidad < ? or cantidad IS NULL",
    (config,))
        productos_noticaciones=cursor.fetchall()
        conn.close()
        return productos_noticaciones
    except sqlite3.Error as e:
        print(f"Error con la consulta de la tabla(notificaciones):{e}")
        conn.rollback()
        conn.close()